import requests
from token_file import token_vk_app

"""Парсит входные данные по поиску профилей пользователя используя Api Vkontakte """


class ApiFunction:

    def __init__(self, users_id=None, access_token=token_vk_app, city=None, sex=None, age_from=None, age_to=None,
                 version='5.131',
                 count=999):
        self.token = access_token
        self.version = version
        self.sex = sex
        self.city = city
        self.age_from = age_from
        self.age_to = age_to
        self.count = count
        self.users_id = users_id
        self.params = {'access_token': self.token, 'v': self.version}

    def users_search(self):
        """Выводит список профилей по заданным критериям.
        Все профили открыты.
        Каждый профиль словарь в котором хранится:
        ИО пользователя, ссылка на профиль, ID профиля"""
        url = 'https://api.vk.com/method/users.search'
        params = {
            'count': self.count,
            'sex': self.sex,
            'age_from': self.age_from,
            'age_to': self.age_to,
            'has_photo': '1',
            'sort': '0',
            'hometown': self.city,
        }
        response = requests.get(url, params={**self.params, **params})
        users_info = []
        for i in response.json()['response']['items']:
            if i['can_access_closed'] is True:
                user_info = {
                    'profile_name': f"{i['first_name']} {i['last_name']}",
                    'link': f"https://vk.com/id{i['id']}",
                    'user_id': i["id"]
                }
                users_info.append(user_info)

        return users_info

    def get_photos(self):
        """
        Выдаёт 3 фотографии с профиля у которых большее количество 'лайков'.

        Сохраняет словарь с данными фотографий в виде:
        id фото, количество 'лайков', id владельца, и фото в формате для последующего чтения
         в интерфесе вконтекте.
         На выходе получаем три последние фотографии(словарь) отсортированного списка по ключу 'likes'
         (с большим количеством лайков)"""

        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.users_id,
            'access_token': self.token,
            'offset': 0,
            'count': 100,
            'photo_size': 0,
            'extended': 1,
            'v': 5.131,
            'album_id': 'profile', }

        response = requests.get(url, params=params)
        photos_info = []
        for i in response.json()['response']['items']:
            photo_info = {
                'id': i['id'],
                'likes': i['likes']['count'],
                'owner_id': i['owner_id'],
                'attachment': f'photo{i["owner_id"]}_{i["id"]}'
            }
            photos_info.append(photo_info)
        sorted_func = sorted(photos_info, key=lambda b: b['likes'])
        return sorted_func[-3:]
