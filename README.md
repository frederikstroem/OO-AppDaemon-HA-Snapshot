# OO-AppDaemon-HA-Snapshot
Snapshot (2024-01-22) of core parts of my object-oriented AppDaemon Home Assistant setup.

My self-hosted setup, including this AppDaemon configuration, is constantly evolving, as I regularly experiment with new ideas. I aim to improve my codebases over time; however, I unfortunately lack the time to uphold projects like this to the standard I desire. Therefore, this AppDaemon configuration should not be viewed as a best practice or even a good example of proper AppDaemon usage. It is simply a reflection of my setup at a particular moment in time. Feel free to use it as you wish. 🙂

A core part of the light control is the use of ["virtual lights"](#virtual-lights), which are [Template Lights](https://www.home-assistant.io/integrations/light.template/), where AppDaemon listens to and controls the state of the light, which in turn controls all the real light entities.

To create cool Lovelace light cards, I use a combination of [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) and [Button Cards](https://github.com/custom-cards/button-card).

I use a variety of tools for deployment, development, and debugging, including automation of these processes. I have not included them in this repo, as some curation for public release would be needed, and I am not sure about the level of community interest.

If this piques the interest of the community, I will happily share more of my setup or provide some guidance. Don't hesitate to [open an issue](https://github.com/frederikstroem/OO-AppDaemon-HA-snapshot/issues/new) if you have any questions or comments.

## Virtual Lights
To create virtual lights, I use empty light templates, selecting the features I need for each room. These are added to the Home Assistant `configuration.yaml` file.

```yaml
light:
  - platform: template
    lights:
      roommate_light_virtual:
        friendly_name: "roommate.light.virtual"
        turn_on:

        turn_off:

        set_level:

        set_temperature:

        set_rgb:

      hall_light_virtual:
        friendly_name: "hall.light.virtual"
        turn_on:

        turn_off:

        set_level:

        set_temperature:

        set_rgb:

      lab_light_virtual:
        friendly_name: "lab.light.virtual"
        turn_on:

        turn_off:

        set_level:

        set_temperature:

        set_rgb:

      up_light_virtual:
        friendly_name: "up.light.virtual"
        turn_on:

        turn_off:

        set_level:

        set_temperature:

        set_rgb:
```
