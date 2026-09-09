"""The AmberChest integration for Home Assistant."""

from __future__ import annotations

from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_SSL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    AmberChestAuthError,
    AmberChestClient,
    AmberChestError,
    AmberChestLockedError,
)
from .const import CONF_VERIFY_SSL
from .coordinator import AmberChestConfigEntry, AmberChestCoordinator
from .frontend import async_register_card

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.BUTTON, Platform.SENSOR]


def build_url(host: str, port: int, ssl: bool) -> str:
    """Build the base URL of an instance, as the config entry describes it."""
    scheme = "https" if ssl else "http"
    return f"{scheme}://{host}:{port}"


async def async_setup_entry(
    hass: HomeAssistant, entry: AmberChestConfigEntry
) -> bool:
    """Set up one AmberChest instance."""
    verify_ssl = entry.data.get(CONF_VERIFY_SSL, True)
    client = AmberChestClient(
        async_get_clientsession(hass, verify_ssl=verify_ssl),
        build_url(
            entry.data[CONF_HOST],
            entry.data[CONF_PORT],
            entry.data.get(CONF_SSL, False),
        ),
        entry.data.get(CONF_PASSWORD),
        verify_ssl=verify_ssl,
    )

    try:
        await client.login()
    except AmberChestAuthError as error:
        raise ConfigEntryAuthFailed(str(error)) from error
    except AmberChestError as error:
        raise ConfigEntryNotReady(str(error)) from error

    coordinator = AmberChestCoordinator(hass, entry, client)
    try:
        await coordinator.async_config_entry_first_refresh()
    except AmberChestLockedError as error:
        # The master password has not been entered yet; try again later.
        raise ConfigEntryNotReady(str(error)) from error

    await async_register_card(hass)

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_reload))
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: AmberChestConfigEntry
) -> bool:
    """Tear the instance down again."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _reload(hass: HomeAssistant, entry: AmberChestConfigEntry) -> None:
    """Start over, which is the simplest way to apply a changed option."""
    await hass.config_entries.async_reload(entry.entry_id)
