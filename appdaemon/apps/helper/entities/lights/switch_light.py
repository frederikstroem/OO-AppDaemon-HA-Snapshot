# /helper/entities/
from helper.entities.light import Light


class SwitchLight(Light):
    """Simple light entity that can be turned on and off."""

    def __init__(self, api, ha_id):
        super().__init__(api, ha_id)
