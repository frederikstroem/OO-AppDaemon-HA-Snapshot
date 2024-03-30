# /helper/
from helper.entity import Entity


class Light(Entity):
    KNOWN_FLAGS = Entity.KNOWN_FLAGS.union({
        "ignore_virtual_light", # Ignore virtual light.
        "sleep_light",          # When sleep mode is active, allow light to operate with virtual light, prioritizing to operate light with low brightness and red color.
    })

    def __init__(self, api, ha_id: str, flags: set):
        super().__init__(api, ha_id, flags)

    def turn_on(self):
        self.api.turn_on(self.ha_id)

    def turn_off(self):
        self.api.turn_off(self.ha_id)
