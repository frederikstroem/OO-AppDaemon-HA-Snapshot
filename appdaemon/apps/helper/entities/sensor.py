# /helper/
from helper.entity import Entity


class Sensor(Entity):
    def __init__(self, api, ha_id: str):
        super().__init__(api, ha_id)

class DiscreteSensor(Sensor):
    def __init__(self, api, ha_id: str, states_enum, event_map):
        super().__init__(api, ha_id)
        self.states_enum = states_enum
        self.event_map = event_map
        self.api.listen_state(self.callback, self.ha_id)

    def callback(self, entity, attribute, old, new, kwargs):
        if new != old and new != "":
            try:
                state = self.states_enum(new)
                if state in self.event_map:
                    self.api.log(f"State change detected for {self.ha_id}: {new}. Executing method from event map", log=self.room.log)
                    self.event_map[state](self.ha_id)
                elif state in self.states_enum:
                    self.api.log(f"State change detected for {self.ha_id}: {new}. State not implemented, no method executed.", log=self.room.log)
            except ValueError:
                self.api.log(f"Unknown state detected for {self.ha_id}: {new}.", log=self.room.log)

class ContinuousSensor(Sensor):
    def __init__(self, api, ha_id, event=None):
        super().__init__(api, ha_id)
        self.event = event
        if event is not None:
            self.api.listen_state(self.callback, self.ha_id)

    def callback(self, entity, attribute, old, new, kwargs):
        if new != old and new != "":
            # Assume that the value is numeric. Might need to be changed in the future.
            try:
                float_new = float(new)
                float_old = float(old)
                if self.event is not None:
                    # self.api.log(f"Value change detected for {self.ha_id}: {new}", log=self.room.log)
                    self.event(float_new, float_old)
            except ValueError:
                self.api.log(f"Invalid numeric value detected for {self.ha_id}: {new}.", log=self.room.log)
