import os
import json
import data

TEST_FILE = "test_data.json"


def setup_function():
    """Створюємо порожній тестовий файл перед кожним тестом"""
    data.FILE_PATH = TEST_FILE
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        json.dump({"films": []}, f)


def teardown_function():
    """Видаляємо тестовий файл після кожного тесту"""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_get_films_empty():
    """Тест: якщо файл існує, але фільмів немає"""
    result = data.get_films()
    assert result == {"films": []}


def test_add_film():
    """Тест: додавання фільму"""
    film = {
        "name": "Interstellar",
        "description": "Sci-fi movie",
        "rating": 9
    }

    data.add_film(film)
    films = data.get_films()["films"]

    assert len(films) == 1
    assert films[0]["name"] == "Interstellar"


def test_update_film_rating():
    """Тест: оновлення рейтингу"""
    film = {"name": "Matrix", "description": "Sci-fi", "rating": 8}
    data.add_film(film)

    result = data.update_film_rating("Matrix", 10)
    films = data.get_films()["films"]

    assert result is True
    assert films[0]["rating"] == 10


def test_update_film_description():
    """Тест: оновлення опису"""
    film = {"name": "Avatar", "description": "Old", "rating": 7}
    data.add_film(film)

    result = data.update_film_description("Avatar", "New description")
    films = data.get_films()["films"]

    assert result is True
    assert films[0]["description"] == "New description"


def test_delete_film():
    """Тест: видалення фільму"""
    film = {"name": "Titanic", "description": "Drama", "rating": 8}
    data.add_film(film)

    result = data.delete_film_by_name("Titanic")
    films = data.get_films()["films"]

    assert result is True
    assert len(films) == 0
