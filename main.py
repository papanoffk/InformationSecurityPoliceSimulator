
from models.Mandatory import Mandatory, can_user_access_to
from models.Discretionary import Discretionary, AccessMatrix


MANDATORY_USER_COUNT, MANDATORY_OBJECT_COUNT = 7, 4
DISCRETIONARY_USER_COUNT, DISCRETIONARY_ADMIN_COUNT, DISCRETIONARY_OBJECT_COUNT = 9, 1, 6


def simulation_of_mandatory():
    model = Mandatory(MANDATORY_USER_COUNT, MANDATORY_OBJECT_COUNT)
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
                    print(f'{counter} - ' + str(obj) + ': ' + obj.security_level.value)
                    counter += 1
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

def simulation_of_discretionary():
    model = Discretionary(DISCRETIONARY_USER_COUNT, DISCRETIONARY_ADMIN_COUNT, DISCRETIONARY_OBJECT_COUNT)
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
                    print(f'{counter} - ' + str(obj) + ': ' + str(user.rights[obj]))
                    counter += 1
                menu = input()
                if menu == 'q':
                    print('Вы вышли из системы!')
                    break
                else:
                    try:
                        obj = objs[int(menu)]
                        print('Выберете, каким правом воспользоваться (q - для выхода):')
                        access_counter = 0
                        for access in AccessMatrix:
                            print(f'{access_counter} - ' + access.value)
                            access_counter += 1
                        menu = input()
                        if menu == 'q':
                            print('Вы вышли из системы!')
                            break
                        elif list(AccessMatrix)[int(menu)] in user.rights[obj].rights:
                            print('Вы успешно воспользовались правом.')
                        else:
                            print('У вас не прав на это.')
                    except Exception as e:
                        print(e)
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
                simulation_of_discretionary()
            case '3':
                break
            case _:
                print('Z-z-z...')

        input()



if __name__ == '__main__':
    main()