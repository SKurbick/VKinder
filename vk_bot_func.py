from vk_api_func import ApiFunction

"""Работа с пользовательской частью бота, непосредственно с интерфейсом и механикой бота. 
В классе BotFunction прописаны функции обрабатывающие входные данные от пользователя"""


class BotFunction:
    def __init__(self, vk_user_id=None, city=None, sex=None, age_from=None, age_to=None):
        self.dataset = None
        self.datas = None
        self.city = city
        self.sex = sex
        self.age_from = age_from
        self.age_to = age_to
        self.favorite_list = []
        self.black_list = []
        self.vk_user_id = vk_user_id

    def user_search_data(self):
        """Обработка запроса на поиск профилей по соответсвующим критериям пользователя.
        Результат: 1. ИО профиля, ссылка на профиль,
        2. фотографии через запятую в формате: <photo><owner_id>_<id>(для удобного просмотра в интерфейсе пользователя)
        Перед этим переопределяет 'data' и 'dataset' для последующей обработки.
        Объект data является последним запрошенный пользователь
        Объект dataset весь запрошенный список """

        sex_key = {"мужской": 2, "женский": 1, "любой": 0}
        vk_search_user = ApiFunction(city=self.city, sex=sex_key[self.sex], age_from=self.age_from,
                                     age_to=self.age_to)
        self.datas = iter(vk_search_user.users_search())
        self.dataset = next(self.datas)
        vk_upload_photo = ApiFunction(users_id=f"{self.dataset['user_id']}")
        users_photo = vk_upload_photo.get_photos()
        photos = ''
        for photo in users_photo:
            photos += photo["attachment"] + ','
        user_name_and_link = f"{self.dataset['profile_name']}\n {self.dataset['link']}"
        return user_name_and_link, photos

    def next_profile(self):
        """Выводит следующего по списку dataset пользователя.
        Формат вывода равноценен 'user_search_data()'.
         Переопределяет пользователя в переменной data"""
        self.dataset = next(self.datas)

        vk_upload_photo = ApiFunction(users_id=f"{self.dataset['user_id']}")
        users_photo = vk_upload_photo.get_photos()
        photos = ''
        for photo in users_photo:
            photos += photo["attachment"] + ','
        user_name_and_link = f"{self.dataset['profile_name']}\n {self.dataset['link']}"
        return user_name_and_link, photos

    def add_to_favorites_lists(self):
        """Добавляет в 'список избранных' профиль из переменной data
        (Последний профиль, который был выведен для пользователя в интерфейсе).
        Корректно обрабатывает выходные данные если пользователь уже добавлял профиль в список"""

        if self.dataset not in self.favorite_list:
            self.favorite_list.append(self.dataset)
            text = f"Профиль '{self.dataset['profile_name']}' добавлен в избранное"
        else:
            text = f"Профиль '{self.dataset['profile_name']}' уже был в избранном"
        return text

    def show_favorites_list(self):
        """Выводит информацию о добавленных в 'избранный список' профилях
        Формат: <ИО><ссылка на профиль>"""
        count = 0
        text = ""
        if len(self.favorite_list)>0:
            for user in self.favorite_list:
                count += 1
                text += f"{count}: {user['profile_name']} ссылка: {user['link']}\n"
        else:
            text = "Список избранных пока пуст"
        return text

    def add_to_black_list(self):
        """добавляет последний профиль в 'черный список'
        в дальнейшем этот профиль будет отсортирован и не попадаться для пользователя в поиске профилей"""
        self.black_list.append(self.dataset)
        text = f"Профиль {self.dataset['profile_name']} больше не отобразится"
        return text
