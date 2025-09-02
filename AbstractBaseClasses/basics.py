from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Abstract base class for all vehicles"""

    def __init__(self, make, model):
        self.make = make
        self.model = model

    @abstractmethod
    def start(self):
        """Start the vehicle"""
        pass

    @abstractmethod
    def stop(self):
        """Stop the vehicle"""
        pass

    @abstractmethod
    def get_max_speed(self):
        """Return maximum speed in km/h"""
        pass

    # Concrete method - provides default implementation
    def get_info(self):
        return f"{self.make} {self.model}"

    # Template method pattern
    def operate(self):
        """Template method using abstract methods"""
        self.start()
        print(f"Operating {self.get_info()} at max speed: {self.get_max_speed()} km/h")
        self.stop()


class Car(Vehicle):
    def __init__(self, make, model, fuel_type):
        super().__init__(make, model)
        self.fuel_type = fuel_type

    def start(self):
        print(f"Starting {self.fuel_type} engine")

    def stop(self):
        print("Applying brakes and stopping")

    def get_max_speed(self):
        return 200


class Bicycle(Vehicle):
    def __init__(self, make, model, gear_count):
        super().__init__(make, model)
        self.gear_count = gear_count

    def start(self):
        print("Starting to pedal")

    def stop(self):
        print("Applying brakes and stopping pedaling")

    def get_max_speed(self):
        return 50


# Usage
car = Car("Toyota", "Camry", "gasoline")
bike = Bicycle("Trek", "FX3", 21)

vehicles = [car, bike]
for vehicle in vehicles:
    vehicle.operate()
    print("---")

print(Vehicle.__abstractmethods__)  # Shows abstract methods that must be implemented by subclasses
print(Car.__abstractmethods__)      # Shows any remaining abstract methods in Car (should be empty if

# Output:
# Starting gasoline engine
# Operating Toyota Camry at max speed: 200 km/h
# Applying brakes and stopping
# ---
# Starting to pedal
# Operating Trek FX3 at max speed: 50 km/h
# Applying brakes and stopping pedaling
# ---
