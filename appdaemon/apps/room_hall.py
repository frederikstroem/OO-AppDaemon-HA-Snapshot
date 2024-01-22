import hassapi as hass

# /helper/rooms/
from helper.rooms.hall import Hall


class RoomHall(hass.Hass):
    def initialize(self):
        Hall(self)
