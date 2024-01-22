import hassapi as hass

# /helper/rooms/
from helper.rooms.roommate import Roommate


class RoomRoommate(hass.Hass):
    def initialize(self):
        Roommate(self)
