from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
from aiogram import Router, types, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, BaseFilter

import random
from asyncio import sleep

from tools import *
from data import *
from keyboards import inline_kb_tapgame
from config import ADMINS
random_router = Router()

@random_router.message()
async def sad_message(message: types.Message):
    a = random.randint(1, 100)
    if a <= 3:
        await message.answer('жаль')
    elif a == 5 and message.chat.id == BUTOVO:
        await message.answer_sticker(creep_tf)