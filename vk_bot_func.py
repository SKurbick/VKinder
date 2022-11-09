from token_file import token_vk_group_bot
from config import start_keyboard, help_message, second_keyboard
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api_func import VK

vk_session = vk_api.VkApi(token=token_vk_group_bot)
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)


def sender(vk_id, keyboard=start_keyboard, text=None, photos=None, ):
    vk_session.method('messages.send', {'user_id': vk_id, 'message': text,
                                        "attachment": photos,
                                        "random_id": 0, "keyboard": keyboard})


favorite_list = []
black_list = []
datas = None
data = None
for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message_from_user = event.text.lower()
            vk_user_id = event.user_id
            if message_from_user == "start" or message_from_user == "изменить поисковые данные"\
                    or message_from_user == "ввести данные для поиска":
                sender(vk_user_id, text=help_message)

            if message_from_user[:6] == "поиск:":
                print(message_from_user)
                search, city, sex, age_from, age_to = message_from_user.split()
                sex_key = {"мужской": 2, "женский": 1, "любой": 0}
                vk_search_user = VK(city=city, sex=sex_key[sex], age_from=age_from, age_to=age_to)
                datas = iter(vk_search_user.users_search())
                data = next(datas)
                print(data)
                sender(vk_user_id, text=f"{data['profile_name']}\n {data['link']}")

                vk_upload_photo = VK(users_id=f"{data['user_id']}")
                users_photo = vk_upload_photo.get_photos()
                for photo in users_photo:
                    sender(vk_user_id, text=None, photos=photo['attachment'], keyboard=second_keyboard)

            if message_from_user == "следующий профиль":
                data = next(datas)
                print(data)
                print(message_from_user)
                sender(vk_user_id, text=f"{data['profile_name']}\n {data['link']}")

                vk_upload_photo = VK(users_id=f"{data['user_id']}")
                users_photo = vk_upload_photo.get_photos()
                for photo in users_photo:
                    sender(vk_user_id, text=None, photos=photo['attachment'], keyboard=second_keyboard)

            if message_from_user == "добавить в избранное":
                if data not in favorite_list:
                    favorite_list.append(data)
                    sender(vk_user_id,
                           text=f"Профиль '{data['profile_name']}' добавлен в избранное",
                           keyboard=second_keyboard)
                    print(favorite_list)
                else:
                    sender(vk_user_id,
                           text=f"Профиль '{data['profile_name']}' уже был в избранном",
                           keyboard=second_keyboard)
                    print(favorite_list)
            if message_from_user == "добавить в черный список":
                black_list.append(data)
                sender(vk_user_id, text=f"Профиль {data['profile_name']} больше не отобразится",
                       keyboard=second_keyboard)

            if message_from_user == "список избранных":
                count = 0
                for user in favorite_list:
                    count += 1
                    sender(vk_user_id, text=f"{count}: {user['profile_name']} ссылка: {user['link']}")
