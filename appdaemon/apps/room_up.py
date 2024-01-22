import hassapi as hass

# /helper/rooms/
from helper.rooms.up import Up


class RoomUp(hass.Hass):
    def initialize(self):
        Up(self)
