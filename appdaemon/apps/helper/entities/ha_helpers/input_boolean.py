# /helper/entities/
from helper.entities.ha_helper import HAHelper

class InputBoolean(HAHelper):
    def __init__(self, api, ha_id: str, callback=None):
        super().__init__(api, ha_id, callback)

    def turn_on(self):
        """Turn on the input boolean."""
        self.api.turn_on(self.ha_id)

    def turn_off(self):
        """Turn off the input boolean."""
        self.api.turn_off(self.ha_id)
