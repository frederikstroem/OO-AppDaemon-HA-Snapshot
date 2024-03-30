from enum import Enum

# /helper/entities/
from helper.entities.controller import Controller


class IkeaButtonActions(Enum):
    ON = "on"
    BRIGHTNESS_MOVE_UP = "brightness_move_up"
    BRIGHTNESS_STOP = "brightness_stop"

class IkeaButton(Controller):
    KNOWN_FLAGS = Controller.KNOWN_FLAGS.union({
        "max_light_button"  # Button is a max light button.
    })

    def __init__(self, api, ha_id, flags: set, action_map={}):
        default_action_map = {
            IkeaButtonActions.ON: self.default_on,
        }
        super().__init__(api, ha_id, flags, IkeaButtonActions, action_map, default_action_map)

    def default_on(self, ha_id):
        if self.has_flag("max_light_button"):
            self.room.virtual_light.turn_on_with_max_illumination()
        else:
            self.room.virtual_light.toggle()
