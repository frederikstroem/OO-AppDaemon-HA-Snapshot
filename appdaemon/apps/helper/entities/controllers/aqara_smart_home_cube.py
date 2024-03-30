from enum import Enum

from globals import (
    angle_to_octet_proportional,
    angle_to_custom_range_proportional
)
# /helper/
from helper.virtual_light import VirtualLightState
# /helper/entities/
from helper.entities.controller import Controller


class AqaraSmartHomeCubeActions(Enum):
    ROTATE_LEFT = "rotate_left"
    ROTATE_RIGHT = "rotate_right"
    SLIDE = "slide"
    FLIP90 = "flip90"
    FLIP180 = "flip180"
    WAKEUP = "wakeup"

class AqaraSmartHomeModes(Enum):
    BRIGHTNESS = "brightness"
    TEMP_KELVIN = "temp_kelvin"

class AqaraSmartHomeCube(Controller):
    def __init__(self, api, ha_id: str, flags: set, action_map={}):
        default_action_map = {
            AqaraSmartHomeCubeActions.ROTATE_LEFT: self.default_rotate,
            AqaraSmartHomeCubeActions.ROTATE_RIGHT: self.default_rotate,
            AqaraSmartHomeCubeActions.SLIDE: self.default_slide,
            AqaraSmartHomeCubeActions.FLIP90: self.default_flip90,
            AqaraSmartHomeCubeActions.FLIP180: self.default_flip180,
            AqaraSmartHomeCubeActions.WAKEUP: self.default_wakeup,
        }
        super().__init__(api, ha_id, flags, AqaraSmartHomeCubeActions, action_map, default_action_map)
        self.default_mode = AqaraSmartHomeModes.BRIGHTNESS
        self.mode = self.default_mode
        self.mode_timeout_handle = None # Handle for the timeout callback
        self.mode_timeout_duration = 30 # Seconds

    def mode_timeout_reset(self):
        # Cancel the existing timeout if it exists
        if self.mode_timeout_handle and self.api.timer_running(self.mode_timeout_handle):
            self.api.cancel_timer(self.mode_timeout_handle)

        # Create a new timeout
        self.mode_timeout_handle = self.api.run_in(self.mode_timeout_callback, self.mode_timeout_duration)

    def mode_timeout_callback(self, kwargs):
        # Reset the mode to default when the timeout occurs
        self.mode = self.default_mode
        self.api.log(f"Resetting {self.ha_id} mode to {self.mode} due to inactivity.", log=self.room.log)

    def mode_next(self):
        # Get the current mode's index in the list of modes
        current_mode_index = list(AqaraSmartHomeModes).index(self.mode)
        # Calculate the next mode's index
        new_mode_index = (current_mode_index + 1) % len(AqaraSmartHomeModes)
        # Get the next mode using the index
        new_mode = list(AqaraSmartHomeModes)[new_mode_index]
        self.api.log(f"Setting {self.ha_id} mode to {new_mode}.", log=self.room.log)
        self.mode = new_mode

    def accelerate_angle(self, angle):
        # Take the absolute value of the action angle for symmetry.
        original_sign = 1 if angle >= 0 else -1
        abs_angle = abs(angle)

        # Apply the acceleration curve symmetrically.
        if abs_angle <= 90:
            # Scale the action angle by 0.75 for values below or equal to 90 degrees.
            return_value = abs_angle * 0.75
        else:
            # Apply an exponential acceleration curve for values above 90 degrees.
            return_value = 67.5 + (187.5 * ((abs_angle - 90) / 90) ** 2)

        # Restore the original sign of the action angle.
        return_value *= original_sign

        # Return the scaled or accelerated action angle.
        return return_value

    ######################
    ## Default actions. ##
    ######################
    def default_rotate(self, ha_id):
        self.mode_timeout_reset()
        if self.room.virtual_light.get_state() == VirtualLightState.ON:

            angle = self.api.get_state(self.ha_id, attribute="angle")
            accelerated_angle = self.accelerate_angle(angle)
            log_msg = f"Cube {self.ha_id} rotated {angle} degress (accelerated to {accelerated_angle} degrees)."
            if self.mode == AqaraSmartHomeModes.BRIGHTNESS:
                delta_brightness = angle_to_octet_proportional(accelerated_angle)
                self.api.log(f"{log_msg} Applying brightness delta of {delta_brightness}.", log=self.room.log)
                self.room.virtual_light.turn_on_with_brightness_delta(delta_brightness)
            elif self.mode == AqaraSmartHomeModes.TEMP_KELVIN:
                min_temp_kelvin = self.room.virtual_light.get_min_temp_kelvin()
                max_temp_kelvin = self.room.virtual_light.get_max_temp_kelvin()
                delta_temp_kelvin = angle_to_custom_range_proportional(accelerated_angle, min_temp_kelvin, max_temp_kelvin)
                self.api.log(f"{log_msg} Applying temp kelvin delta of {delta_temp_kelvin}, in range [{min_temp_kelvin}, {max_temp_kelvin}].", log=self.room.log)
                self.room.virtual_light.turn_on_with_temp_kelvin_delta(delta_temp_kelvin)

    def default_slide(self, ha_id):
        self.mode_timeout_reset()

    def default_flip90(self, ha_id):
        self.mode_timeout_reset()
        if self.room.virtual_light.get_state() == VirtualLightState.OFF:
            self.mode = self.default_mode
            self.room.virtual_light.turn_on()
        elif self.room.virtual_light.get_state() == VirtualLightState.ON:
            self.room.virtual_light.turn_off()

    def default_flip180(self, ha_id):
        self.mode_timeout_reset()
        self.mode_next()

    def default_wakeup(self, ha_id):
        pass
