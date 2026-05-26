import configparser, os

class ConfigManager:
    _instance = None
    _config = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance
    def _load(self):
        self._config = configparser.ConfigParser()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base_dir, "config", "config.ini")
        if not os.path.exists(path):
            raise FileNotFoundError(f"config.ini not found: {path}")
        self._config.read(path)
    def get(self, key, section="settings"):
        return self._config.get(section, key)
    @property
    def web_url(self): return self.get("web_url")
    @property
    def browser(self): return self.get("browser")
    @property
    def excel_path(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, self.get("excel_path"))
    @property
    def headless(self): return self.get("headless").lower() == "true"
    @property
    def implicit_wait(self): return int(self.get("implicit_wait"))
    @property
    def explicit_wait(self): return int(self.get("explicit_wait"))
    @property
    def screenshot_dir(self):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, self.get("screenshot_dir"))
