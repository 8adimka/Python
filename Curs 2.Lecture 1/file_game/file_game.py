import random

player_name = input ('Введите ваше имя:\n->')
print (f'Пользователь: {player_name}')
score = 0

with open (r'C:\Users\m8adi\Desktop\Python\Test_2\files\words.txt', 'r') as file:
    for line in file:
        secret_word = list (line.strip())
        random.shuffle (secret_word)
        secret_word = ''.join(secret_word)
        player_ansver = input (f'Угадайте слово: {secret_word}\n->')
        if player_ansver.lower() == line.strip().lower():
            print ('Верно! +10 очков!')
            score += 10
        else:
            print (f'Неверно! Верный ответ: {line.strip()}')

with open (r'C:\Users\m8adi\Desktop\Python\Test_2\files\history.txt', 'a+', encoding='utf-8') as file:
    file.write (f'{player_name}   {score}\n')
    file.seek(0)
    total = [line.strip() for line in file]
    total_games = len (total)
    total_score = 0
    total_max = 0
    for line in total:
        parts = line.split('   ')
        total_score += int (parts[-1])
        if int (parts[-1]) > total_max:
            total_max = int (parts[-1])

    print (f"total_score - {total_score}\nВсего игр сыграно: {total_games}\nМаксимальный рекорд: {total_max}")