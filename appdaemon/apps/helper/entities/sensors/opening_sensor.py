from enum import Enum

# /helper/entities/
from helper.entities.sensor import DiscreteSensor


class OpeningSensorStates(Enum):
    CLOSED = "off"
    OPEN = "on"

class OpeningSensor(DiscreteSensor):
    def __init__(self, api, ha_id: str, flags: set, event_map):
        super().__init__(api, ha_id, flags, OpeningSensorStates, event_map)
