"""Buttons: start a backup, or stop one that is running."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .api import MailArchiverError
from .const import DOMAIN
from .coordinator import MailArchiverConfigEntry, MailArchiverCoordinator
from .entity import MailArchiverAccountEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MailArchiverConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Create a backup and a cancel button per mailbox."""
    coordinator = entry.runtime_data
    entities: list[ButtonEntity] = []
    for account_id in coordinator.data.accounts:
        entities.append(BackupButton(coordinator, account_id))
        entities.append(CancelButton(coordinator, account_id))
    async_add_entities(entities)


class BackupButton(MailArchiverAccountEntity, ButtonEntity):
    """Start a backup of this mailbox."""

    def __init__(self, coordinator: MailArchiverCoordinator, account_id: str) -> None:
        """Name the entity."""
        super().__init__(coordinator, account_id, "backup_now")

    async def async_press(self) -> None:
        """Ask the server to back up, then refresh so the flag flips."""
        try:
            await self.coordinator.client.start_backup(self.account_id)
        except MailArchiverError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="backup_failed",
                translation_placeholders={"error": str(error)},
            ) from error
        await self.coordinator.async_request_refresh()


class CancelButton(MailArchiverAccountEntity, ButtonEntity):
    """Stop the backup of this mailbox."""

    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator: MailArchiverCoordinator, account_id: str) -> None:
        """Name the entity."""
        super().__init__(coordinator, account_id, "cancel_backup")

    async def async_press(self) -> None:
        """Ask the server to stop, then refresh."""
        try:
            await self.coordinator.client.cancel_backup(self.account_id)
        except MailArchiverError as error:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="cancel_failed",
                translation_placeholders={"error": str(error)},
            ) from error
        await self.coordinator.async_request_refresh()
