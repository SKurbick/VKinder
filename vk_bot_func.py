from vk_api_func import ApiFunction


class BotFunction:
    def __init__(self, vk_user_id, city, sex, age_from, age_to):
        self.data = None
        self.datas = None
        self.city = city
        self.sex = sex
        self.age_from = age_from
        self.age_to = age_to
        self.favorite_list = []
        self.black_list = []
        self.vk_user_id = vk_user_id

    def user_search_data(self):
        sex_key = {"мужской": 2, "женский": 1, "любой": 0}
        vk_search_user = ApiFunction(city=self.city, sex=sex_key[self.sex], age_from=self.age_from,
                                     age_to=self.age_to)
        self.datas = iter(vk_search_user.users_search())
        self.data = next(self.datas)
        vk_upload_photo = ApiFunction(users_id=f"{self.data['user_id']}")
        users_photo = vk_upload_photo.get_photos()
        photos = ''
        for photo in users_photo:
            photos += photo["attachment"] + ','
        user_name_and_link = f"{self.data['profile_name']}\n {self.data['link']}"
        return user_name_and_link, photos

    def next_profile(self):
        self.data = next(self.datas)

        vk_upload_photo = ApiFunction(users_id=f"{self.data['user_id']}")
        users_photo = vk_upload_photo.get_photos()
        photos = ''
        for photo in users_photo:
            photos += photo["attachment"] + ','
        user_name_and_link = f"{self.data['profile_name']}\n {self.data['link']}"
        return user_name_and_link, photos

    def add_to_favorites_lists(self):
        if self.data not in self.favorite_list:
            self.favorite_list.append(self.data)
            text = f"Профиль '{self.data['profile_name']}' добавлен в избранное"
        else:
            text = f"Профиль '{self.data['profile_name']}' уже был в избранном",
        return text

    def show_favorites_list(self):
        count = 0
        text = ""
        for user in self.favorite_list:
            count += 1
            text += f"{count}: {user['profile_name']} ссылка: {user['link']}\n"
        return text

    def add_to_black_list(self):
        self.black_list.append(self.data)
        text = f"Профиль {self.data['profile_name']} больше не отобразится"
        return text
