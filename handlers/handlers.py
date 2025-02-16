from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.filters import Command

from random import randint
from asyncio import sleep


from generating import *
from data import *
from keyboards import inline_kb_tapgame

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f'тише')


@router.message(Command(commands='help')) 
async def cmd_start(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Заклинания.. некоторые"),
            "/hru <целое число> - что-то будет...",
        ),
        sep="\n",
    )
    await message.answer(**content.as_kwargs())


@router.message(Command(prefix='!', commands=['multy', 'm']))
async def test(message: Message, command: CommandObject):
    times, phrase, separator = command.args.split(sep='_')
    if message.from_user.id in hruKings:
        await multyMessage(msg=message, times=int(times), word=phrase)


@router.message(F.text.upper().contains('ТАПАТЬ'))
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
        await callback_query.message.answer(text='cool')

@router.message(F.text.upper().contains('УНИЧТОЖИТЬ'))
async def how_are_you(message: Message):
    if message.chat.id == BUTOVO:
        for i in range(1, 5 + 1 ):
            sleep(25)
            await message.answer('НЕХУЙ СПАТЬ')


@router.message(F.text.upper().contains('ПАЛЬЧИК'))
async def yes_sir(message: Message):
    if message.chat.id == BUTOVO:
        if message.from_user.id == 893693230:
            await message.answer_sticker(finger)


@router.message(F.text.upper().contains('ЖОПА'))
async def yes_sir(message: Message):
    if message.chat.id == BUTOVO:
        await message.answer_sticker(jopa)


@router.message(F.text.upper().contains('КОТ'))
async def yes_sir(message: Message):
    cats = [tima, musya, leo, kooot]
    a = randint(0, 3)
    await message.answer_sticker(cats[a])


@router.message(F.text == 'мяу для скрюченого')
async def yes_sir(message: Message):
    if message.from_user.id == 893693230:
        await message.answer(text='где арахисы там и зима. мартамяу')


@router.message()
async def sad_message(message: types.Message):
    a = randint(1, 100)
    if a <= 4:
        await message.answer('жаль')
    elif a == 5 and message.chat.id == BUTOVO:
        await message.answer_sticker(creep_tf)


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
