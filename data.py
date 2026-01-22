import json

FILE_PATH = "data.json"
#Додати фільм
def get_films():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"films": []}
    return data
#Зберегти фільм
def save_films(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
#Додати фільм
def add_film(film: dict):
    data = get_films()
    data.setdefault("films", []).append(film)
    save_films(data)
#Видалити фільм
def delete_film_by_name(name: str) -> bool:
    data = get_films()
    for film in data["films"]:
        if film["name"].lower() == name.lower():
            data["films"].remove(film)
            save_films(data)
            return True
    return False
#Обновити опис фільму
def update_film_description(name: str, description: str) -> bool:
    data = get_films()
    for film in data["films"]:
        if film["name"].lower() == name.lower():
            film["description"] = description
            save_films(data)
            return True
    return False
#обновити рейтинг фільму
def update_film_rating(name: str, rating: int) -> bool:
    data = get_films()
    for film in data["films"]:
        if film["name"].lower() == name.lower():
            film["rating"] = rating
            save_films(data)
            return True
    return False

