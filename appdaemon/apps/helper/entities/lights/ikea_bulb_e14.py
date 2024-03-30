# /helper/entities/
from helper.entities.light import Light
# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_boolean import InputBooleanState

# TODO: This class is maybe a little too hacky, consider refactoring.

class IkeaBulbE14(Light):
    def __init__(self, api, ha_id, flags: set):
        super().__init__(api, ha_id, flags)

    # def turn_on_with_brightness(self, brightness):
    #     self.api.turn_on(self.ha_id, brightness=brightness)

    # def turn_on_with_brightness_and_temp_kelvin(self, brightness, temp_kelvin):
    #     self.api.turn_on(self.ha_id, brightness=brightness, color_temp_kelvin=temp_kelvin)

    # def turn_on_with_brightness_and_rgb(self, brightness, rgb):
    #     self.api.turn_on(self.ha_id, brightness=brightness, rgb_color=rgb)

    def artifical_brightness_scale(self, brightness):
        # If night mode is active, pass the brightness as is.
        input_boolean_sleep_mode = self.room.get_input_boolean_sleep_mode()
        if input_boolean_sleep_mode is not None:
            if input_boolean_sleep_mode.get_state() == InputBooleanState.ON:
                return brightness

        if brightness >= 255:
            return 255
        elif brightness / 255 < 0.60:
            return 1
        else:
            return round(brightness * 0.75)

    def turn_on_with_brightness(self, brightness):
        self.api.turn_on(self.ha_id, brightness=self.artifical_brightness_scale(brightness))

    def turn_on_with_brightness_and_temp_kelvin(self, brightness, temp_kelvin):
        self.api.turn_on(self.ha_id, brightness=self.artifical_brightness_scale(brightness), color_temp_kelvin=temp_kelvin)

    def turn_on_with_brightness_and_rgb(self, brightness, rgb):
        self.api.turn_on(self.ha_id, brightness=self.artifical_brightness_scale(brightness), rgb_color=rgb)
