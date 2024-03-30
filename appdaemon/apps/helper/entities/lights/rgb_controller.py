"""RGB light controller entity.

Zigbee2MQTT device: https://www.zigbee2mqtt.io/devices/TS0503B.html
"""

from globals import (
    decimal_to_octet_proportional
)
# /helper/entities/
from helper.entities.light import Light


class RGBController(Light):
    def __init__(self, api, ha_id, flags: set):
        super().__init__(api, ha_id, flags)

    def artifical_brightness_scale(self, brightness):
        if brightness > 100:
            return 255
        elif brightness <= 100:
            return decimal_to_octet_proportional(brightness / 100)

    def turn_on_with_brightness(self, brightness):
        self.api.turn_on(self.ha_id, brightness=self.artifical_brightness_scale(brightness))

    def turn_on_with_brightness_and_temp_kelvin(self, brightness, temp_kelvin):
        self.api.turn_on(self.ha_id, brightness=self.artifical_brightness_scale(brightness), color_temp_kelvin=temp_kelvin)

    def turn_on_with_brightness_and_rgb(self, brightness, rgb):
        self.api.turn_on(self.ha_id, brightness=self.artifical_brightness_scale(brightness), rgb_color=rgb)
