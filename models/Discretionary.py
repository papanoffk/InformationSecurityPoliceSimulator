from enum import Enum
from typing import List


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


if __name__ == '__main__':
    r = Rights(AccessStatus.PARTIAL_ACCESS, [AccessMatrix.READ, AccessMatrix.WRITE])
    print(r)