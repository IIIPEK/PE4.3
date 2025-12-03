"""Обработчики загрузки и отправки аудио."""
from pathlib import Path

from telebot import TeleBot, types

from services import get_latest_audio, list_audio_files, save_audio_file


def register_audio_handlers(bot: TeleBot) -> None:
    """Регистрирует обработчики приема/отправки аудио."""

    @bot.message_handler(content_types=["audio", "voice"])
    def handle_audio(message: types.Message) -> None:
        saved_path = save_audio_file(bot, message)
        bot.reply_to(
            message,
            "Аудио сохранено.\n"
            f"Имя файла: {saved_path.name}\n"
            f"Отправить этот файл: /send {saved_path.name}",
        )

    @bot.message_handler(commands=["files"])
    def handle_files(message: types.Message) -> None:
        files = list_audio_files()
        if not files:
            bot.reply_to(message, "Хранилище пусто. Отправьте аудио или voice.")
            return
        bot.reply_to(message, "Доступные файлы:\n" + "\n".join(files))

    @bot.message_handler(commands=["send"])
    def handle_send(message: types.Message) -> None:
        requested_name = _parse_filename_argument(message.text)
        try:
            audio_path = get_latest_audio(requested_name)
        except FileNotFoundError as exc:
            bot.reply_to(message, str(exc))
            return

        with audio_path.open("rb") as audio_file:
            bot.send_audio(
                chat_id=message.chat.id,
                audio=audio_file,
                caption=f"Файл: {audio_path.name}",
            )


def _parse_filename_argument(text: str | None) -> str | None:
    if not text:
        return None
    parts = text.split(maxsplit=1)
    return parts[1].strip() if len(parts) > 1 else None
