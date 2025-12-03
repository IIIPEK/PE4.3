"""Точка входа Telegram-бота."""
from telebot import TeleBot

from config import settings
from handlers import register_audio_handlers, register_start_handlers, register_tts_handlers


def create_bot() -> TeleBot:

    return TeleBot(token=settings.token, parse_mode="HTML")


def register_handlers(bot: TeleBot) -> None:
    register_start_handlers(bot)
    register_audio_handlers(bot)
    register_tts_handlers(bot)


def main() -> None:
    bot = create_bot()
    register_handlers(bot)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
