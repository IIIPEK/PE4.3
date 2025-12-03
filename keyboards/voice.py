"""Построение клавиатур, связанных с выбором голоса."""
from telebot import types


def build_voice_keyboard(voices: tuple[str, ...]) -> types.InlineKeyboardMarkup:
    """Создает inline-клавиатуру с вариантами голосов."""
    markup = types.InlineKeyboardMarkup()
    for voice in voices:
        markup.add(types.InlineKeyboardButton(text=voice, callback_data=f"voice:{voice}"))
    return markup
