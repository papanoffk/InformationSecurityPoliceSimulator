from enum import Enum
from typing import List, Dict
from random import sample, randint


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

# Класс, реализующий права пользователя
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
                self.__rights = _rights
                if len(_rights) == len(AccessStatus):
                    self.__status = AccessStatus.ALL_ACCESS
                elif len(_rights) == 0:
                    self.__status = AccessStatus.TOTAL_BAN
                else:
                    self.__status = _status

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
            ret_str = ', '.join(i.value for i in self.__rights)
            return ret_str

# Класс, реализующий объект, к которому у пользователя есть права доступа
class Object:
    def __init__(self, _name: str):
        self.__name = _name

    def __str__(self):
        return self.__name

# Перечисление ролей пользователя
class UserRole(Enum):
    User = 'Обычный пользователь'
    Admin = 'Администратор'

# Класс, реализующий пользователя
class User:
    def __init__(self, _name: str,
                 _password: str,
                 _role: UserRole,
                 _obj: List[Object],
                 _rights: List[Rights]):
        self.__name = _name
        self.__password = _password
        self.__role = _role
        self.__rights: Dict[Object, Rights] = self.__create_obj_rights_dict(_obj, _rights)

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

    @role.setter
    def role(self, value: UserRole):
        if value == UserRole.Admin:
            for right in self.__rights:
                self.__rights[right].all_rights()
        self.__role = value

    @property
    def rights(self):
        return self.__rights

    def __str__(self):
        result = '\n' + 'Имя: ' + self.name + '\n'
        result += 'Пароль: ' + self.password + '\n'
        result += 'Роль: ' + self.role + '\n'
        return result

#
class Discretionary:
    def __init__(self, user_count: int, admin_count: int, object_count):
        if admin_count > user_count:
            raise ValueError('Количество админов должно быть меньше или равно кол-ву пользователей!')

        # Заполняем объекты
        self.__objects = [Object(f'Object-{i}') for i in range(object_count)]

        # Заполняем пользователей
        self.__users = []
        access_length = len(AccessMatrix)
        for i in range(user_count):
            self.__users.append(self.__create_random_user(i, object_count, access_length))

        # Создаем админа
        admins = sample(self.__users, admin_count)
        for admin in admins:
            admin.role = UserRole.Admin

    def __create_random_user(self, index: int, obj_count: int, access_len: int):
        _rights = []
        for i in range(obj_count):
            random_access = sample(list(AccessMatrix), randint(0, access_len))
            _rights.append(Rights(AccessStatus.PARTIAL_ACCESS, random_access))

        return User(f'User-{index}', 'admin', UserRole.User, self.__objects, _rights)

    def __str__(self):
        user_column = 24
        column = 36
        # Построение строки с объектами
        _obj_mas_to_str = [str(i) for i in self.__objects]
        _obj_str = ' ' * user_column +  '|'
        for obj in _obj_mas_to_str:
            dif = column - len(obj)
            left_dif = int(dif/2)
            right_dif = dif - left_dif
            _obj_str += ' ' * left_dif + obj + ' ' * right_dif + '|'
        _obj_str += '\n'
        _obj_str += '-' * user_column + '|' + ''.join('-' * (column+1) for i in self.__objects) + '\n'

        # Построение строк с пользователями
        _users_strs = []
        for user in self.__users:
            _users_str = ' ' * user_column + '|' + ''.join(' ' * column + '|' for i in user.rights) + '\n'
            _users_str += f'{user.name}' + ' ' * (user_column - len(user.name)) + '|'
            _rights_mas_to_str = [i.__str__() for i in user.rights.values()]
            for right_str in _rights_mas_to_str:
                dif = column - len(right_str)
                left_dif = int(dif / 2)
                right_dif = dif - left_dif
                _users_str += ' ' * left_dif + right_str + ' ' * right_dif + '|'
            _users_str += '\n'
            _users_str += f'{user.role}' + ' ' * (user_column - len(user.role)) + '|' + ''.join(' ' * column + '|' for i in _rights_mas_to_str) + '\n'
            _users_str += '-' * user_column +  '|' + ''.join('-' * (column+1) for i in _rights_mas_to_str) + '\n'
            _users_strs.append(_users_str)

        result = _obj_str + ''.join(_users_strs)
        return result


if __name__ == '__main__':
    r = Rights(AccessStatus.PARTIAL_ACCESS, [AccessMatrix.READ, AccessMatrix.WRITE])
    objects = [Object('Obj1'), Object('Obj2'), Object('Obj3')]
    rights = [Rights(AccessStatus.TOTAL_BAN), Rights(AccessStatus.TOTAL_BAN), Rights(AccessStatus.TOTAL_BAN)]
    _user = User('name1', 'pas', UserRole.User, objects, rights)
    print('User: ', _user)
    _admin = User('name2', 'password', UserRole.Admin, objects, rights)
    print('Admin: ', _admin)

    some = Discretionary(9, 1, 6)
    print(some)