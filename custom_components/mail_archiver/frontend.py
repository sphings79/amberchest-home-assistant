"""Serves the Lovelace card and registers it as a resource."""

from __future__ import annotations

import logging

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant
from homeassistant.loader import async_get_integration

from .const import DOMAIN

LOGGER = logging.getLogger(__package__)

CARD_FILE = "mail-archiver-card.js"
CARD_URL = f"/{DOMAIN}/{CARD_FILE}"
REGISTERED = f"{DOMAIN}_frontend_registered"


async def async_register_card(hass: HomeAssistant) -> None:
    """Publish the card once per Home Assistant process.

    Registering the static path twice raises, and a second config entry would
    do exactly that, so the fact that it happened is remembered in hass.data.
    """
    if hass.data.get(REGISTERED):
        return
    hass.data[REGISTERED] = True

    integration = await async_get_integration(hass, DOMAIN)
    root = integration.file_path / "frontend"

    await hass.http.async_register_static_paths(
        [StaticPathConfig(CARD_URL, str(root / CARD_FILE), cache_headers=False)]
    )

    # The version turns the browser cache over on an update.
    url = f"{CARD_URL}?v={integration.version}"
    await _add_resource(hass, url)


async def _add_resource(hass: HomeAssistant, url: str) -> None:
    """Add the card to the Lovelace resources, if that is possible."""
    lovelace = hass.data.get("lovelace")
    resources = getattr(lovelace, "resources", None)
    if resources is None:
        LOGGER.debug("Lovelace runs in YAML mode; add the card resource by hand")
        return

    if hasattr(resources, "async_get_info"):
        await resources.async_get_info()

    items = resources.async_items() or []
    for item in items:
        if str(item.get("url", "")).startswith(CARD_URL):
            if item["url"] != url:
                await resources.async_update_item(item["id"], {"url": url})
            return

    await resources.async_create_item({"res_type": "module", "url": url})
    LOGGER.info("Registered the Mail Archiver card as a Lovelace resource")
