"""Базовые настройки бота."""
import os
from dataclasses import dataclass
from typing import Tuple

try:
    from dotenv import load_dotenv
except ImportError:  # пакет опционален, но рекомендуем установить
    load_dotenv = None

if load_dotenv:
    load_dotenv()


DEFAULT_VOICES: Tuple[str, ...] = (
    "Нейтральный",
    "Женский",
    "Мужской",
)


@dataclass(frozen=True)
class Settings:
    token: str
    voices: Tuple[str, ...]
    storage_dir: str
    eleven_api_key: str
    eleven_model: str


def load_settings() -> Settings:
    """Читает настройки из переменных окружения/значений по умолчанию."""
    voices = tuple(os.getenv("BOT_VOICES", "").split(",")) if os.getenv("BOT_VOICES") else DEFAULT_VOICES
    return Settings(
        token=os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN"),
        voices=voices,
        storage_dir=os.getenv("STORAGE_DIR", "storage"),
        eleven_api_key=os.getenv("ELEVENLABS_API_KEY") or os.getenv("API_KEY", ""),
        eleven_model=os.getenv("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
    )


settings = load_settings()
