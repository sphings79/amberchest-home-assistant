"""Binary sensor: is a backup running right now."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import AmberChestConfigEntry, AmberChestCoordinator
from .entity import AmberChestAccountEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AmberChestConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """One running flag per mailbox."""
    coordinator = entry.runtime_data
    async_add_entities(
        BackupRunningSensor(coordinator, account_id)
        for account_id in coordinator.data.accounts
    )


class BackupRunningSensor(AmberChestAccountEntity, BinarySensorEntity):
    """On while AmberChest is talking to this mailbox."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING

    def __init__(self, coordinator: AmberChestCoordinator, account_id: str) -> None:
        """Name the entity."""
        super().__init__(coordinator, account_id, "backup_running")

    @property
    def is_on(self) -> bool:
        """Whether a backup is going on."""
        return bool(self.overview.get("running"))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """What the backup is doing, while it does it."""
        progress = self.overview.get("progress") or {}
        return {
            "phase": progress.get("phase"),
            "folder": progress.get("currentFolder"),
            "messages_done": progress.get("folderMessagesDone"),
            "messages_total": progress.get("folderMessagesTotal"),
        }
