import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    URLInputFile
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import BOT_TOKEN
from data import (
    get_films,
    add_film,
    update_film_rating,
    update_film_description,
    delete_film_by_name
)

# --------------------------------
# НАЛАШТУВАННЯ
# --------------------------------
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

class AddMovie(StatesGroup):
    """Додавання фільму"""
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()


class EditMovie(StatesGroup):
    """Редагування"""
    description = State()


class RateMovie(StatesGroup):
    """Оцінювання"""
    rating = State()


# =================================
# КЛАВІАТУРИ
# =================================

def main_menu():
    """Головне меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎬 Фільми"), KeyboardButton(text="➕ Додати")],
            [KeyboardButton(text="⭐ Рекомендація")]
        ],
        resize_keyboard=True
    )


def film_buttons(index: int):
    """Кнопки під фільмом"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Оцінити", callback_data=f"rate_{index}"),
                InlineKeyboardButton(text="✏️ Редагувати", callback_data=f"edit_{index}")
            ],
            [
                InlineKeyboardButton(text="🗑 Видалити", callback_data=f"delete_{index}")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back")
            ]
        ]
    )


# =================================
# START
# =================================

@dp.message(Command("start"))
async def start(message: Message):
    """Запуск бота"""
    await message.answer(
        "🎥 Привіт! Обери дію:",
        reply_markup=main_menu()
    )


# =================================
# СПИСОК ФІЛЬМІВ
# =================================

@dp.message(lambda m: m.text == "🎬 Фільми")
async def show_films(message: Message):
    """Показ списку фільмів"""
    films = get_films()["films"]

    if not films:
        await message.answer("📭 Фільмів поки немає")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f["name"], callback_data=f"film_{i}")]
            for i, f in enumerate(films)
        ]
    )

    await message.answer("🎬 Обери фільм:", reply_markup=keyboard)


# =================================
# КАРТКА ФІЛЬМУ
# =================================

@dp.callback_query(lambda c: c.data.startswith("film_"))
async def film_card(callback: CallbackQuery):
    """Деталі фільму"""
    films = get_films()["films"]
    index = int(callback.data.split("_")[1])
    film = films[index]

    text = (
        f"🎬 <b>{film['name']}</b>\n"
        f"⭐ Рейтинг: {film.get('rating', 'N/A')}\n"
        f"🎭 Жанр: {film.get('genre', '-')}\n"
        f"🎬 Актори: {', '.join(film.get('actors', []))}\n\n"
        f"{film.get('description', '')}"
    )

    try:
        await callback.message.answer_photo(
            photo=URLInputFile(film["poster"]),
            caption=text,
            reply_markup=film_buttons(index),
            parse_mode="HTML"
        )
    except Exception:
        await callback.message.answer(
            text + "\n\n⚠️ Постер недоступний",
            reply_markup=film_buttons(index),
            parse_mode="HTML"
        )

    await callback.answer()


# =================================
# ⭐ ОЦІНИТИ (КНОПКА)
# =================================

@dp.callback_query(lambda c: c.data.startswith("rate_"))
async def rate_start(callback: CallbackQuery, state: FSMContext):
    """Початок оцінювання"""
    index = int(callback.data.split("_")[1])
    film = get_films()["films"][index]

    await state.set_state(RateMovie.rating)
    await state.update_data(name=film["name"])

    await callback.message.answer(
        f"⭐ Введи рейтинг для «{film['name']}» (1–10):"
    )
    await callback.answer()


@dp.message(RateMovie.rating)
async def rate_save(message: Message, state: FSMContext):
    """Збереження рейтингу"""
    try:
        rating = int(message.text)
        data = await state.get_data()

        if 1 <= rating <= 10:
            update_film_rating(data["name"], rating)
            await message.answer("✅ Рейтинг збережено", reply_markup=main_menu())
        else:
            await message.answer("❌ Введи число від 1 до 10")

    except ValueError:
        await message.answer("❗ Введи число")

    await state.clear()


# =================================
# ✏️ РЕДАГУВАТИ
# =================================

@dp.callback_query(lambda c: c.data.startswith("edit_"))
async def edit_start(callback: CallbackQuery, state: FSMContext):
    """Початок редагування опису"""
    index = int(callback.data.split("_")[1])
    film = get_films()["films"][index]

    await state.set_state(EditMovie.description)
    await state.update_data(name=film["name"])

    await callback.message.answer(
        f"✏️ Введи новий опис для «{film['name']}»:"
    )
    await callback.answer()


@dp.message(EditMovie.description)
async def edit_save(message: Message, state: FSMContext):
    """Збереження опису"""
    data = await state.get_data()

    update_film_description(data["name"], message.text)
    await message.answer("✅ Опис оновлено", reply_markup=main_menu())

    await state.clear()


# =================================
# 🗑 ВИДАЛЕННЯ
# =================================

@dp.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_movie(callback: CallbackQuery):
    """Видалення фільму"""
    index = int(callback.data.split("_")[1])
    film = get_films()["films"][index]

    delete_film_by_name(film["name"])
    await callback.message.answer(
        f"🗑 Фільм «{film['name']}» видалено",
        reply_markup=main_menu()
    )
    await callback.answer()


# =================================
# 🔙 НАЗАД
# =================================

@dp.callback_query(lambda c: c.data == "back")
async def back(callback: CallbackQuery):
    """Повернення до списку"""
    await show_films(callback.message)
    await callback.answer()


# =================================
# ⭐ РЕКОМЕНДАЦІЯ
# =================================

@dp.message(lambda m: m.text == "⭐ Рекомендація")
async def recommend(message: Message):
    """Рекомендація найкращого фільму"""
    films = get_films()["films"]
    rated = [f for f in films if isinstance(f.get("rating"), (int, float))]

    if not rated:
        await message.answer("❌ Немає оцінених фільмів")
        return

    best = max(rated, key=lambda f: f["rating"])
    await message.answer(f"⭐ Рекомендуємо: {best['name']} ({best['rating']})")


# =================================
# ДОДАВАННЯ ФІЛЬМУ
# =================================

@dp.message(lambda m: m.text == "➕ Додати")
async def add_start(message: Message, state: FSMContext):
    """Початок додавання"""
    await state.set_state(AddMovie.name)
    await message.answer("Назва фільму:", reply_markup=ReplyKeyboardRemove())


@dp.message(AddMovie.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddMovie.description)
    await message.answer("Опис:")


@dp.message(AddMovie.description)
async def add_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddMovie.rating)
    await message.answer("Рейтинг (0–10):")


@dp.message(AddMovie.rating)
async def add_rating(message: Message, state: FSMContext):
    await state.update_data(rating=float(message.text))
    await state.set_state(AddMovie.genre)
    await message.answer("Жанр:")


@dp.message(AddMovie.genre)
async def add_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(AddMovie.actors)
    await message.answer("Актори через , ")


@dp.message(AddMovie.actors)
async def add_actors(message: Message, state: FSMContext):
    await state.update_data(actors=message.text.split(", "))
    await state.set_state(AddMovie.poster)
    await message.answer("Посилання на постер:")


@dp.message(AddMovie.poster)
async def add_poster(message: Message, state: FSMContext):
    data = await state.get_data()
    data["poster"] = message.text
    add_film(data)

    await message.answer("✅ Фільм додано", reply_markup=main_menu())
    await state.clear()


# =================================
# ЗАПУСК
# =================================

async def main():
    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
