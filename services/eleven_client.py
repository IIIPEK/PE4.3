"""Создает клиент ElevenLabs."""
from __future__ import annotations

from functools import lru_cache

from elevenlabs.client import ElevenLabs

from config import settings


@lru_cache(maxsize=1)
def get_client() -> ElevenLabs:
    if not settings.eleven_api_key:
        raise RuntimeError("Не задан ELEVENLABS_API_KEY/API_KEY для ElevenLabs")
    return ElevenLabs(api_key=settings.eleven_api_key)
