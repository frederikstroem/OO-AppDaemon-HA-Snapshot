from enum import Enum

from globals import decimal_to_octet_proportional, decimal_to_custom_range_proportional
# /helper/entities/ha_helpers/
from helper.entities.ha_helpers.input_boolean import InputBooleanState

class VirtualLightState(Enum):
    ON = "on"
    OFF = "off"

class VirtualLight:
    def __init__(self, api, ha_id, light_entities, input_boolean_sleep_mode=None):
        # Set attributes.
        self.api = api
        self.ha_id = ha_id
        self.room = None # Set post room initialisation.
        self.light_entities = light_entities
        self.input_boolean_sleep_mode = input_boolean_sleep_mode # The sleep mode input boolean entity is optional on a per room basis.

        # Defaults.
        self.default_temp_kelvin = 3000

        # Last on values.
        self.last_on_brightness = None
        self.last_on_temp_kelvin = None
        self.last_on_rgb = None

        # Overwrite next on values.
        self.overwrite_next_on_brightness = None
        self.overwrite_next_on_temp_kelvin = None
        self.overwrite_next_on_rgb = None

        # Register callback.
        self.api.listen_state(self.callback, self.ha_id, attribute="all")

    ##############
    ## Getters. ##
    ##############
    def get_state(self):
        return VirtualLightState(self.api.get_state(self.ha_id))

    def get_brightness(self):
        return self.api.get_state(self.ha_id, attribute="brightness")

    def get_temp_kelvin(self):
        return self.api.get_state(self.ha_id, attribute="color_temp_kelvin")

    def get_default_temp_kelvin(self):
        return self.default_temp_kelvin

    def get_min_temp_kelvin(self):
        return self.api.get_state(self.ha_id, attribute="min_color_temp_kelvin")

    def get_max_temp_kelvin(self):
        return self.api.get_state(self.ha_id, attribute="max_color_temp_kelvin")

    def get_rgb(self):
        return self.api.get_state(self.ha_id, attribute="rgb_color")

    ##############
    ## Setters. ##
    ##############
    def set_overwrite_next_on_brightness(self, brightness):
        self.overwrite_next_on_brightness = brightness

    def set_overwrite_next_on_temp_kelvin(self, temp_kelvin):
        self.overwrite_next_on_temp_kelvin = temp_kelvin

    def set_overwrite_next_on_rgb(self, rgb):
        self.overwrite_next_on_rgb = rgb

    ###################################
    ## Standard turn on/off methods. ##
    ###################################
    def turn_on(self):
        self.api.turn_on(self.ha_id)

    def turn_on_with_brightness(self, brightness):
        self.api.turn_on(self.ha_id, brightness=brightness)

    def turn_on_with_brightness_and_temp_kelvin(self, brightness, temp_kelvin):
        self.api.turn_on(self.ha_id, brightness=brightness, color_temp_kelvin=temp_kelvin)

    def turn_on_with_brightness_and_rgb(self, brightness, rgb):
        self.api.turn_on(self.ha_id, brightness=brightness, rgb_color=rgb)

    def turn_off(self):
        self.api.turn_off(self.ha_id)

    def toggle(self):
        if self.get_state() == VirtualLightState.ON:
            self.turn_off()
        else:
            self.turn_on()

    ##############################
    ## Special turn on methods. ##
    ##############################
    def turn_on_with_max_illumination(self):
        self.turn_on_with_brightness_and_temp_kelvin(255, self.get_default_temp_kelvin())

    def turn_on_with_last_or_default_temp_kelvin(self):
        if self.last_on_temp_kelvin is not None:
            self.turn_on_with_brightness_and_temp_kelvin(self.last_on_brightness, self.last_on_temp_kelvin)
        elif self.last_on_brightness is not None:
            self.turn_on_with_brightness_and_temp_kelvin(self.last_on_brightness, self.default_temp_kelvin)
        else:
            self.turn_on_with_brightness_and_temp_kelvin(255, self.default_temp_kelvin)

    def turn_on_with_brightness_delta(self, brightness_delta):
        new_brightness = self.get_brightness() + brightness_delta
        if new_brightness < 0:
            new_brightness = 0
        elif new_brightness > 255:
            new_brightness = 255
        self.turn_on_with_brightness(new_brightness)

    def turn_on_with_brightness_delta_decimal(self, brightness_delta_decimal):
        self.turn_on_with_brightness_delta(decimal_to_octet_proportional(brightness_delta_decimal))

    def turn_on_with_temp_kelvin_delta(self, temp_kelvin_delta):
        # Get the current temperature of the virtual light.
        temp_kelvin = self.get_temp_kelvin()

        # If the current temperature is not available, use the last known temperature.
        # If that is also not available, use the default temperature.
        if temp_kelvin is None:
            temp_kelvin = self.last_on_temp_kelvin if self.last_on_temp_kelvin is not None else self.default_temp_kelvin

        # Calculate the new temperature by applying the delta.
        new_temp_kelvin = temp_kelvin + temp_kelvin_delta

        # Retrieve the minimum and maximum allowed temperatures for the light.
        min_temp_kelvin = self.get_min_temp_kelvin()
        max_temp_kelvin = self.get_max_temp_kelvin()

        # Clamp the new temperature to ensure it's within the allowed range.
        new_temp_kelvin = max(min(new_temp_kelvin, max_temp_kelvin), min_temp_kelvin)

        # Get the current brightness of the virtual light.
        current_brightness = self.get_brightness()

        # Turn on the virtual light with the new temperature and current brightness.
        self.turn_on_with_brightness_and_temp_kelvin(current_brightness, new_temp_kelvin)

    def turn_on_with_temp_kelvin_delta_decimal(self, temp_kelvin_delta_decimal):
        self.turn_on_with_temp_kelvin_delta(decimal_to_custom_range_proportional(temp_kelvin_delta_decimal, self.get_min_temp_kelvin(), self.get_max_temp_kelvin()))

    ######################
    ## Handler methods. ##
    ######################
    def handle_sleep_mode(self):
        if self.input_boolean_sleep_mode is not None: # If sleep mode is not set for the room, do nothing.
            # Get states.
            virtual_light_state = self.get_state()
            sleep_mode_state = self.input_boolean_sleep_mode.get_state()
            # Sleep mode brightness and RGB.
            sleep_mode_brightness = 1
            sleep_mode_rgb = [255, 0, 0]
            # Wake up brightness and temp kelvin.
            wake_up_brightness = decimal_to_octet_proportional(0.35)
            wake_up_temp_kelvin = self.default_temp_kelvin
            # Sleep mode logic.
            if virtual_light_state == VirtualLightState.ON:
                if sleep_mode_state == InputBooleanState.ON:
                    self.turn_on_with_brightness_and_rgb(sleep_mode_brightness, sleep_mode_rgb)
                else:
                    self.turn_on_with_brightness_and_temp_kelvin(wake_up_brightness, wake_up_temp_kelvin)
            elif virtual_light_state == VirtualLightState.OFF:
                if sleep_mode_state == InputBooleanState.ON:
                    self.overwrite_next_on_brightness = sleep_mode_brightness
                    self.overwrite_next_on_temp_kelvin = None
                    self.overwrite_next_on_rgb = sleep_mode_rgb
                else:
                    self.overwrite_next_on_brightness = wake_up_brightness
                    self.overwrite_next_on_temp_kelvin = wake_up_temp_kelvin
                    self.overwrite_next_on_rgb = None

    ######################
    ## Callback method. ##
    ######################
    def callback(self, entity, attribute, old, new, kwargs):
        if new != "":
            self.api.log(f"Virtual light event detected: {new}.", log=self.room.log)

            state = VirtualLightState(new["state"])
            if (
                state == VirtualLightState.ON and
                new["attributes"]["brightness"] is not None # If brightness is None, virtual light should not be considered on. Next elif will handle this.
            ):
                if (
                    self.overwrite_next_on_brightness is not None or
                    self.overwrite_next_on_temp_kelvin is not None or
                    self.overwrite_next_on_rgb is not None
                ):
                    self.api.log("Virtual light turned on with overwrites.", log=self.room.log)

                    # Create temporary variables.
                    overwrite_next_on_brightness = self.overwrite_next_on_brightness
                    overwrite_next_on_temp_kelvin = self.overwrite_next_on_temp_kelvin
                    overwrite_next_on_rgb = self.overwrite_next_on_rgb

                    # Clear overwrite next on values.
                    self.overwrite_next_on_brightness = None
                    self.overwrite_next_on_temp_kelvin = None
                    self.overwrite_next_on_rgb = None

                    if overwrite_next_on_brightness is not None and overwrite_next_on_temp_kelvin is not None:
                        self.turn_on_with_brightness_and_temp_kelvin(overwrite_next_on_brightness, overwrite_next_on_temp_kelvin)
                    elif overwrite_next_on_brightness is not None and overwrite_next_on_rgb is not None:
                        self.turn_on_with_brightness_and_rgb(overwrite_next_on_brightness, overwrite_next_on_rgb)
                    elif overwrite_next_on_brightness is not None:
                        self.turn_on_with_brightness(overwrite_next_on_brightness)
                    else:
                        # Something went wrong, just turn on.
                        self.turn_on()

                else:
                    self.api.log("Virtual light turned on.", log=self.room.log)

                    # Update last on values.
                    self.last_on_brightness = new["attributes"]["brightness"]
                    self.last_on_temp_kelvin = new["attributes"]["color_temp_kelvin"]
                    self.last_on_rgb = new["attributes"]["rgb_color"]

                    # Update light entities.
                    for light_entity in self.light_entities:
                        # Walk down though priority list of attributes.
                        if (   # If ignore_virtual_light flag is set, do nothing.
                            light_entity.has_flag("ignore_virtual_light")
                        ):
                            pass
                        elif ( # If sleep_light flag is not set and sleep mode is on, turn off the light entity.
                            light_entity.has_flag("sleep_light") is False and
                            self.input_boolean_sleep_mode is not None and # If sleep mode is not set for the room, do nothing.
                            self.input_boolean_sleep_mode.get_state() == InputBooleanState.ON
                        ):
                            light_entity.turn_off()
                        elif ( # Kelvin temperature takes precedence over RGB.
                            new["attributes"]["color_temp_kelvin"] is not None and
                            hasattr(light_entity, "turn_on_with_brightness_and_temp_kelvin")
                        ):
                            light_entity.turn_on_with_brightness_and_temp_kelvin(
                                new["attributes"]["brightness"],
                                new["attributes"]["color_temp_kelvin"]
                            )
                        elif ( # If no Kelvin temperature is available, use RGB.
                            new["attributes"]["rgb_color"] is not None and
                            hasattr(light_entity, "turn_on_with_brightness_and_rgb")
                        ):
                            light_entity.turn_on_with_brightness_and_rgb(
                                new["attributes"]["brightness"],
                                new["attributes"]["rgb_color"]
                            )
                        elif ( # If no RGB is available, use brightness.
                            hasattr(light_entity, "turn_on_with_brightness")
                        ):
                            light_entity.turn_on_with_brightness(new["attributes"]["brightness"])
                        elif ( # If no brightness is available, just turn on, but only at ~100% brightness and above 2900K.
                            new["attributes"]["brightness"] > 247 and
                            new["attributes"]["color_temp_kelvin"] is not None and
                            new["attributes"]["color_temp_kelvin"] > 2900
                        ):
                            light_entity.turn_on()
                        else:  # If no requirements are met, just turn off.
                            light_entity.turn_off()

            elif (
                state == VirtualLightState.ON and
                new["attributes"]["brightness"] is None
            ):
                self.api.log("Virtual light turned on, but brightness is None. Calling virtual light with half brightness and default temperature kelvin.", log=self.room.log)

                self.turn_on_with_brightness_and_temp_kelvin(decimal_to_octet_proportional(0.5), self.default_temp_kelvin)

            elif state == VirtualLightState.OFF:
                self.api.log("Virtual light turned off.", log=self.room.log)

                for light_entity in self.light_entities:
                    # Turn off all light entities, unless the ignore_virtual_light flag is set for the light entity.
                    if light_entity.has_flag("ignore_virtual_light") is False:
                        light_entity.turn_off()
