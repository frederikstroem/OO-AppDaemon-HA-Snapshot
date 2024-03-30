# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_boolean import InputBoolean


class InputBooleanSleepMode(InputBoolean):
    """Class to handle sleep mode input boolean, which is used to automate the sleep mode of a room, this is optional for each room.

    Args:
        api: Instance of the Home Assistant API.
        ha_id: ID of the input boolean in Home Assistant.
    """
    def __init__(self, api, ha_id: str, flags: set):
        super().__init__(api, ha_id, flags, self.callback)

    def callback(self, entity, attribute, old, new, kwargs):
        if new != "" and new != old:
            self.room.virtual_light.handle_sleep_mode()
