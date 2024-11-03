from enum import Enum
from typing import List, Dict


# Матрица доступа, где хранятся все возможные виды прав
class AccessMatrix(Enum):
    READ = 'Право на чтение'
    WRITE = 'Право на запись'
    TRANSFER = 'Передача прав'

# Класс статуса прав у пользователя
class AccessStatus(Enum):
    ALL_ACCESS = 'Полный доступ'
    TOTAL_BAN = 'Полный запрет'
    PARTIAL_ACCESS = 'Частичный доступ'

class Rights:
    def __init__(self, _status: AccessStatus, _rights: List[AccessMatrix]=None):
        self.__status = None
        self.__rights = None

        match _status:
            case AccessStatus.ALL_ACCESS:
                self.all_rights()
            case AccessStatus.TOTAL_BAN:
                self.total_ban()
            case AccessStatus.PARTIAL_ACCESS:
                self.__status = _status
                self.__rights = _rights

        if self.__status is None or self.__rights is None:
            raise ValueError('Неверно заданы права!')


    def add_right(self, right: AccessMatrix):
        if right not in self.__rights:
            self.__rights.append(right)
            if len(self.__rights) == len(AccessStatus):
                self.__status = AccessStatus.ALL_ACCESS
            else:
                self.__status = AccessStatus.PARTIAL_ACCESS

    def del_right(self, right: AccessMatrix):
        if right in self.__rights:
            self.__rights.remove(right)
            if len(self.__rights) == 0:
                self.__status = AccessStatus.TOTAL_BAN
            else:
                self.__status = AccessStatus.PARTIAL_ACCESS

    def all_rights(self):
        self.__rights = list(AccessMatrix)
        self.__status = AccessStatus.ALL_ACCESS

    def total_ban(self):
        self.__rights = []
        self.__status = AccessStatus.TOTAL_BAN

    def __str__(self):
        if self.__status in [AccessStatus.ALL_ACCESS, AccessStatus.TOTAL_BAN]:
            return self.__status.value
        else:
            ret_str = ''
            for right in self.__rights:
                ret_str += right.value + '\n'
            return ret_str

class Object:
    def __init__(self, _name: str):
        self.__name = _name

    def __str__(self):
        return self.__name


class UserRole(Enum):
    User = 'Обычный пользователь'
    Admin = 'Администратор'

class User:
    def __init__(self, _name: str,
                 _password: str,
                 _role: UserRole,
                 _obj: List[Object],
                 _rights: List[Rights]):
        self.__name = _name
        self.__password = _password
        self.__role = _role
        self.__rights = self.__create_obj_rights_dict(_obj, _rights)

    def __create_obj_rights_dict(self, obj_list: List[Object], rights_list: List[Rights]) -> Dict[Object, Rights]:
        if len(obj_list) != len(rights_list):
            raise ValueError('Списки объектов и прав должны быть одинаковой длины!')
        result = {}
        for obj, right in zip(obj_list, rights_list):
            result[obj] = right if self.__role==UserRole.User else Rights(AccessStatus.ALL_ACCESS)
        return result

    @property
    def name(self):
        return self.__name

    @property
    def password(self):
        _password = ''
        for i in self.__password:
            _password += '*'
        return _password

    @property
    def role(self):
        return self.__role.value

    @property
    def rights(self):
        return self.__rights

    def __str__(self):
        result = '\n' + 'Имя: ' + self.name + '\n'
        result += 'Пароль: ' + self.password + '\n'
        result += 'Роль: ' + self.role + '\n'
        return result


if __name__ == '__main__':
    r = Rights(AccessStatus.PARTIAL_ACCESS, [AccessMatrix.READ, AccessMatrix.WRITE])
    objects = [Object('Obj1'), Object('Obj2'), Object('Obj3')]
    rights = [Rights(AccessStatus.TOTAL_BAN), Rights(AccessStatus.TOTAL_BAN), Rights(AccessStatus.TOTAL_BAN)]
    user = User('name1', 'pas', UserRole.User, objects, rights)
    print('User: ', user)
    admin = User('name2', 'password', UserRole.Admin, objects, rights)
    print('Admin: ', admin)