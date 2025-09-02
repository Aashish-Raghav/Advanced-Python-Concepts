from abc import ABC, abstractmethod


class ConfigurableDevice(ABC):
    def __init__(self, name):
        self._name = name

    @property
    @abstractmethod
    def device_type(self):
        """Device type must be defined by subclasses"""
        pass

    @property
    @abstractmethod
    def max_connections(self):
        """Maximum number of connections"""
        pass

    @max_connections.setter
    @abstractmethod
    def max_connections(self, value):
        """Setter for max_connections"""
        pass

    def get_info(self):
        return f"{self._name} ({self.device_type}): {self.max_connections} connections"


class Router(ConfigurableDevice):
    def __init__(self, name, model):
        super().__init__(name)
        self.model = model
        self._max_connections = 100

    @property
    def device_type(self):
        return "Network Router"

    @property
    def max_connections(self):
        return self._max_connections

    @max_connections.setter
    def max_connections(self, value):
        if value < 1 or value > 1000:
            raise ValueError("Connections must be between 1 and 1000")
        self._max_connections = value


class Switch(ConfigurableDevice):

    def __init__(self, name, port_count):
        super().__init__(name)
        self.port_count = port_count
        self._max_connections = port_count

    @property
    def device_type(self):
        return "Network Switch"

    @property
    def max_connections(self):
        return self._max_connections

    @max_connections.setter
    def max_connections(self, value):
        if value > self.port_count:
            raise ValueError(f"Cannot Exceed port count of {self.port_count}")
        self._max_connections = value


# Usage
router = Router("Office Router", "WRT3200ACM")
switch = Switch("Main Switch", 24)

devices = [router, switch]
for device in devices:
    print(device.get_info())

# Modify properties
router.max_connections = 150
print(f"Updated router: {router.get_info()}")

try:
    switch.max_connections = 30  # Will raise ValueError
except ValueError as e:
    print(f"Error: {e}")
