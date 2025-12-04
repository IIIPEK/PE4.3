"""Построение клавиатур, связанных с выбором голоса."""
from telebot import types


def build_voice_keyboard(voices: tuple[str, ...], buttons_per_row: int = 2) -> types.InlineKeyboardMarkup:
    """Создает inline-клавиатуру с вариантами голосов."""
    markup = types.InlineKeyboardMarkup(row_width=max(1, buttons_per_row))
    buttons = [types.InlineKeyboardButton(text=voice, callback_data=f"voice:{voice}") for voice in voices]
    markup.add(*buttons)
    return markup
