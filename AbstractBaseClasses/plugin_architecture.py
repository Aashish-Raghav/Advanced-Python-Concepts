from abc import ABC, abstractmethod

class Plugin(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def version(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    @abstractmethod
    def cleanup(self):
        pass

class AuthenticationPlugin(Plugin):
    @property
    def name(self):
        return "Authentication Plugin"
    
    @property
    def version(self):
        return "1.1.0"
    
    def initialize(self):
        print("Initializing Authentication System")
    
    def execute(self, username, password):
        return username == "admin" and password == "secret"
    
    def cleanup(self):
        print("Cleaning up authentication resources")
        
class LoggingPlugin(Plugin):
    @property
    def name(self):
        return "Logging Plugin"
    
    @property
    def version(self):
        return "1.1.0"
    
    def initialize(self):
        print("Started Logging System")
        self.logs = []
    
    def execute(self, message, level="INFO"):
        log_entry = f"[{level.upper()}] : {message}"
        self.logs.append(log_entry)
        print(log_entry)
        return log_entry  # Return the log entry for consistency
    
    def cleanup(self):
        print(f"Saved {len(self.logs)} log entries")
        

class PluginManager:

    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin: Plugin):
        """Register the Plugin"""

        if not isinstance(plugin, Plugin):
            raise TypeError("Plugin must inherit from Plugin Base")
        
        print(f"Registering {plugin.name} v{plugin.version}")
        plugin.initialize()
        self.plugins.append(plugin)

    def get_plugin(self, plugin_type):
        """Get plugin by type"""
        for plugin in self.plugins:
            if isinstance(plugin, plugin_type):
                return plugin
        return None


manager = PluginManager()
manager.register_plugin(AuthenticationPlugin())
manager.register_plugin(LoggingPlugin())

# Use plugins individually
auth_plugin = manager.get_plugin(AuthenticationPlugin)
log_plugin = manager.get_plugin(LoggingPlugin)

auth_result = auth_plugin.execute('admin', 'secret')
log_result = log_plugin.execute('User Logged In', 'DEBUG')

print("Authentication result:", auth_result)
print("Log result:", log_result)
