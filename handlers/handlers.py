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
from config import ADMINS
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f'тише')


class CatFilter(BaseFilter):
    def __init__(self): # Добавляем пустой __init__
        pass

    async def __call__(self, message: Message) -> bool: # Используйте __call__ вместо call
        if message.text :
            processed_text = await del_repetitions(message.text.upper())
            for char_ in ['0', 'O', '(О)', '<>', '()', '( )', '%', '°']:
                processed_text = processed_text.replace(char_, 'О')
            processed_text = processed_text.replace('K', 'К')
            processed_text = processed_text.replace('T', 'Т')
            return "КОТ" in (await del_repetitions(processed_text))
        return ""

@router.message(Command(commands='help')) 
async def cmd_start(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Заклинания.. некоторые"),
            "/hru <целое число> - что-то будет..."
        ),
        sep="\n",
    )
    await message.answer(**content.as_kwargs())


@router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Подтверждаем нажати
    if callback_query.data == 'back':
        await callback_query.message.delete()
    elif callback_query.data == 'forward':
        await callback_query.message.edit_text('нихуяешеньки тута()')
    elif callback_query.data == 'tapped':
        users_ID = callback_query.from_user.id
        fname = callback_query.from_user.first_name

        await start_count(users_ID, fname)
        await increment_taps(users_ID)


@router.message(F.text.upper().contains('УНИЧТОЖИТЬ'))
async def how_are_you(message: Message):
    if message.chat.id == BUTOVO:
        for i in range(1, 5 + 1 ):
            sleep(25)
            await message.answer('НЕХУЙ СПАТЬ')


@router.message((F.text.upper() == 'ЖОПА') & (F.chat.id == BUTOVO))
async def jops(message: Message):
    await message.answer_sticker(jopa)


#КООООООООООТ
@router.message(CatFilter())
async def caaaaat(message: Message):
    random_cat = random.choice(cats) 
    await message.answer_sticker(random_cat)
