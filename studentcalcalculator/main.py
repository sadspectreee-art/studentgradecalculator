ocenki = []
fio = []

while True:
    print('\n--------Калькулятор для оценки студента-------')
    print('1.Ввести данные студента')
    print('2.Добавить оценку')
    print('3.Показать все оценки')
    print('4.Рассчитать итоговый результат')
    print('5.Выход')

    choice = input('Выберите действие от 1 до 5: ').strip()
    if choice == '1':
        ocenki.clear()
        fio.clear()
        name = input('введите имя')
        fio.append(name)
        if name == '':
            print('нельзя оставить пустым')
        familia = input('введите фамилию')
        fio.append(familia)
        if familia == '':
            print('нельзя оставить пустым')
        vosrast = int(input('Введите возраст'))
        fio.append(vosrast)
        if 5> vosrast or vosrast > 100:
            print('Возраст не соответсвует указанному диапазону')
        else:
            print('готово')

    elif choice == '2':
        ocenka = int(input('Добавьте оценку'))
        if 0 < ocenka <= 100:
            ocenki.append(ocenka)
            print('добавлена',ocenki,)
        else:
            print('Введите значение от 0 до 100!')


    elif choice == '3':
        print(ocenki)

    elif choice == '4':
         print(f'\nКоличество оценок: {len(ocenki)}')
         summa = sum(ocenki)
         srball = summa / 2
         print(f'Средний Балл {srball}')
         km = max(ocenki)
         print(f'Максимальная оценка: {km}')
         mk = min(ocenki)
         print(f'Минимальная оценка: {mk}')
         if 90 <= summa <= 100:
                print(f'Сдал, Категория A')
         if 80 <= summa <= 89.99:
                print(f'Сдал, Категория B')
         if 70 <= summa <= 79.99:
             print(f'Сдал, Категория C')
         if 60 <= summa <= 69.99:
             print(f'Сдал, Категория D')
         if 60 > summa:
             print(f'Не сдал, Категория F')
         print (ocenki)




    elif choice == '5':
         print('\n\t\tВыход из программы')
    else:
         print('\n\t\tнадо ввести число от 1 до 5!')
