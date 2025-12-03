"""Озвучка текста через ElevenLabs."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from config import settings
from services.eleven_client import get_client
from services.file_service import STORAGE_PATH
from services.voice_service import get_voice_id


def _slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_") or "voice"


def synthesize_speech(text: str, voice_name: str) -> Path:
    """Генерирует речь из текста и сохраняет файл в хранилище."""
    if not settings.eleven_api_key:
        raise RuntimeError("Не задан ELEVENLABS_API_KEY/API_KEY.")

    client = get_client()
    voice_id = get_voice_id(voice_name)
    audio_stream = client.text_to_speech.convert(  # type: ignore[attr-defined]
        text=text,
        voice_id=voice_id,
        model_id=settings.eleven_model,
        output_format="mp3_44100_128",
    )
    filename = f"tts_{_slug(voice_name)}_{uuid.uuid4().hex}.mp3"
    destination = STORAGE_PATH / filename
    with destination.open("wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    return destination
