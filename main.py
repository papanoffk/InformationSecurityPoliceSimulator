import os

from models.Mandatory import Mandatory, can_user_access_to


MANDATORY_USER_COUNT, MANDATORY_SUBJECT_COUNT = 7, 4


def simulation_of_mandatory():
    model = Mandatory(MANDATORY_USER_COUNT, MANDATORY_SUBJECT_COUNT)
    print(model)
    if input('Зайти в систему (Да, Нет)?').lower() == 'да':
        print('Введите данные для входа')
        name = input('Идентификатор: ')
        password = input('Пароль: ')
        user = None
        for _user in model.users:
            if _user.name == name and _user.check_password(password):
                user = _user
                break
        if user is not None:
            print('Вы вошли в систему!')
            objs = model.objects
            while True:
                print('Выберете номер объекта (q - для выхода):')
                counter = 0
                for obj in objs:
                    counter += 1
                    print(f'{counter} - ' + str(obj) + ': ' + obj.security_level.value)
                menu = input()
                if menu == 'q':
                    print('Вы вышли из системы!')
                    break
                else:
                    try:
                        obj = objs[int(menu)]
                        if can_user_access_to(user, obj):
                            print('Доступ получен.')
                        else:
                            print('Доступа нет.')
                    except:
                        print('Неверный ввод!')
        else:
            print('Не удалось войти!')


def main():
    while True:
        print('Выберите модель: ')
        print('1. Мандатная')
        print('2. Дискреционная')
        print('3. Это выход, Нео!')

        match input('Введите номер модели: '):
            case '1':
                simulation_of_mandatory()
            case '2':
                print('Пока не реализовано!')
            case '3':
                break
            case _:
                print('Z-z-z...')

        input()



if __name__ == '__main__':
    main()