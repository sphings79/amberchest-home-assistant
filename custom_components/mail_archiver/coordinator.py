"""Polls one Mail Archiver instance and hands the result to the entities."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MailArchiverAuthError, MailArchiverClient, MailArchiverError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

LOGGER = logging.getLogger(__package__)

type MailArchiverConfigEntry = ConfigEntry[MailArchiverCoordinator]


@dataclass
class MailArchiverData:
    """Everything one poll brings back."""

    accounts: dict[str, dict[str, Any]] = field(default_factory=dict)
    total_bytes: int = 0
    total_messages: int = 0
    next_run: str | None = None
    cron: str | None = None


class MailArchiverCoordinator(DataUpdateCoordinator[MailArchiverData]):
    """Asks the server for the state of every mailbox."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: MailArchiverConfigEntry,
        client: MailArchiverClient,
    ) -> None:
        """Set up the polling loop."""
        super().__init__(
            hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
            config_entry=entry,
        )
        self.client = client

    async def _async_update_data(self) -> MailArchiverData:
        try:
            accounts = await self.client.accounts()
            schedule = await self.client.schedule()
        except MailArchiverAuthError as error:
            raise ConfigEntryAuthFailed(str(error)) from error
        except MailArchiverError as error:
            raise UpdateFailed(str(error)) from error

        data = MailArchiverData(
            next_run=schedule.get("nextRun"),
            cron=schedule.get("expression"),
        )
        for overview in accounts:
            account_id = overview["account"]["id"]
            data.accounts[account_id] = overview
            data.total_bytes += overview.get("bytes", 0)
            data.total_messages += overview.get("messageCount", 0)
        return data
