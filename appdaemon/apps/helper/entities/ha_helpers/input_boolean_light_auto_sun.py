import datetime as dt

# /helper/
from helper.virtual_light import VirtualLightState
# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_boolean import InputBoolean


class InputBooleanLightAutoSun(InputBoolean):
    """Class to automate periods when the hallway light shouldn't auto turn on, on movement detection.

    Args:
        api: Instance of the Home Assistant API.
        ha_id: ID of the input boolean in Home Assistant.
    """
    def __init__(self, api, ha_id: str, flags: set):
        super().__init__(api, ha_id, flags, None)
        self.api.run_at_sunrise(self.callback_sunrise)
        self.api.run_at_sunset(self.callback_sunset, offset = dt.timedelta(minutes = -45).total_seconds())

    def callback_sunrise(self, kwargs):
        # At sunrise, turn off auto light boolean.
        self.turn_off()

        self.room.virtual_light.turn_off()
        self.room.virtual_light.set_overwrite_next_on_brightness(255)
        self.room.virtual_light.set_overwrite_next_on_temp_kelvin(self.room.virtual_light.get_default_temp_kelvin())

        self.api.log("Sunrise detected, turning off boolean.", log=self.room.log)

    def callback_sunset(self, kwargs):
        # 45 minutes before sunset, turn on auto light boolean.
        self.turn_on()

        if self.room.virtual_light.get_state() == VirtualLightState.OFF:
            self.room.virtual_light.turn_on_with_brightness_and_temp_kelvin(int(255 * 0.70), self.room.virtual_light.get_min_temp_kelvin())

        self.api.log("Sunset detected, turning on boolean.", log=self.room.log)
