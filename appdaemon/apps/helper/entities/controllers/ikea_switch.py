from enum import Enum

from globals import (
    decimal_to_octet_proportional
)
# /helper/entities/
from helper.entities.controller import Controller


class IkeaSwitchActions(Enum):
    ON = "on"
    OFF = "off"
    BRIGHTNESS_MOVE_UP = "brightness_move_up"
    BRIGHTNESS_MOVE_DOWN = "brightness_move_down"

class IkeaSwitch(Controller):
    def __init__(self, api, ha_id, flags: set, action_map={}):
        default_action_map = {
            IkeaSwitchActions.ON: self.default_on,
            IkeaSwitchActions.OFF: self.default_off,
            IkeaSwitchActions.BRIGHTNESS_MOVE_DOWN: self.default_brightness_down,
            IkeaSwitchActions.BRIGHTNESS_MOVE_UP: self.default_brightness_up,
        }
        super().__init__(api, ha_id, flags, IkeaSwitchActions, action_map, default_action_map)

    def default_on(self, ha_id):
        self.room.virtual_light.turn_on()

    def default_off(self, ha_id):
        self.room.virtual_light.turn_off()

    def default_brightness_down(self, ha_id):
        self.room.virtual_light.turn_on_with_brightness_delta(decimal_to_octet_proportional(-0.25))

    def default_brightness_up(self, ha_id):
        self.room.virtual_light.turn_on_with_brightness_delta(decimal_to_octet_proportional(0.25))
