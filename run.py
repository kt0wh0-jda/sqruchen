import logging
import asyncio
import aiosqlite

from random import randint, random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.methods.set_message_reaction import SetMessageReaction
from aiogram.filters import CommandStart, CommandObject, Command

from config import TOKEN, DB_NAME
from handlers.handlers import router
from generating import *
from db import create_table

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['hru', 'test']))
async def test(message: Message, command: CommandObject):

    txt = f'{message.from_user.full_name} с id: {message.from_user.id}'
    times = command.args
    prmtr = '+'

    if times == None:
        await message.answer(text='хрю + скока надо...')
        await bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id, reaction=[{"type": "emoji", "emoji": "👀"}])
    else:
        if times.isdigit() or (times[1:].isdigit() and times[0] in ['-', '+']):
            if times[0].isdigit() == False: 
                prmtr = times[0]
                times = times[1:]

            times = int(times)

            if int(times) % 2 == 1:
                if times > 100:
                    print(f'tried {times} times')
                    x = randint(1, 100)
                    if x == 1:
                        print(txt,'WINNER', sep='\n')
                        await multyMessage(msg=message, times=int(times), word='Хрю ', sign=prmtr)
                    else:
                        print(txt,'loser', sep='\n')
                        await message.answer(text='keep going')
                else:
                    await multyMessage(msg=message, times=int(times), word='Хрю ', sign=prmtr)
            else:
                await bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id, reaction=[{"type": "emoji", "emoji": "🤣"}])
        else:
            await message.reply(text='гмм... некорректное число хрюков')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу в базе данных, если она еще не существует
        await create_table()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')


