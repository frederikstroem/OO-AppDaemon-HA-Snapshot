# /helper/
from helper.virtual_light import VirtualLight

"""
    Room class
    Represents a room in the house.
    Attributes:
        api (API): The API object, hass.Hass object.
        id (str): The unique id of the room.
        entities (list): A list of entities (types) in the room.
        virtual_light (VirtualLight): The virtual light of the room.
"""
class Room:
    def __init__(self, api, id: str, entities, virtual_light: VirtualLight):
        self.api = api
        self.id = id
        self.entities = entities
        self.virtual_light = virtual_light

        # All rooms have their own log file. Note that these are defined in appdaemon.yaml.
        self.log = f"{self.id}_log"

    def get_entity_by_ha_id(self, ha_id):
        for entity in self.entities:
            if entity.ha_id == ha_id:
                return entity
        return None

    def get_room_id(self):
        return self.id
