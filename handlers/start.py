"""Обработчики команд /start и выбора голоса."""
from telebot import TeleBot, types

from config import settings
from keyboards import build_voice_keyboard
from services import set_user_voice
from services.voice_service import get_voice_names


def register_start_handlers(bot: TeleBot) -> None:
    """Регистрирует обработчики приветствия и выбора голоса."""

    @bot.message_handler(commands=["start"])
    def handle_start(message: types.Message) -> None:
        try:
            voices = get_voice_names()
        except Exception as exc:
            bot.reply_to(
                message,
                "Не удалось получить список голосов ElevenLabs. "
                f"Проверьте API ключ. Ошибка: {exc}",
            )
            return

        keyboard = build_voice_keyboard(tuple(voices), buttons_per_row=settings.keyboard_row_width)
        if voices:
            set_user_voice(message.from_user.id, voices[0])
        bot.send_message(
            message.chat.id,
            "Привет! Я бот для создания озвучки! "
            "Выберите голос, который будет использоваться при создании озвучки.",
            reply_markup=keyboard,
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("voice:"))
    def handle_voice_choice(call: types.CallbackQuery) -> None:
        voice = call.data.split("voice:", maxsplit=1)[-1] if call.data else "неизвестный"
        set_user_voice(call.from_user.id, voice)
        bot.answer_callback_query(call.id, text=f"Голос «{voice}» выбран")
        bot.send_message(call.message.chat.id, f"Вы выбрали голос: {voice}")

    @bot.message_handler(commands=["help"])
    def handle_help(message: types.Message) -> None:
        bot.send_message(
            message.chat.id,
            "Доступные команды:\n"
            "/start — выбор голоса из ElevenLabs\n"
            "/tts <code>текст</code> — озвучить текст выбранным голосом\n"
            "/files — список сохраненных файлов с кнопками\n"
            "/send <code>имя_файла</code> — отправить конкретный файл (или последний без аргумента)",
        )
