questions = ["Me ___  Vadim", "Soy ___ Russia", "Vivo ___ Spain"]
answers = ["llamo", "de", "en"]
right_answers = 0
score = 0

start = int(input ('Привет! Давай поиграем в игру?\n1- Запустить игру\n2 - Выход\n-> '))
if start == 1:
    print ('Предлагаю проверить свои знания Испанского!\nЗа каждый правильный ответ тебе начисляются балы.\nУ тебя три попытки. За верный ответ с первой попытки - 3 балла, со второй - 2 и т.д.\nУдачи!')
    for i in range (len(questions)):        
        chanses = 3
        while chanses>0:
            player_answer = input (f'Введи недостающее слово: {questions[i]}\n')
            if player_answer.lower() == answers [i].lower():
                print ('Верно!')
                right_answers += 1
                score += chanses
                break
            else:
                chanses -= 1
                print (f'Осталось попыток: {chanses}, попробуйте еще раз!')
        else:
            print (f'Неправильно. Правильный ответ: {answers [i]}')
    print (f'Вот и всё! Вы ответили на {right_answers} из {len (questions)} вопросов верно, это {round(right_answers / (len(questions)/100), 1)} процентов и набрали {score} баллов. ')
elif start == 2:
    print ('Кажется, вы не хотите играть. Тогда всего доброго!')
else:
    print ('Я такого не знаю')