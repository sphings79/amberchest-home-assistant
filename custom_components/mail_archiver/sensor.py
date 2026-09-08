"""Sensors: how much is archived, and when it last happened."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from .coordinator import MailArchiverConfigEntry, MailArchiverCoordinator
from .entity import MailArchiverAccountEntity, MailArchiverEntity


def _timestamp(value: str | None) -> datetime | None:
    """Mail Archiver sends ISO strings; Home Assistant wants aware datetimes."""
    return dt_util.parse_datetime(value) if value else None


@dataclass(frozen=True, kw_only=True)
class AccountSensorDescription(SensorEntityDescription):
    """A sensor that reads one value out of the overview of a mailbox."""

    value: Callable[[dict[str, Any]], Any]


ACCOUNT_SENSORS: tuple[AccountSensorDescription, ...] = (
    AccountSensorDescription(
        key="messages",
        translation_key="messages",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="messages",
        value=lambda overview: overview.get("messageCount", 0),
    ),
    AccountSensorDescription(
        key="archive_size",
        translation_key="archive_size",
        device_class=SensorDeviceClass.DATA_SIZE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfInformation.BYTES,
        suggested_unit_of_measurement=UnitOfInformation.MEGABYTES,
        suggested_display_precision=1,
        value=lambda overview: overview.get("bytes", 0),
    ),
    AccountSensorDescription(
        key="folders",
        translation_key="folders",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="folders",
        entity_registry_enabled_default=False,
        value=lambda overview: overview.get("folderCount", 0),
    ),
    AccountSensorDescription(
        key="last_backup",
        translation_key="last_backup",
        device_class=SensorDeviceClass.TIMESTAMP,
        value=lambda overview: _timestamp(
            (overview.get("lastRun") or {}).get("finished_at")
            or (overview.get("lastRun") or {}).get("started_at")
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MailArchiverConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Create the sensors for the instance and for every mailbox."""
    coordinator = entry.runtime_data

    entities: list[SensorEntity] = [
        TotalSizeSensor(coordinator),
        NextRunSensor(coordinator),
    ]
    for account_id in coordinator.data.accounts:
        entities.extend(
            AccountSensor(coordinator, account_id, description)
            for description in ACCOUNT_SENSORS
        )
    async_add_entities(entities)


class AccountSensor(MailArchiverAccountEntity, SensorEntity):
    """One number of one mailbox."""

    entity_description: AccountSensorDescription

    def __init__(
        self,
        coordinator: MailArchiverCoordinator,
        account_id: str,
        description: AccountSensorDescription,
    ) -> None:
        """Remember which value this sensor shows."""
        super().__init__(coordinator, account_id, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> Any:
        """The current value, straight out of the last poll."""
        return self.entity_description.value(self.overview)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """The result of the last backup, on the "last backup" sensor only."""
        if self.entity_description.key != "last_backup":
            return None
        run = self.overview.get("lastRun") or {}
        stats = run.get("stats")
        if isinstance(stats, str):
            # SQLite has no object column, so the statistics arrive as text.
            try:
                stats = json.loads(stats)
            except ValueError:
                stats = {}
        stats = stats or {}
        return {
            "status": run.get("status"),
            "new": stats.get("messagesNew", 0),
            "moved": stats.get("messagesMoved", 0),
            "removed": stats.get("messagesDeleted", 0),
            "error": run.get("error"),
        }


class TotalSizeSensor(MailArchiverEntity, SensorEntity):
    """The size of the whole archive."""

    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfInformation.BYTES
    _attr_suggested_unit_of_measurement = UnitOfInformation.MEGABYTES
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: MailArchiverCoordinator) -> None:
        """Name the entity."""
        super().__init__(coordinator, "total_size")

    @property
    def native_value(self) -> int:
        """Bytes across every mailbox."""
        return self.coordinator.data.total_bytes

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """The numbers that do not deserve a sensor of their own."""
        return {
            "accounts": len(self.coordinator.data.accounts),
            "messages": self.coordinator.data.total_messages,
        }


class NextRunSensor(MailArchiverEntity, SensorEntity):
    """When the container will back up next; unknown without a schedule."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator: MailArchiverCoordinator) -> None:
        """Name the entity."""
        super().__init__(coordinator, "next_run")

    @property
    def native_value(self) -> datetime | None:
        """The next scheduled run."""
        return _timestamp(self.coordinator.data.next_run)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """The cron expression behind it, for the curious."""
        return {"cron": self.coordinator.data.cron}
