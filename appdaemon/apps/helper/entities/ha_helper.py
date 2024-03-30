# /helper/
from helper.entity import Entity


class HAHelper(Entity):
    def __init__(self, api, ha_id: str, flags: set, event_handler=None):
        super().__init__(api, ha_id, flags)
        if event_handler is not None:
            self.api.listen_state(event_handler, self.ha_id)

    def get_state(self):
        return self.api.get_state(self.ha_id)
