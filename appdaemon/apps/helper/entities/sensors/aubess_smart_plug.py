# /helper/entities/
from helper.entities.sensor import ContinuousSensor


class AubessSmartPlug(ContinuousSensor):
    def __init__(self, api, ha_id: str, flags: set, event=None):
        super().__init__(api, ha_id, flags, event=event)
