# /helper/
from helper.entity import Entity


class Relay(Entity):
    def __init__(self, api, ha_id):
        super().__init__(api, ha_id)

    def turn_on(self):
        self.api.turn_on(self.ha_id)

    def turn_off(self):
        self.api.turn_off(self.ha_id)
