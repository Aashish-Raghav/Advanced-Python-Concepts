# Metaclass for auto-registering subclasses in a registry


class RegistryMeta(type):
    registry = {}

    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)

        # Auto register classes (except for base class)
        if bases:
            mcls.registry[name.lower()] = cls
            print(f"Registered {name} in registry")

        return cls

    @classmethod
    def get_class(mcls, name):
        # Retrieve a class from the registry by name (case-insensitive)
        return mcls.registry.get(name.lower())


# Base class using RegistryMeta
class Plugin(metaclass=RegistryMeta):
    pass


# Subclass that will be auto-registered
class AudioPlugin(Plugin):
    def process_audio(self):
        return "processing audio"


# Subclass that will be auto-registered
class VideoPlugin(Plugin):
    def process_video(self):
        return "processing video"


# Show all registered classes
print(RegistryMeta.registry)

# Retrieve and use a registered class
audio_cls = RegistryMeta.get_class("AudioPlugin")
audio_instance = audio_cls()
print(audio_instance.process_audio())
