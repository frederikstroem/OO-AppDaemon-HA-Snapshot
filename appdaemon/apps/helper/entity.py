class Entity:
    def __init__(self, api, ha_id: str):
        self.api = api
        self.ha_id = ha_id
        self.room = None # Set post room initialisation.
