import json, os

class LocatorReader:
    _instance = None
    _cache = {}
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def _load_page(self, page_name):
        if page_name not in self._cache:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base, "locators", f"{page_name}.json")
            if not os.path.exists(path):
                raise FileNotFoundError(f"Locator file not found: {path}")
            with open(path, "r", encoding="utf-8") as f:
                self._cache[page_name] = json.load(f)
        return self._cache[page_name]
    def get_locator(self, page_name, key):
        data = self._load_page(page_name)
        if key not in data:
            raise KeyError(f"Locator key '{key}' not found in '{page_name}.json'")
        return data[key]
    def get_selector(self, page_name, key):
        loc = self.get_locator(page_name, key)
        t = loc["type"].lower()
        v = loc["value"]
        if t == "css": return v
        if t == "xpath": return f"xpath={v}"
        if t == "id": return f"#{v}"
        if t == "text": return f"text={v}"
        return v
