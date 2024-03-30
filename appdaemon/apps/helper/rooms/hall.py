from globals import (
    HOME_NAME,
    HOME_LOG,
)
# /helper/
from helper.room import Room
from helper.virtual_light import VirtualLight
# /helper/entities/
from helper.entities.light import Light
# /helper/entities/controllers/
from helper.entities.controllers.ikea_switch import IkeaSwitch
# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_boolean_light_auto_sun import InputBooleanLightAutoSun
from helper.entities.ha_helpers.input_button_light_max import InputButtonLightMax
# /helper/entities/lights/
from helper.entities.lights.ikea_bulb import IkeaBulb
# /helper/entities/sensors/
from helper.entities.sensors.ikea_motion_sensor import IkeaMotionSensor, IkeaMotionSensorStates


class Hall(Room):
    def __init__(self, api):

        ############# START #############
        ## Pre-initialization of room. ##
        #################################

        # Room id.
        id = "hall"

        # Entities in the room.
        entities = [
            # Input buttons.
            InputButtonLightMax(
                api,
                f"input_button.{id}_light_max",
                set(),
            ),
            # Input booleans.
            InputBooleanLightAutoSun(
                api,
                f"input_boolean.{id}_light_auto",
                set(),
            ),
            # Controllers.
            IkeaSwitch(
                api,
                f"sensor.{id}_controller_ikea_switch_action",
                set(),
            ),
            # Sensors.
            IkeaMotionSensor(
                api,
                f"binary_sensor.{id}_ir_by_rooms_occupancy",
                set(),
                {
                    IkeaMotionSensorStates.ON: self.event_IkeaMotionSensor_on,
                    IkeaMotionSensorStates.OFF: self.event_IkeaMotionSensor_off,
                },
            ),
            # Lights.
            IkeaBulb(
                api,
                f"light.{id}_light_ceiling",
                set(),
            ),
        ]

        # Virtual light, pass all light entities in the room.
        virtual_light = VirtualLight(
            api,
            f"light.{id}_light_virtual",
            [entity for entity in entities if isinstance(entity, Light)]
        )

        # Initialize room so that it can register itself with entities.
        super().__init__(api, id, entities, virtual_light)

        ############## END ##############
        ## Pre-initialization of room. ##
        #################################

        ############## START ##############
        ## Post-initialization of room.  ##
        ###################################

        # Register this room with the virtual light.
        self.virtual_light.room = self

        # Register this room with all entities in the room.
        for entity in self.entities:
            entity.room = self

        # Print room init log.
        self.api.log(f"Hallway initialized, a part of {HOME_NAME}.", log=HOME_LOG)

        ############### END ###############
        ## Post-initialization of room.  ##
        ###################################

    ################
    ## Callbacks. ##
    ################
    def event_IkeaMotionSensor_on(self, ha_id):
        self.api.log("Motion detected, turning on lights.", log=self.log)
        if self.get_entity_by_ha_id("input_boolean.hall_light_auto").get_state() == "on":
            self.virtual_light.turn_on()

    def event_IkeaMotionSensor_off(self, ha_id):
        self.api.log("No motion detected, turning off lights.", log=self.log)
        if self.get_entity_by_ha_id("input_boolean.hall_light_auto").get_state() == "on":
            self.virtual_light.turn_off()
