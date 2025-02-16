import aiosqlite
from config import DB_NAME
from aiogram.types import Message


async def create_table() -> None:
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу для хранения данных пользователей
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users_stats (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                taps_stat INTEGER
            )
        ''')
        await db.commit()  # Сохраняем изменения в базе данных

async def start_count(user_id: int, username: str) -> None:
    """Проверяет, есть ли пользователь в базе данных, и если нет, добавляет его.
       Не возвращает ничего.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id FROM users_stats WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result is None:
                # Пользователя нет в базе данных, добавляем его
                try:
                    await db.execute('''
                        INSERT INTO users_stats (user_id, username, taps_stat)
                        VALUES (?, ?, 0)  -- taps_stat по умолчанию 0
                    ''', (user_id, username))
                    await db.commit()
                    print(f"Пользователь с ID {user_id} успешно добавлен.")
                except aiosqlite.IntegrityError:
                    # Этот случай маловероятен, но все же обрабатываем
                    print(f"Ошибка при добавлении пользователя с ID {user_id} (возможно, ID уже существует).")
            else:
                print(f"Пользователь с ID {user_id} уже существует.")


async def set_name(user_id: int, new_name: str, msg: Message) -> None:
    """Изменяет имя пользователя в базе данных"""
    async with aiosqlite.connect(DB_NAME) as db:
        if new_name != None and len(new_name) <= 21:
            await db.execute('''
                UPDATE users_stats
                SET username = ?
                WHERE user_id = ?
            ''', (new_name, user_id))
            await db.commit()
            await msg.reply(text=f'Имя изменено на {new_name}')
        else:
            await msg.reply(text=f'не пойдёт')
        


async def increment_taps(user_id: int) -> None:
    """Увеличивает значение taps_stat на 1 для указанного пользователя."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            UPDATE users_stats
            SET taps_stat = taps_stat + 1
            WHERE user_id = ?
        ''', (user_id,))
        await db.commit()
        print(f"Taps_stat пользователя с ID {user_id} увеличен на 1.")


async def add_user(id: int, name: str, stat: int) -> None:
    """Добавляет нового пользователя в таблицу users_stats."""
    async with aiosqlite.connect(DB_NAME) as db:
        try:
            await db.execute('''
                INSERT INTO users_stats (user_id, username, taps_stat)
                VALUES (?, ?, ?)
            ''', (id, name, stat))
            await db.commit()
            print(f"Пользователь с ID {id} успешно добавлен.")  # Добавлено сообщение
        except aiosqlite.IntegrityError:
            print(f"Пользователь с ID {id} уже существует.") # Обработка ошибки дубликата


async def get_taps_stat(msg: Message) -> None:
    """Получает имя пользователя и значение taps_stat для указанного пользователя.

    Отправляет сообщение с именем пользователя и taps_stat, если пользователь найден.
    Отправляет сообщение, что пользователь не найден, если пользователь не найден.
    """
    user_id = msg.from_user.id
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT username, taps_stat FROM users_stats WHERE user_id = ?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            if result:
                username, taps = result  # Распаковываем результаты запроса
                await msg.answer(text=f'Ваши тапы, {username}: {taps}')
            else:
                await msg.answer(f"Пользователь с ID {user_id} не найден.")
            

async def get_all_data() -> list:
    """Возвращает все данные из таблицы users_stats."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users_stats") as cursor:
            data = await cursor.fetchall()
            return data


async def delete_user(user_id: int) -> None:
    """Удаляет пользователя из таблицы users_stats по его ID."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            DELETE FROM users_stats
            WHERE user_id = ?
        ''', (user_id,))
        await db.commit()
        print(f"Пользователь с ID {user_id} успешно удален.")  # Добавлено сообщение