"""Озвучка текстовых сообщений."""
from telebot import TeleBot, types

from config import settings
from services import get_user_voice, set_user_voice, synthesize_speech
from services.voice_service import get_voice_names


def register_tts_handlers(bot: TeleBot) -> None:
    """Регистрирует обработчики текстов для озвучки."""

    @bot.message_handler(commands=["tts"])
    def handle_tts_command(message: types.Message) -> None:
        text = _extract_text(message.text)
        if not text:
            bot.reply_to(message, "Используйте: /tts ваш текст для озвучки")
            return
        _speak_and_send(bot, message, text)

    @bot.message_handler(func=lambda m: bool(m.text) and not m.text.startswith("/"))
    def handle_plain_text(message: types.Message) -> None:
        _speak_and_send(bot, message, message.text)


def _extract_text(text: str | None) -> str:
    if not text:
        return ""
    parts = text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ""


def _speak_and_send(bot: TeleBot, message: types.Message, text: str) -> None:
    default_voice = settings.voices[0]
    try:
        available = get_voice_names()
        if available:
            default_voice = available[0]
    except Exception:
        pass

    voice_name = get_user_voice(message.from_user.id, default_voice)
    try:
        audio_path = synthesize_speech(text=text, voice_name=voice_name)
    except Exception as exc:
        bot.reply_to(message, f"Не удалось создать озвучку: {exc}")
        return

    with audio_path.open("rb") as audio_file:
        bot.send_audio(
            chat_id=message.chat.id,
            audio=audio_file,
            caption=f"Озвучка голосом: {voice_name}\nФайл: {audio_path.name}",
        )
