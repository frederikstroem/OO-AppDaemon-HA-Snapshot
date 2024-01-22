from globals import (
    HOME_LOG,
)
# /helper/
from helper.room import Room
from helper.virtual_light import VirtualLight
# /helper/entities/
from helper.entities.light import Light
from helper.entities.relay import Relay
# /helper/entities/controllers/
from helper.entities.controllers.aqara_opple_switch_3 import AqaraOppleSwitch3
from helper.entities.controllers.aqara_smart_home_cube import AqaraSmartHomeCube
from helper.entities.controllers.ikea_remote import IkeaRemote
# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_button_light_max import InputButtonLightMax
# /helper/entities/lights/
from helper.entities.lights.ikea_bulb import IkeaBulb
from helper.entities.lights.switch_light import SwitchLight
from helper.entities.lights.rgb_controller import RGBController
# /helper/entities/sensors/
from helper.entities.sensors.aubess_smart_plug import AubessSmartPlug
from helper.entities.sensors.person import Person, PersonStates


class Lab(Room):
    def __init__(self, api):

        ############# START #############
        ## Pre-initialization of room. ##
        #################################

        # Room id.
        id = "lab"

        # Entities in the room.
        entities = [
            # Input buttons.
            InputButtonLightMax(
                api,
                f"input_button.{id}_light_max",
            ),
            # Sensors.
            Person(
                api,
                "person.frederik_holm_strom",
                {
                    PersonStates.AWAY: self.callback_person_away,
                }
            ),
            AubessSmartPlug(
                api,
                f"sensor.{id}_relay_desktop_power",
                self.callback_desktop_power_change,
            ),
            # Controllers.
            AqaraOppleSwitch3(
                api,
                f"sensor.{id}_controller_desk_action",
            ),
            AqaraSmartHomeCube(
                api,
                f"sensor.{id}_controller_cube_action",
            ),
            IkeaRemote(
                api,
                f"sensor.{id}_controller_by_door_action",
            ),
            # Lights.
            IkeaBulb(
                api,
                f"light.{id}_light_ceiling",
            ),
            IkeaBulb(
                api,
                f"light.{id}_light_by_mirror",
            ),
            RGBController(
                api,
                f"light.{id}_light_ceiling_bar",
            ),
            SwitchLight(
                api,
                f"switch.{id}_light_bed_lamp",
            ),
            # Relays.
            Relay(
                api,
                f"switch.{id}_relay_speakers",
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
        self.api.log("Lab initialized.", log=HOME_LOG)

        ############### END ###############
        ## Post-initialization of room.  ##
        ###################################

    ################
    ## Callbacks. ##
    ################
    def callback_person_away(self, ha_id):
        self.api.log("Strøm left House, turning off the lights in lab.", log=self.log)
        self.virtual_light.turn_off()

    def callback_desktop_power_change(self, new_value, old_value):
        # self.api.log(f"Desktop power changed to {new_value}W.", log=self.log)
        speaker_relay = self.get_entity_by_ha_id("switch.lab_relay_speakers")
        if new_value > 18 and old_value <= 18:
            self.api.log(f"Desktop power changed to {new_value}W, was {old_value}W, turning on speakers.", log=self.log)
            speaker_relay.turn_on()
        elif new_value <= 18 and old_value > 18:
            self.api.log(f"Desktop power changed to {new_value}W, was {old_value}W, turning off speakers.", log=self.log)
            speaker_relay.turn_off()
