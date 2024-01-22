# /helper/entities/
from helper.entities.ha_helper import HAHelper


class InputButton(HAHelper):
    def __init__(self, api, ha_id: str, event_handler=None):
        super().__init__(api, ha_id, event_handler)
