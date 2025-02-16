from aiogram.types import Message
from asyncio import sleep
maxMessageLen = 4096

async def multyMessage(msg = Message, times = 0, word = 'хрю умолчательное ', sign = '+'):
    max_val = maxMessageLen/len(word)
    val = min(int(max_val), times)

    if sign == '+':
        await msg.answer(text=word*val)
    elif sign == '-':
        buffer = (word*val)[::-1].strip()
        print(buffer)
        print(buffer.strip())
        await msg.answer(text=buffer)
    
    if times > max_val:
        sleep(1)
        await msg.answer(text=f'и ещё {int(abs(times) - max_val)} {word}...')
