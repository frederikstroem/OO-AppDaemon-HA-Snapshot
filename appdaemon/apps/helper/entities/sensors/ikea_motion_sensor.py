from enum import Enum

# /helper/entities/
from helper.entities.sensor import DiscreteSensor


class IkeaMotionSensorStates(Enum):
    ON = "on"
    OFF = "off"

class IkeaMotionSensor(DiscreteSensor):
    def __init__(self, api, ha_id, event_map):
        super().__init__(api, ha_id, IkeaMotionSensorStates, event_map)
