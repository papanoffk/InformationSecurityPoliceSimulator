from enum import Enum
from random import choice

# Уровни доступа
class SecurityAttributes(Enum):
    LEVEL_0 = 'Открытые данные'
    LEVEL_1 = 'Секретно'
    LEVEL_2 = 'Совершенно секретно'

# Класс, реализующий объект
class Object:
    def __init__(self, _name: str, _security: SecurityAttributes):
        self.__name = _name
        self.__security = _security

    @property
    def security_level(self) -> SecurityAttributes:
        return self.__security

    @property
    def name(self) -> str:
        return self.__name

    def __str__(self):
        return self.__name

# Класс, реализующий пользователя
class User:
    def __init__(self, _name: str, _password: str, _security: SecurityAttributes):
        self.__name = _name
        self.__password = _password
        self.__security = _security

    @property
    def security_level(self) -> SecurityAttributes:
        return self.__security

    @property
    def name(self) -> str:
        return self.__name

    @property
    def password(self):
        return '*' * len(self.__password)

    def __str__(self):
        return self.__name

# Проверка на доступ субъекта к объекту
def can_user_access_to(_user: User, _obj: Object) -> bool:
    user_security_lvl = _user.security_level
    obj_security_lvl = _obj.security_level
    if user_security_lvl == obj_security_lvl:
        return True
    for lvl in SecurityAttributes:
        if user_security_lvl == lvl:
            return False
        if obj_security_lvl == lvl:
            return True

# Класс, реализующий мандатную модель
class Mandatory:
    def __init__(self, user_count: int, obj_count: int):
        self.__users = [User(f'User-{i}', 'admin', choice(tuple(SecurityAttributes))) for i in range(user_count)]
        self.__objs = [Object(f'Object-{i}', choice(tuple(SecurityAttributes))) for i in range(obj_count)]

    @property
    def users(self):
        return self.__users

    @property
    def objects(self):
        return  self.__objs

    def __str__(self):
        result = 'Пользователи: \n'
        for user in self.__users:
            result += str(user) + ': ' + user.security_level.value + '\n'
        result += 'Объекты \n'
        for obj in self.__objs:
            result += str(obj) + ': ' + obj.security_level.value + '\n'

        return result

if __name__ == '__main__':
    some_obj = Object('Obj', SecurityAttributes.LEVEL_0)
    some_user = User('User', 'Admin', SecurityAttributes.LEVEL_2)
    some_mandatory = Mandatory(7, 4)
    print(some_mandatory)
