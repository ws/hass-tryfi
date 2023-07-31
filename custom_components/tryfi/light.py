import logging
from datetime import datetime, timedelta

from homeassistant.components.light import LightEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import DOMAIN

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    tryfi = coordinator.data

    new_devices = []
    for pet in tryfi.pets:
        new_devices.append(TryFiPetLight(hass, pet, coordinator))
    if new_devices:
        async_add_devices(new_devices)


class TryFiPetLight(CoordinatorEntity, LightEntity):
    def __init__(self, hass, pet, coordinator):
        self._petId = pet.petId
        # self._tryfi = tryfi
        self._hass = hass
        # self._coordinator = coordinator
        super().__init__(coordinator)

    @property
    def name(self):
        return f"{self.pet.name} - Collar Light"

    @property
    def petId(self):
        return self._petId

    @property
    def pet(self):
        return self.coordinator.data.getPet(self.petId)

    @property
    def tryfi(self):
        return self.coordinator.data

    @property
    def unique_id(self):
        return f"{self.pet.petId}-light"

    @property
    def device_id(self):
        return self.unique_id

    @property
    def is_on(self):
        return bool(self.pet.device.ledOn)

    # @property
    # def hs_color(self):
    #    colorObj = color(self.pet.device.ledColor)
    #    return colorObj.hsl
    # @property
    # def supported_features(self):
    #    return SUPPORT_COLOR

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.pet.petId)},
            "name": self.pet.name,
            "manufacturer": "TryFi",
            "model": self.pet.breed,
            "sw_version": self.pet.device.buildId,
        }

    # Fix later, request update
    def turn_on(self, **kwargs):
        self.pet.turnOnOffLed(self.tryfi.session, True)
        # self.coordinator.async_request_refresh()

    def turn_off(self, **kwargs):
        self.pet.turnOnOffLed(self.tryfi.session, False)
        # self.coordinator.async_request_refresh()
