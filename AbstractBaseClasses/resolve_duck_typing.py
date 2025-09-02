from abc import ABC, abstractmethod


class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass


class Swimmable(ABC):
    @abstractmethod
    def swim(self):
        pass


class Duck(Flyable, Swimmable):
    def fly(self):
        print("Duck Flying")

    def swim(self):
        print("Duck Swimming")


class Airplane(Flyable):
    def fly(self):
        print("Airplane Flying")


class Boat(Swimmable):
    def swim(self):
        print("Boat Swimming")


def make_flyable_objects_fly(flyable_obj: Flyable):
    flyable_obj.fly()


objects = [Airplane(), Duck(), Boat()]
try:
    for obj in objects:
        make_flyable_objects_fly(obj)
except Exception as e:
    print(f"Exception occured {e}")
