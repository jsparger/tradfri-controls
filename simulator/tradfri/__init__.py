
from lewis.devices import Device
from lewis.adapters.stream import StreamInterface, Cmd, scanf, regex

from .pytradfri import Gateway
from .pytradfri.api.libcoap_api import APIFactory

import pickle

# import logging
# logging.disable(logging.CRITICAL)

class Light(object):
    def __init__(self, host, identity, key):
        api_factory = APIFactory(host=host, psk_id=identity, psk=key)
        self._api = api_factory.request
        gateway = Gateway()
        devices = self._api(self._api(gateway.get_devices()))
        self.light = [d for d in devices if d.has_light_control][0]
        self.control = self.light.light_control

    def set_state(self, state):
        self._api(self.control.set_state(state))
        self._api(self.light.update())
    def set_color(self, color):

        self._api(self.control.set_predefined_color(color))
        self._api(self.light.update())
    def set_brightness(self, fraction):

        dimmer = int(fraction * 254)
        self._api(self.control.set_dimmer(dimmer))
        self._api(self.light.update())

class TradfriBulb(Device):
    def __init__(self, physical=None):
        self.color = 'Soft White'
        self.brightness = 1.0
        self.on = True;
        self.physical = physical

    def set_color(self, color):
        color = color.decode("utf-8")
        self.color = color
        if self.physical:
            self.physical.set_color(color)


    def get_color(self):
        return self.color

    def set_brightness(self, brightness):
        self.brightness = brightness
        if self.physical:
            self.physical.set_brightness(brightness)

    def get_brightness(self, brightness):
        return self.brightness

    def set_state(self, state):
        self.on = state
        if self.physical:
            self.physical.set_state(state)

    def get_state(self):
        return self.on

class TradfriBulbStreamInterface(StreamInterface):
    commands = {
        Cmd('set_state', scanf('state=%d')),
        Cmd('set_color', scanf('color=%s'), argument_mappings=(bytes,)),
        Cmd('set_brightness', scanf('brightness=%f')),
    }

    in_terminator = '\r\n'
    out_terminator = '\r\n'

secret = pickle.load(open("secret.p", "rb"))
setups = {
    "default": {
        "device_type": TradfriBulb,
        "parameters": {
            "physical": Light(**secret)
        },
    }
}
