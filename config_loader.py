import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.yml"

class Config:
    def __init__(self):
        if not CONFIG_PATH.exists():
            raise FileNotFoundError("config.yml не найден")

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self.API_ID: int = data.get("API_ID", 0)
        self.API_HASH: str = data.get("API_HASH", "")
        self.SESSION_STRING: str = data.get("SESSION_STRING", "")
        self.OWNER_ID: int = data.get("OWNER_ID", 0)
        self.PREFIXES: list[str] = data.get("PREFIXES", [".", "!", "/", "$"])

    def validate(self):
        if not self.API_ID or not self.API_HASH:
            raise ValueError("API_ID и API_HASH должны быть заданы в config.yml")

    def save_session_string(self, session_string: str):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        data["SESSION_STRING"] = session_string

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True)

config = Config()

