"""Простое хранение выбранных голосов пользователей (in-memory)."""
from __future__ import annotations

from typing import Dict

_user_voice: Dict[int, str] = {}


def set_user_voice(user_id: int, voice_name: str) -> None:
    _user_voice[user_id] = voice_name


def get_user_voice(user_id: int, default: str) -> str:
    return _user_voice.get(user_id, default)
