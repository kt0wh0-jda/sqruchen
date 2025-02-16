from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_kb_tapgame = InlineKeyboardMarkup(inline_keyboard= [
    [InlineKeyboardButton(text='хочу назад(', callback_data='back'), InlineKeyboardButton(text='хочу вперёд', callback_data='forward')],
    [InlineKeyboardButton(text='ТАААААААП', callback_data='tapped')]
    ])
