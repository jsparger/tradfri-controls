from lewis.devices import Device
from lewis.adapters.stream import StreamInterface, Cmd, scanf, regex

from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory

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
    def __init__(self):
        self.color = 'Soft White'
        self.brightness = 1.0
        self.on = True;

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_brightness(self, brightness):
        self.brightness = brightness

    def get_brightness(self, brightness):
        return self.brightness

    def turn_on(self, on):
        self.on = on

    def is_on(self):
        return self.on

class TradfriBulbStreamInterface(StreamInterface):
    commands = {
    }



setups = {
    "default": {
        "device_type": TradfriBulb,
        "parameters": {},
    }
}
