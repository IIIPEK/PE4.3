"""Клавиатура с файлами для скачивания."""
from telebot import types


def build_files_keyboard(file_names: list[str], buttons_per_row: int = 2) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=max(1, buttons_per_row))
    buttons = [
        types.InlineKeyboardButton(text=name, callback_data=f"file:{name}")
        for name in file_names
    ]
    markup.add(*buttons)
    return markup
