"""Shared entity base, so every platform describes its devices the same way."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MailArchiverCoordinator


class MailArchiverEntity(CoordinatorEntity[MailArchiverCoordinator]):
    """An entity that belongs to the instance as a whole."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MailArchiverCoordinator, key: str) -> None:
        """Attach the entity to the server device."""
        super().__init__(coordinator)
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name="Mail Archiver",
            manufacturer="Mail Archiver",
            model="Mail backup",
            configuration_url=coordinator.client.base_url,
        )


class MailArchiverAccountEntity(CoordinatorEntity[MailArchiverCoordinator]):
    """An entity that belongs to one mailbox."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: MailArchiverCoordinator, account_id: str, key: str
    ) -> None:
        """Attach the entity to the device of its mailbox."""
        super().__init__(coordinator)
        self.account_id = account_id
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_{account_id}_{key}"
        self._attr_translation_key = key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{account_id}")},
            name=self.account.get("name", "Mailbox"),
            manufacturer="Mail Archiver",
            model="IMAP account",
            via_device=(DOMAIN, entry_id),
            configuration_url=coordinator.client.base_url,
        )

    @property
    def overview(self) -> dict[str, Any]:
        """The last poll for this mailbox, or an empty document."""
        return self.coordinator.data.accounts.get(self.account_id, {})

    @property
    def account(self) -> dict[str, Any]:
        """The stored account details of this mailbox."""
        return self.overview.get("account", {})

    @property
    def available(self) -> bool:
        """A mailbox that was removed in Mail Archiver is not available."""
        return super().available and self.account_id in self.coordinator.data.accounts
