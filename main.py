from token_file import token_vk_group_bot
from config import start_keyboard, how_search_message, second_keyboard
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot_func import BotFunction

vk_session = vk_api.VkApi(token=token_vk_group_bot)
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)


def sender(vk_id, keyboard=start_keyboard, text=None, photos=None, ):
    vk_session.method('messages.send', {'user_id': vk_id, 'message': text,
                                        "attachment": photos,
                                        "random_id": 0, "keyboard": keyboard})


for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message_from_user = event.text.lower()
            vk_user_id = event.user_id
            if message_from_user == "start" or message_from_user == "изменить поисковые данные" \
                    or message_from_user == "ввести данные для поиска":
                sender(vk_user_id, text=how_search_message)

            if message_from_user[:5] == "поиск":
                search, city, sex, age_from, age_to = message_from_user.split()
                vk = BotFunction(vk_user_id=vk_user_id, city=city, sex=sex, age_from=age_from, age_to=age_to)
                text_for_user, photos_for_user = vk.user_search_data()
                sender(vk_user_id, text=text_for_user, photos=photos_for_user, keyboard=second_keyboard)

            if message_from_user == "следующий профиль":
                text_for_user, photos_for_user = vk.next_profile()
                sender(vk_user_id, text=text_for_user, photos=photos_for_user, keyboard=second_keyboard)

            if message_from_user == "добавить в избранное":
                text_for_user = vk.add_to_favorites_lists()
                sender(vk_user_id, text=text_for_user, keyboard=second_keyboard)

            if message_from_user == "добавить в черный список":
                text_for_user = vk.add_to_black_list()
                sender(vk_user_id, text=text_for_user, keyboard=second_keyboard)

            if message_from_user == "список избранных":
                text_for_user = vk.show_favorites_list()
                sender(vk_user_id, text=text_for_user, keyboard=second_keyboard)
