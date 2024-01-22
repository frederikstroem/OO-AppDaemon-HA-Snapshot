# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_button import InputButton


class InputButtonLightMax(InputButton):
    def __init__(self, api, ha_id: str):
        super().__init__(api, ha_id, self.callback)

    def callback(self, entity, attribute, old, new, kwargs):
        if new != "" and new != old:
            try:
                self.api.log(f"Action detected for {entity}: {new}", log=self.room.log)
                self.room.virtual_light.turn_on_with_max_illumination()
            except ValueError:
                self.api.log(f"Unknown action: {new}", log="error_log")
