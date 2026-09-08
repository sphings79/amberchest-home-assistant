"""Setting the integration up from the interface."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_SSL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)
import voluptuous as vol

from .api import (
    MailArchiverAuthError,
    MailArchiverClient,
    MailArchiverError,
)
from .const import CONF_VERIFY_SSL, DEFAULT_PORT, DOMAIN


def schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """Build the form, pre-filled when an existing entry is being repaired."""
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(CONF_HOST, default=defaults.get(CONF_HOST, "")): str,
            vol.Required(CONF_PORT, default=defaults.get(CONF_PORT, DEFAULT_PORT)): int,
            vol.Optional(CONF_PASSWORD, default=""): TextSelector(
                TextSelectorConfig(type=TextSelectorType.PASSWORD)
            ),
            vol.Optional(CONF_SSL, default=defaults.get(CONF_SSL, False)): bool,
            vol.Optional(
                CONF_VERIFY_SSL, default=defaults.get(CONF_VERIFY_SSL, True)
            ): bool,
        }
    )


class MailArchiverConfigFlow(ConfigFlow, domain=DOMAIN):
    """Ask for the address of the instance and try it out."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Ask for the address and try it out."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}"
            )
            self._abort_if_unique_id_configured()

            error = await self._check(user_input)
            if error is None:
                return self.async_create_entry(
                    title=f"Mail Archiver ({user_input[CONF_HOST]})",
                    data=user_input,
                )
            errors["base"] = error

        return self.async_show_form(
            step_id="user", data_schema=schema(user_input), errors=errors
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Mail Archiver forgets its sessions on a restart; ask again."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Take a new password for the existing entry."""
        entry = self._get_reauth_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            merged = {**entry.data, **user_input}
            error = await self._check(merged)
            if error is None:
                return self.async_update_reload_and_abort(entry, data=merged)
            errors["base"] = error

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_PASSWORD, default=""): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    )
                }
            ),
            errors=errors,
        )

    async def _check(self, data: Mapping[str, Any]) -> str | None:
        """Return an error key, or None when the instance answered."""
        verify_ssl = data.get(CONF_VERIFY_SSL, True)
        scheme = "https" if data.get(CONF_SSL) else "http"
        client = MailArchiverClient(
            async_get_clientsession(self.hass, verify_ssl=verify_ssl),
            f"{scheme}://{data[CONF_HOST]}:{data[CONF_PORT]}",
            data.get(CONF_PASSWORD) or None,
            verify_ssl=verify_ssl,
        )

        try:
            state = await client.state()
        except MailArchiverError:
            return "cannot_connect"

        if not state.get("initialized"):
            return "not_initialized"

        # An instance with a password refuses everything until we log in.
        if state.get("authMode") == "password":
            if not data.get(CONF_PASSWORD):
                return "password_required"
            try:
                await client.login()
            except MailArchiverAuthError:
                return "invalid_auth"
            except MailArchiverError:
                return "cannot_connect"

        try:
            await client.accounts()
        except MailArchiverAuthError:
            return "invalid_auth"
        except MailArchiverError:
            # Reachable but locked, which sorts itself out once the master
            # password has been entered there.
            return "locked"

        return None
