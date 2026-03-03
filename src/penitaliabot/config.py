import os
from typing import Optional


class LazyEnvironmentVar:
    def __init__(self, var_name: str, default: Optional[str] = None):
        self.var_name = var_name
        self.default = default
        self.value = None

    def __get__(self, instance, owner) -> str:
        if self.value is None:
            self.value = os.environ.get(self.var_name, self.default)
            if self.value is None:
                raise RuntimeError(f"Environment variable {self.var_name} is not set")
        return self.value


class Config:
    http_url = LazyEnvironmentVar("PENITALIA_HTTP_URL")
    http_token = LazyEnvironmentVar("PENITALIA_HTTP_TOKEN")
    root_path = LazyEnvironmentVar("PENITALIA_ROOT_PATH", "/")
    tts_url = LazyEnvironmentVar("PENITALIA_TTS_URL", "http://localhost:8080/v1")
    tts_model = LazyEnvironmentVar("PENITALIA_TTS_MODEL", "tts-loquendo-roberto")
    tts_voice = LazyEnvironmentVar("PENITALIA_TTS_VOICE", "")
    tts_instructions = LazyEnvironmentVar("PENITALIA_TTS_INSTRUCTIONS", "")
    tts_speed = LazyEnvironmentVar("PENITALIA_TTS_SPEED", "1.0")
    tts_api_key = LazyEnvironmentVar("PENITALIA_TTS_API_KEY", "")
    redis_url = LazyEnvironmentVar("REDIS_URL", "")
    allowed_ids = LazyEnvironmentVar("PENITALIA_ALLOWED_IDS", "")
    telegram_token = LazyEnvironmentVar("PENITALIA_TOKEN")
