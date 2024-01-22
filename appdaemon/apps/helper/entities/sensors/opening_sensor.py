from enum import Enum

# /helper/entities/
from helper.entities.sensor import DiscreteSensor


class OpeningSensorStates(Enum):
    CLOSED = "off"
    OPEN = "on"

class OpeningSensor(DiscreteSensor):
    def __init__(self, api, ha_id, event_map):
        super().__init__(api, ha_id, OpeningSensorStates, event_map)
