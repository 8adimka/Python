import random

def get_secret_word (word):
    '''
    Функция для перемешивания букв в слове
    '''
    letters = list(word)
    random.shuffle (letters)
    return ''.join(letters)


def get_words (file_name='words.txt'):
    '''
    Чтение списка слов из файла
    '''
    with open (file_name, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


def record_results (player_name, score, file_name='history.txt'):
    '''
    Запись результатов в файл history.txt
    '''
    with open (file_name, 'a', encoding='utf-8') as file:
        file.writelines (f'{player_name}   {score}')


def show_results (file_name='history.txt'):
    '''
    Чтение истории игр из файла history.txt и вывод статистики
    '''
    with open (file_name, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
        score = [int(num.split ('   ')[-1]) for num in lines]
        total_score = sum (score)
        max_score = max (score)
        count_game = len (score)
        print (f'Всего игр сыграно: {count_game}\n"Максимальный рекорд: {max_score}\nОбщий счёт:{total_score}')


def main ():
    '''
    Основная функция игры
    '''
    # Просим пользователя представиться
    player_name = input ("Введите ваше имя:\n->")

    # Получаем слова из файла
    words = get_words ()

    score = 0  # Счёт игрока

    # Цикл удавывания зашиврованных слов
    for word in words:
        player_answer = input (f'Постарайся угадать зашифрованное слово: {get_secret_word (word)}\n->')
        if player_answer.lower() == word.lower():
            print ('Верно! +10 очков!')
            score += 10
        else:
            print (f'Не верно! Это слово - {word}')

    # Запись результатов
    record_results (player_name, score)

    # Вывод статистики
    print (f'Ваш результат: {score}')
    show_results ()


main ()
