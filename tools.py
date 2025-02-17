from aiogram.types import Message
from asyncio import sleep
maxMessageLen = 4096


async def multyMessage(msg = Message, times = 0, word = 'хрю умолчательное ', sign = '+') -> None:
    max_val = maxMessageLen/len(word)
    val = min(int(max_val), times)

    if sign == '+':
        await msg.answer(text=word*val)
    elif sign == '-':
        buffer = (word*val)[::-1].strip()
        await msg.answer(text=buffer)
    
    if times > max_val:
        sleep(1)
        await msg.answer(text=f'и ещё {int(abs(times) - max_val)} {word}...')


async def del_repetitions(text = str, l = None, r = None) -> str:
    if l == None: l = 0
    if r == None: r = len(text) - 1

    new_text = text[l]
    
    for i in text:
        if new_text[-1] != i:
            new_text += i
        else:
            pass

    return new_text
