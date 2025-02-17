from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
from aiogram import Router, types, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, BaseFilter

import random
from asyncio import sleep

from db.taps_db import *
from tools import *
from data import *
from keyboards import inline_kb_tapgame
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
            "/hru <целое число> - что-то будет...",
            "/all_stat - покажу закрома",
            "/set_name <имя> - изменю ваше имя"
        ),
        sep="\n",
    )
    await message.answer(**content.as_kwargs())


@router.message(Command(commands='add_user'))
async def add_user_to_db(message: Message):
    await add_user(999, 'тестовый', 999)
    await message.answer(text='Юзер добавлен фуух')
    

@router.message(Command(commands='my_stat'))
async def get_my_stat(message: Message):
    await get_taps_stat(message)


@router.message(Command(commands='all_stat'))
async def show_data(message: Message):
    """Обработчик команды /show_db. Отправляет данные из базы данных в чат."""
    data = await get_all_data()  # Получаем данные из базы данных
    sorted_data = sorted(data, key=lambda x: x[2],reverse=True)
    if data:
        txt = 'Статистика:\n\n'
        for user_id, username, taps_stat in sorted_data:
            txt += f"{username} - {taps_stat}\n"
        await message.answer(text=txt)
    else:
        await message.answer(text='База данных пуста.')


@router.message(Command(commands='delete_user'))
async def del_user(message: Message, command: CommandObject):
    if message.from_user.id in ADMINS:
        user_id= command.args
    try:
        await delete_user(user_id)
    except:
        await print('что-то не так')


@router.message(Command(commands='del_reps'))
async def del_reps(message: Message, command: CommandObject):
    try:
        await message.answer(f'{await del_repetitions(text=command.args)}')
    except:
        await message.answer('что-то не так')


@router.message(Command(commands='set_name'))
async def set_new_name(message: Message, command: CommandObject):

    arg = command.args
    users_ID = message.from_user.id

    await set_name(users_ID, arg, message)


@router.message(Command(prefix='!', commands=['multy', 'm']))
async def test(message: Message, command: CommandObject):
    times, phrase, separator = command.args.split(sep='_')
    if message.from_user.id in hruKings:
        await multyMessage(msg=message, times=int(times), word=phrase)


@router.message(F.text.upper().in_(tapping_filter))
async def tap_game(message:Message):
    await message.answer(text='нукась', reply_markup=inline_kb_tapgame)


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


@router.message(F.text.upper().contains('ПАЛЬЧИК'))
async def palchik(message: Message):
    if message.chat.id == BUTOVO:
        if message.from_user.id in ADMINS:
            await message.answer_sticker(finger)


@router.message((F.text.upper() == 'ЖОПА') & (F.chat.id == BUTOVO))
async def jops(message: Message):
    await message.answer_sticker(jopa)


#КООООООООООТ
@router.message(CatFilter())
async def caaaaat(message: Message):
    random_cat = random.choice(cats) 
    await message.answer_sticker(random_cat)





# @router.message()
# async def anti_max(message: Message):
#     number = randint(1, 10)
#     if message.from_user.id == 906710511 and number < 4:
#         await message.reply(text='иди дрыхни убежище солнце уже встало')
#     elif message.from_user.id == 906710511 and number == 7:
#          await message.answer_sticker(creep_tf)
#     elif message.from_user.id == 906710511 and number in [4, 5, 6]:
#         await message.reply(text=arr[randint(0, 3)])


        
# @router.message()
# async def sanya_trolling(message: Message):
#     number = randint(1, 10)
#     if message.from_user.id == 2101837141 and number < 3:
#         await message.reply(text='keep calm')
