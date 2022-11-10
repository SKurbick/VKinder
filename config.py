import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


start_keyboard = {
    "one_time": True,
    "buttons": [
        [get_button("ввести данные для поиска", "primary")]
    ]
}
second_keyboard = {
    "one_time": True,
    "buttons": [
        [get_button("следующий профиль", "positive")],
        [get_button("добавить в избранное", "positive"), get_button("список избранных", "positive")],
        [get_button("изменить поисковые данные", "primary"), get_button("help", "secondary")],
    ]
}
start_keyboard = json.dumps(start_keyboard, ensure_ascii=False).encode("utf-8")
start_keyboard = str(start_keyboard.decode("utf-8"))
how_search_message = """Введите данные в формате 'поиск город пол возраст от\до'
                    Пример ввода: 'Поиск Москва женский 18 25'
                    Для разделения используйте только пробел, в конце его использовать не нужно"""

second_keyboard = json.dumps(second_keyboard, ensure_ascii=False).encode("utf-8")
second_keyboard = str(second_keyboard.decode("utf-8"))
