from enum import Enum

# /helper/entities/
from helper.entities.sensor import DiscreteSensor


class PersonStates(Enum):
    HOME = "home"
    AWAY = "not_home"

class Person(DiscreteSensor):
    def __init__(self, api, ha_id: str, event_map):
        super().__init__(api, ha_id, PersonStates, event_map)
