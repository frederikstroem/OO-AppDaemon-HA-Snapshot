import hassapi as hass

# /helper/rooms/
from helper.rooms.lab import Lab


class RoomLab(hass.Hass):
    def initialize(self):
        Lab(self)
