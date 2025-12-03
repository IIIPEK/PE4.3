"""Утилиты для загрузки и выдачи звуковых файлов."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Optional

from telebot import TeleBot
from telebot.types import Message

from config import settings

STORAGE_PATH = Path(settings.storage_dir)
STORAGE_PATH.mkdir(parents=True, exist_ok=True)


def _build_filename(message: Message, file_path: str | None) -> str:
    """Определяет имя файла для сохранения."""
    suffix = Path(file_path or "").suffix or ".ogg"
    if message.audio:
        base = Path(message.audio.file_name or f"audio_{uuid.uuid4().hex}")
        return f"{base.stem}{suffix}"
    return f"voice_{uuid.uuid4().hex}{suffix}"


def save_audio_file(bot: TeleBot, message: Message) -> Path:
    """
    Загружает файл из Telegram и сохраняет его в локальное хранилище.
    Возвращает путь до сохраненного файла.
    """
    file_id = message.audio.file_id if message.audio else message.voice.file_id  # type: ignore[union-attr]
    file_info = bot.get_file(file_id)
    file_bytes = bot.download_file(file_info.file_path)

    filename = _build_filename(message, file_info.file_path)
    destination = STORAGE_PATH / filename
    destination.write_bytes(file_bytes)
    return destination


def get_latest_audio(name: Optional[str] = None) -> Path:
    """
    Возвращает путь к файлу из хранилища:
    - если указано имя, то конкретный файл,
    - иначе последний измененный.
    """
    if name:
        candidate = STORAGE_PATH / name
        if not candidate.exists():
            raise FileNotFoundError(f"Файл {name} не найден в {STORAGE_PATH}")
        return candidate

    files = sorted(STORAGE_PATH.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise FileNotFoundError("Нет сохраненных аудиофайлов.")
    return files[0]


def list_audio_files() -> list[str]:
    """Список сохраненных аудиофайлов."""
    return sorted(p.name for p in STORAGE_PATH.glob("*") if p.is_file())
