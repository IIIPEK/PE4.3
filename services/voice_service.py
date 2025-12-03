"""Загрузка и предоставление списка голосов ElevenLabs."""
from __future__ import annotations

from typing import Dict, List

from services.eleven_client import get_client

_voice_map: Dict[str, str] = {}


def refresh_voices() -> List[str]:
    """Запрашивает голоса у ElevenLabs, обновляет кэш и возвращает имена."""
    client = get_client()
    voices_response = client.voices.get_all()
    _voice_map.clear()
    for voice in voices_response.voices:  # type: ignore[attr-defined]
        _voice_map[voice.name] = voice.voice_id
    return list(_voice_map.keys())


def get_voice_names() -> List[str]:
    """Возвращает список имен голосов (если пусто — загружает)."""
    if not _voice_map:
        refresh_voices()
    return list(_voice_map.keys())


def get_voice_id(name: str) -> str:
    """Возвращает voice_id по имени или поднимает ошибку."""
    if not _voice_map:
        refresh_voices()
    if name in _voice_map:
        return _voice_map[name]
    # fallback на первый доступный голос
    if _voice_map:
        return next(iter(_voice_map.values()))
    raise RuntimeError("Список голосов пуст. Проверьте API ключ ElevenLabs.")
