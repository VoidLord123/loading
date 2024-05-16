import vk_api
from system.lib import Database
from vk_api.longpoll import VkLongPoll, VkEventType
from system.config import database_filename, dialogs_vk, test, results, vk_commands, vk_admin_id, time_constants
from system.vk_keyboards import not_subscribed, num_buttons, to_user


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.group_id = group_id
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkLongPoll(self.vk)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()
        self.database = Database(database_filename)

    def send_msg(self, send_id, message, keyboard=None):
        """
        Отправка сообщения через метод messages.send
        :param send_id: vk id пользователя, который получит сообщение
        :param message: содержимое отправляемого письма
        :param keyboard: объект клавиатуры для отправки
        :return: None
        """
        params = {
            "peer_id": send_id,
            "message": message,
            "random_id": 0
        }
        if keyboard:
            params["keyboard"] = keyboard.get_keyboard()
        self.vk_api.messages.send(**params)

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(518223512, "Привет-привет!")

    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    self.handle_events(event)

    def is_member(self, user_id):
        return self.vk.method("groups.isMember", {"group_id": self.group_id,
                                                  "user_id": user_id})

    def handle_events(self, event):
        user_id = event.user_id
        string_id = str(user_id)
        in_db = self.database.check_user(string_id, "vk")
        if in_db:
            in_test = self.database.get_user_status(string_id, "vk")
            passed = self.database.get_user_passed(string_id, "vk")
        else:
            in_test = False
            passed = False
        if not self.is_member(event.user_id):
            self.handle_not_subscribed(event)
        elif event.text == vk_commands["start"]:
            if not in_test and not passed:
                if not in_db:
                    self.database.add_user(string_id, user_type="vk")
                    self.database.set_user_status(string_id, True, "vk")
                self.send_msg(user_id, "Отвечайте на вопросы числом от 1 до 10."
                                       " После ответа на все вопросы вы получите результат")
                self.send_msg(user_id, test[self.database.get_user_index(string_id, "vk")], num_buttons)
        elif event.text in [str(i) for i in range(1, 11)] and in_test and not passed:
            fin, scr = self.database.answer(string_id, int(event.text), "vk")
            if fin:
                i = 0
                while not scr < results[i][0]:
                    i += 1
                self.database.set_user_passed(string_id, True, "vk")
                self.send_msg(user_id, results[i][-1])
                self.send_msg(user_id, dialogs_vk["finish_test"], to_user)
            else:
                self.send_msg(user_id, test[self.database.get_user_index(string_id, "vk")], num_buttons)
        elif event.text.lower() == vk_commands["first"]:
            self.send_msg(user_id, dialogs_vk["start_bot"], not_subscribed)
        elif event.text == vk_commands["statistic"]:
            if string_id != vk_admin_id:
                self.send_msg(user_id, "Вы не имеете доступа")
                return
            st = self.database.get_statistics()
            t = dialogs_vk["statistic"]
            t = t.replace("{vk_m}", str(st["month"]["vk"]))
            t = t.replace("{tg_m}", str(st["month"]["tg"]))
            t = t.replace("{all_m}", str(st["month"]["all"]))
            t = t.replace("{vk_a}", str(st["all_time"]["vk"]))
            t = t.replace("{tg_a}", str(st["all_time"]["tg"]))
            t = t.replace("{all_a}", str(st["all_time"]["all"]))
            self.send_msg(user_id, t)
        elif event.text.startswith(vk_commands["sending"]):
            # /sending [mth] [n] or [all] ~msg~
            if string_id != vk_admin_id:
                self.send_msg(user_id, "Вы не имеете доступа")
                return
            try:
                k = event.text.split("~")
                n = k[0].split(' ')
                if len(n) == 3:
                    self.sending(1, "all", k[1])
                else:
                    self.sending(int(n[2]), n[1], k[1])
                self.send_msg(user_id, "Успешно")
            except Exception:
                self.send_msg(user_id, "Что то пошло не так. Попробуйте снова.")

    def sending(self, n: int, d: str, msg: str):
        if d != "all":
            d2 = time_constants[d] * n
            for i in self.database.get_active_users(d2, "vk"):
                self.send_msg(i.user_id, msg)
        else:
            for i in self.database.get_all_users("vk"):
                self.send_msg(i.user_id, msg)

    def handle_not_subscribed(self, event):
        self.send_msg(event.user_id, dialogs_vk["not_subscribed"], not_subscribed)
