from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

start_board = [[InlineKeyboardButton(text="Начать тест", callback_data="start_test")]]
sub_board = [[InlineKeyboardButton(text="Подписаться!", url="https://t.me/test_channel_hgt")]]
to_user_board = [[InlineKeyboardButton(text="Записаться на бесплатную консультацию!", url="https://t.me/HGT123t")]]
to_bot_board = [[InlineKeyboardButton(text="Пройти тест!", url="https://t.me/VoidDeveloperBot?start=s")]]

num_board = [
    [KeyboardButton(text=f"{i}", callback_data=f"{i}") for i in range(1, 6)],
    [KeyboardButton(text=f"{i}", callback_data=f"{i}") for i in range(6, 11)]
]

markup_nums = ReplyKeyboardMarkup(keyboard=num_board, resize_keyboard=True)
markup_start = InlineKeyboardMarkup(inline_keyboard=start_board)
markup_sub = InlineKeyboardMarkup(inline_keyboard=sub_board)
markup_to_user = InlineKeyboardMarkup(inline_keyboard=to_user_board)
markup_to_bot = InlineKeyboardMarkup(inline_keyboard=to_bot_board)
