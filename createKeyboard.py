
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from helper import langList, timestamp_to_date
from loguru import logger

def keyboard_select_day():
    kb = [
        [
            KeyboardButton(text="Сегодня"),
            KeyboardButton(text="Завтра"),
            
        ],
        [KeyboardButton(text="Послезавтра"),]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Или посмотрите все на определенный день",
        one_time_keyboard=True,
    )
    return keyboard




if __name__ == '__main__':
    pass