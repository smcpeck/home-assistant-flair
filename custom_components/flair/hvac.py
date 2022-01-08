import logging
from homeassistant.exceptions import PlatformNotReady
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
ATTR_IS_ON = "is_on"

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Flair Vents."""
    flair = hass.data[DOMAIN]

    hvac_units = []
    try:
        for hvac in flair.hvac_units():
            hvac_units.append(FlairHvac(hvac))
    except Exception as e:
        _LOGGER.error("Failed to get hvac_units from Flair servers")
        raise PlatformNotReady from e

    async_add_entities(hvac_units)

class FlairHvac(SwitchEntity):
    """Representation of a Flair HVAC Unit as Switch."""

    def __init__(self, hvac):
        self._hvac = hvac
        self._available = True

    @property
    def unique_id(self):
        """Return the ID of this vent."""
        return self._hvac.hvac_id

    @property
    def name(self):
        """Return the name of the vent."""
        return "flair_hvac_" + self._hvac.hvac_name.lower()

    @property
    def icon(self):
        """Set vent icon"""
        return 'mdi:toggle-switch'

    @property
    def is_on(self):
        """Return true if vent is open."""
        return self._hvac.is_powered_on

    @property
    def available(self):
        """Return true if device is available."""
        return self._available

    @property
    def extra_state_attributes(self) -> dict:
        """Return optional state attributes."""
        return {
            ATTR_IS_ON: self.is_powered_on
        }

    def toggle(self, **kwargs):
        """Toggle the entity."""
        if self.is_powered_on:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self, **kwargs) -> None:
        """Open the vent."""
        self._hvac.turn_on()

    def turn_off(self, **kwargs) -> None:
        """Close the vent"""
        self._hvac.turn_off()

    def update(self):
        """Update automation state."""
        _LOGGER.info("Refreshing device state")
        self._hvac.refresh()
