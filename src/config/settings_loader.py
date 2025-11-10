import json
import os

def load_settings():
    path = os.path.join(os.path.dirname(__file__), "settings.example.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load settings: {e}")
        return {}