from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand


START_COMMAND = Command("start")
FILMS_COMMAND = Command("films")
ADD_MOVIE_COMMAND = Command("add_movie")
SEARCH_MOVIE_COMMAND = Command("search_movie")
FILTER_MOVIES_COMMAND = Command("filter_movies")
EDIT_MOVIE_COMMAND = Command("edit_movie")
DELETE_MOVIE_COMMAND = Command("delete_movie")
RATE_MOVIE_COMMAND = Command("rate_movie")
RECOMMEND_MOVIE_COMMAND = Command("recommend_movie")

BOT_COMMANDS = [
    BotCommand(command="start", description="Почати розмову з ботом"),
    BotCommand(command="films", description="Перегляд списку фільмів"),
    BotCommand(command="add_movie", description="Додати новий фільм"),
    BotCommand(command="search_movie", description="Пошук фільму за назвою"),
    BotCommand(command="filter_movies", description="Фільтр фільмів за жанром або роком"),
    BotCommand(command="edit_movie", description="Редагування опису фільму"),
    BotCommand(command="delete_movie", description="Видалення фільму"),
    BotCommand(command="rate_movie", description="Оцінити фільм"),
    BotCommand(command="recommend_movie", description="Отримати рекомендацію кращого фільму"),
]
