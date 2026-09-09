"""Diagnostics, with the password left out."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.const import CONF_PASSWORD
from homeassistant.core import HomeAssistant

from .coordinator import AmberChestConfigEntry

REDACT = {CONF_PASSWORD, "email", "username", "host"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: AmberChestConfigEntry
) -> dict[str, Any]:
    """Everything that helps with a bug report, minus the personal parts."""
    coordinator = entry.runtime_data
    return {
        "entry": async_redact_data(dict(entry.data), REDACT),
        "accounts": [
            async_redact_data(overview, REDACT)
            for overview in coordinator.data.accounts.values()
        ],
        "schedule": {
            "cron": coordinator.data.cron,
            "next_run": coordinator.data.next_run,
        },
    }
