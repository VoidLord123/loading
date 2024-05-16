import datetime


from system.config import test
from system.data.__all_models import *
from system.data.db_session import *


class Database:

    def __init__(self, file: str):
        global_init(file)
        self.session = create_session()

    def check_user(self, user_id: str, user_type="vk"):
        users = self.session.query(Users.User)
        filtered = users.filter(Users.User.user_id == user_id, Users.User.type == user_type).all()
        return len(filtered) > 0

    def add_user(self, user_id: str, last_time: datetime.datetime = datetime.datetime.now(),
                 user_type: str = "vk"):
        us = Users.User()
        us.user_id = user_id
        us.last_date = last_time
        us.type = user_type
        self.session.add(us)
        self.session.commit()

    def get_user(self, user_id: str, user_type: str):
        user = self.session.query(Users.User).filter(Users.User.user_id == user_id,
                                                     Users.User.type == user_type).first()
        return user

    def answer(self, user_id: str, answer: int, user_type: str = "vk"):
        user = self.get_user(user_id, user_type)
        user.question_id += 1
        user.score += answer
        self.session.commit()
        user = self.get_user(user_id, user_type)
        if user.question_id >= len(test):
            user.in_test = False
            user.last_date = datetime.datetime.now()
            self.session.commit()
            return True, user.score
        return False, -1

    def get_user_status(self, user_id: str, user_type: str = "vk"):
        user = self.get_user(user_id, user_type)
        return user.in_test

    def set_user_status(self, user_id: str, status: bool, user_type: str = "vk"):
        user = self.get_user(user_id, user_type)
        user.in_test = status
        self.session.commit()
        return user.in_test

    def get_user_passed(self, user_id: str, user_type: str = "vk"):
        user = self.get_user(user_id, user_type)
        return user.passed

    def set_user_passed(self, user_id: str, status: bool, user_type: str = "vk"):
        user = self.get_user(user_id, user_type)
        user.passed = status
        self.session.commit()
        return user.passed

    def get_user_index(self, user_id: str, user_type: str):
        return self.get_user(user_id, user_type).question_id

    def get_all_users(self, user_type: str = "", passed: bool = True) -> list[Users.User]:
        if user_type:
            return self.session.query(Users.User).filter(Users.User.type == user_type,
                                                         Users.User.passed == passed).all()
        else:
            return list(self.session.query(Users.User).all())

    def get_active_users(self, delta: datetime.timedelta, user_type: str = "") -> list[Users.User]:
        us = self.get_all_users(user_type)
        b = []
        for i in us:
            if i.last_date + delta >= datetime.datetime.now():
                b.append(i)
        return b

    def get_statistics(self):
        tg_month = len(self.get_active_users(datetime.timedelta(days=31), "tg"))
        vk_month = len(self.get_active_users(datetime.timedelta(days=31), "vk"))
        all_month = len(self.get_active_users(datetime.timedelta(days=31)))
        tg_all = len(self.get_all_users("tg"))
        vk_all = len(self.get_all_users("vk"))
        all_all = len(self.get_all_users())
        return {
            "month": {
                "vk": vk_month,
                "tg": tg_month,
                "all": all_month
            },
            "all_time": {
                "vk": vk_all,
                "tg": tg_all,
                "all": all_all
            }
        }


if __name__ == "__main__":

    db = Database("db/database.sqlite")
    print(db.get_statistics())
