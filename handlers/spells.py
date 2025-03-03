from aiogram.filters import CommandStart, CommandObject, Command
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)
from aiogram import Router, types, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command, BaseFilter

import random
from asyncio import sleep

from db.ye_db import *
from tools import *
from data import *
from keyboards import inline_kb_tapgame
from config import ADMINS
spells_router = Router()

@spells_router.message(F.text.__eq__('-<>-'))
async def feel_energy(message: Message):
    await message.answer(text='энергия течёт...')
