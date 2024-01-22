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
from helper.entities.controllers.aqara_smart_home_cube import AqaraSmartHomeCube
# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_button_light_max import InputButtonLightMax
# /helper/entities/lights/
from helper.entities.lights.ikea_bulb import IkeaBulb
from helper.entities.lights.switch_light import SwitchLight
# /helper/entities/sensors/
from helper.entities.sensors.ikea_motion_sensor import IkeaMotionSensor, IkeaMotionSensorStates


class Up(Room):
    def __init__(self, api):

        ############# START #############
        ## Pre-initialization of room. ##
        #################################

        # Room id.
        id = "up"

        # Entities in the room.
        entities = [
            # Input buttons.
            InputButtonLightMax(
                api,
                f"input_button.{id}_light_max"
            ),
            # Sensors.
            IkeaMotionSensor(
                api,
                f"binary_sensor.{id}_ir_stairs_occupancy",
                {
                    IkeaMotionSensorStates.ON: self.event_IkeaMotionSensor_on,
                    IkeaMotionSensorStates.OFF: self.event_IkeaMotionSensor_off,
                },
            ),
            # Controllers.
            AqaraSmartHomeCube(
                api,
                f"sensor.{id}_controller_cube_action",
            ),
            # Lights.
            SwitchLight(
                api,
                f"switch.{id}_light_neon_cactus",
            ),
            IkeaBulb(
                api,
                f"light.{id}_light_north",
            ),
            IkeaBulb(
                api,
                f"light.{id}_light_south",
            ),
        ]

        # Virtual light, pass all light entities in the room.
        virtual_light = VirtualLight(
            api,
            "light.up_light_virtual",
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
        self.api.log(f"Upstairs initialized, a part of {HOME_NAME}.", log=HOME_LOG)

        ############### END ###############
        ## Post-initialization of room.  ##
        ###################################

    ################
    ## Callbacks. ##
    ################
    def event_IkeaMotionSensor_on(self, ha_id):
        self.api.log("Motion detected, turning on cactus.", log=self.log)
        self.get_entity_by_ha_id("switch.up_light_neon_cactus").turn_on()

    def event_IkeaMotionSensor_off(self, ha_id):
        self.api.log("No motion detected, turning off cactus.", log=self.log)
        self.get_entity_by_ha_id("switch.up_light_neon_cactus").turn_off()
