from globals import (
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


class Roommate(Room):
    def __init__(self, api):

        ############# START #############
        ## Pre-initialization of room. ##
        #################################

        # Room id.
        id = "roommate"

        entities = [
            # Input buttons.
            InputButtonLightMax(
                api,
                f"input_button.{id}_light_max",
            ),
            # Controllers.
            AqaraSmartHomeCube(
                api,
                f"sensor.{id}_controller_cube_action",
            ),
            # Lights.
            IkeaBulb(
                api,
                f"light.{id}_light_ceiling"
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
        self.api.log("Roommate's room initialized.", log=HOME_LOG)

        ############### END ###############
        ## Post-initialization of room.  ##
        ###################################
