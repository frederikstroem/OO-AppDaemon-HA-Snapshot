from enum import Enum

# /helper/entities/
from helper.entities.controller import Controller


class AqaraOppleSwitch3Actions(Enum):
    BUTTON_1_SINGLE = "button_1_single"
    BUTTON_1_DOUBLE = "button_1_double"
    BUTTON_1_TRIPLE = "button_1_triple"
    BUTTON_1_HOLD = "button_1_hold"
    BUTTON_1_RELEASE = "button_1_release"

    BUTTON_2_SINGLE = "button_2_single"
    BUTTON_2_DOUBLE = "button_2_double"
    BUTTON_2_TRIPLE = "button_2_triple"
    BUTTON_2_HOLD = "button_2_hold"
    BUTTON_2_RELEASE = "button_2_release"

    BUTTON_3_SINGLE = "button_3_single"
    BUTTON_3_DOUBLE = "button_3_double"
    BUTTON_3_TRIPLE = "button_3_triple"
    BUTTON_3_HOLD = "button_3_hold"
    BUTTON_3_RELEASE = "button_3_release"

    BUTTON_4_SINGLE = "button_4_single"
    BUTTON_4_DOUBLE = "button_4_double"
    BUTTON_4_TRIPLE = "button_4_triple"
    BUTTON_4_HOLD = "button_4_hold"
    BUTTON_4_RELEASE = "button_4_release"

    BUTTON_5_SINGLE = "button_5_single"
    BUTTON_5_DOUBLE = "button_5_double"
    BUTTON_5_TRIPLE = "button_5_triple"
    BUTTON_5_HOLD = "button_5_hold"
    BUTTON_5_RELEASE = "button_5_release"

    BUTTON_6_SINGLE = "button_6_single"
    BUTTON_6_DOUBLE = "button_6_double"
    BUTTON_6_TRIPLE = "button_6_triple"
    BUTTON_6_HOLD = "button_6_hold"
    BUTTON_6_RELEASE = "button_6_release"

class AqaraOppleSwitch3(Controller):
    def __init__(self, api, ha_id: str, flags: set, action_map={}):
        default_action_map = {
            AqaraOppleSwitch3Actions.BUTTON_1_SINGLE: self.default_button_1_single,
            AqaraOppleSwitch3Actions.BUTTON_2_SINGLE: self.default_button_2_single,
            AqaraOppleSwitch3Actions.BUTTON_3_SINGLE: self.default_button_3_single,
            AqaraOppleSwitch3Actions.BUTTON_4_SINGLE: self.default_button_4_single,
            AqaraOppleSwitch3Actions.BUTTON_6_SINGLE: self.default_button_6_single,
            AqaraOppleSwitch3Actions.BUTTON_6_DOUBLE: self.default_button_6_double,
        }
        super().__init__(api, ha_id, flags, AqaraOppleSwitch3Actions, action_map, default_action_map)

    def default_button_1_single(self, ha_id):
        """Decrease temperature."""

        self.room.virtual_light.turn_on_with_temp_kelvin_delta_decimal(-0.125)

    def default_button_2_single(self, ha_id):
        """Increase temperature."""

        self.room.virtual_light.turn_on_with_temp_kelvin_delta_decimal(0.125)

    def default_button_3_single(self, ha_id):
        """Decrease brightness."""

        self.room.virtual_light.turn_on_with_brightness_delta_decimal(-0.125)

    def default_button_4_single(self, ha_id):
        """Increase brightness."""

        self.room.virtual_light.turn_on_with_brightness_delta_decimal(0.125)

    def default_button_6_single(self, ha_id):
        """Toggle the virtual light."""

        self.room.virtual_light.toggle()

    def default_button_6_double(self, ha_id):
        """Toggle sleep mode."""

        input_boolean_sleep_mode = self.room.get_input_boolean_sleep_mode()
        if input_boolean_sleep_mode is not None:
            input_boolean_sleep_mode.toggle()
