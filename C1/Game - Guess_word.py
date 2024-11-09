# Объявление переменных

words_easy = { 
    "family":"семья", 
    "hand": "рука", 
    "people":"люди", 
    "evening": "вечер",
    "minute":"минута", 
}

words_medium = { 
    "believe":"верить", 
    "feel": "чувствовать", 
    "make":"делать", 
    "open": "открывать",
    "think":"думать", 
}

words_hard   = { 
    "rural":"деревенский", 
    "fortune": "удача", 
    "exercise":"упражнение", 
    "suggest": "предлагать",
    "except":"кроме", 
}

levels = {
   0: "Нулевой", 
   1: "Так себе", 
   2: "Можно лучше", 
   3: "Норм", 
   4: "Хорошо", 
   5: "Отлично",
}

difficultes = {'hard' : words_hard, 'medium' : words_medium, 'easy' : words_easy}

answers = {}

# Выбор сложности
player_difficult = input ('Давай поиграем в игру! Выбери уроверь сложности, напиши:\n"Hard" - для сложного\n"Medium" - для среднего\n"Easy" - для легкого\n->')

# Цикл - вопрос\ответ
for word in difficultes[player_difficult.lower()].keys():
    secret_word = word[0]+''.join(['*'*(len(word)-2)])+word[-1]
    player_answer = input (f'\nПереведи слово на английский - "{difficultes[player_difficult.lower()][word].title()}" *подсказка - {secret_word}\n->')
    if player_answer.lower() == word.lower():
        print ('Верно!')
        answers [word] = True
    else:
        print (f'Не верно. Правильный ответ - {word.title()}')
        answers [word] = False

# Вывод статистики
print ('\nВерно отвеченные слова:')
rang = [print (word) for word in answers if answers[word]== True]
print ('\nНе верно отвеченные слова:')
[print (word) for word in answers if answers[word]== False]
print (f'Ваш ранг: {levels[len(rang)]}')
