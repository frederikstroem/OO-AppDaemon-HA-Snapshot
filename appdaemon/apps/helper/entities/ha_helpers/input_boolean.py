from enum import Enum

# /helper/entities/
from helper.entities.ha_helper import HAHelper

class InputBooleanState(Enum):
    ON = "on"
    OFF = "off"

class InputBoolean(HAHelper):
    def __init__(self, api, ha_id: str, flags: set, callback=None):
        super().__init__(api, ha_id, flags, callback)

    def get_state(self):
        return InputBooleanState(self.api.get_state(self.ha_id))

    def turn_on(self):
        """Turn on the input boolean."""
        self.api.turn_on(self.ha_id)

    def turn_off(self):
        """Turn off the input boolean."""
        self.api.turn_off(self.ha_id)

    def toggle(self):
        """Toggle the input boolean."""
        self.api.toggle(self.ha_id)
