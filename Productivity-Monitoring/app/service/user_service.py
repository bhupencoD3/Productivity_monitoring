from app.dao.user_dao import UserDAO

class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def get_user_by_email(self, email: str):
        return self.user_dao.get_user_by_email(email)
