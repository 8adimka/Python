score = 0
libr = {'My name ___ Vova.':'is', 'I ___ a coder.':'am', "I live ___ Moscow.":"in"}

player_name = input ('Введите ваше имя - ')
print (f'''Привет, {player_name}!
Давай поиграем в Игру!''')
starting = (input ('Если не хочешь скажи нет, иначе начинаем! ->')).lower()
if starting == 'нет':
    print ('Тогда пока-пока!')
else:
    print ('Начинаем!')
    for i in libr:
        print (i)
        player_answer = (input ('Введите пропущенное слово - ')).lower()
        if player_answer == libr [i]:
            print ('Верно!')
            score += 1
        else:
            print ('Не верно!')
    print (f'Правильных ответов - {score}')

