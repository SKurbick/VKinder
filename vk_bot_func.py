from token_file import token_vk_group_bot
from config import start_keyboard, help_message, second_keyboard
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from main import VK

vk_session = vk_api.VkApi(token=token_vk_group_bot)
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)


def sender(vk_id, keyboard=start_keyboard, text=None, photos=None, ):
    vk_session.method('messages.send', {'user_id': vk_id, 'message': text,
                                        "attachment": photos,
                                        "random_id": 0, "keyboard": keyboard})


profiles = []
datas = None
data = None
id_in_profiles = 0
for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            vk_user_id = event.user_id
            if msg == "start" or msg == "изменить поисковые данные" or msg == "вести данные для поиска":
                sender(vk_user_id, text=help_message)
            # msg == "ввести данные для поиска" or "изменить поисковые данные":
            if msg[:6] == "поиск:":
                print(msg)
                search, city, sex, age_from, age_to = msg.split()
                vk_search_user = VK(city=city, sex=sex, age_from=age_from, age_to=age_to)
                datas = iter(vk_search_user.users_search())
                data = next(datas)
                print(data)
                sender(vk_user_id, text=f"{data['profile_name']}\n {data['link']}")

                vk_upload_photo = VK(users_id=f"{data['user_id']}")
                users_photo = vk_upload_photo.get_photos()
                for photo in users_photo:
                    sender(vk_user_id, text=None, photos=photo['attachment'], keyboard=second_keyboard)

            if msg == "следующий профиль":
                data = next(datas)
                print(data)
                print(msg)
                sender(vk_user_id, text=f"{data['profile_name']}\n {data['link']}")

                vk_upload_photo = VK(users_id=f"{data['user_id']}")
                users_photo = vk_upload_photo.get_photos()
                for photo in users_photo:
                    sender(vk_user_id, text=None, photos=photo['attachment'], keyboard=second_keyboard)
            # else:
            #     sender(vk_user_id, text=start_message, keyboard=second_keyboard)
            if msg == "добавить в избранное":
                if data not in profiles:
                    profiles.append(data)
                    sender(vk_user_id,
                           text=f"Профиль '{data['profile_name']}' добавлен в избранное",
                           keyboard=second_keyboard)
                    print(profiles)
                else:
                    sender(vk_user_id,
                           text=f"Профиль '{data['profile_name']}' уже был в избранном",
                           keyboard=second_keyboard)
                    print(profiles)
            if msg == "список избранных":
                count = 0
                for user in profiles:
                    count += 1
                    sender(vk_user_id, text=f"{count}: {user['profile_name']} ссылка: {user['link']}")
