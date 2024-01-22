# /helper/entities/
from helper.entities.light import Light


class IkeaBulb(Light):
    def __init__(self, api, ha_id):
        super().__init__(api, ha_id)

    def turn_on_with_brightness(self, brightness):
        self.api.turn_on(self.ha_id, brightness=brightness)

    def turn_on_with_brightness_and_temp_kelvin(self, brightness, temp_kelvin):
        self.api.turn_on(self.ha_id, brightness=brightness, color_temp_kelvin=temp_kelvin)

    def turn_on_with_brightness_and_rgb(self, brightness, rgb):
        self.api.turn_on(self.ha_id, brightness=brightness, rgb_color=rgb)
