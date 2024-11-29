import random

# Функция для перемешивания букв в слове
def shuffle_word(word):
    letters = list(word)
    random.shuffle(letters)
    return ''.join(letters)

# Чтение списка слов из файла
def read_words_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file.readlines()]
    return words

# Запись результатов в файл history.txt
def save_score(username, score):
    with open('history.txt', 'a', encoding='utf-8') as file:
        file.write(f'{username}   {score}\n')

# Чтение истории игр из файла history.txt и вывод статистики
def read_and_print_stats():
    try:
        with open('history.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if not lines:
                print("Нет сохранённых результатов.")
                return
            scores = [int(line.split('   ')[1]) for line in lines]
            total_games = len(scores)
            max_score = max(scores)
            print(f"Всего игр сыграно: {total_games}")
            print(f"Максимальный рекорд: {max_score}")
    except FileNotFoundError:
        print("Нет сохранённых результатов.")

# Основная функция игры
def play_game():
    # Просим пользователя представиться
    username = input("Введите ваше имя: ")

    # Читаем слова из файла
    words = read_words_from_file('words.txt')
    
    score = 0  # Счёт игрока

    # Шаг 3: Перебираем все слова
    for word in words:
        shuffled_word = shuffle_word(word)
        print(f"**** Угадайте слово: {shuffled_word}")
        user_guess = input("Ваш ответ: ")

        if user_guess == word:
            print("Верно! Вы получаете 10 очков.")
            score += 10
        else:
            print(f"Неверно! Верный ответ – {word}.")

    # Шаг 4: Запись результата
    save_score(username, score)

    # Вывод результатов
    print(f"Игра завершена. Ваш счёт: {score} очков.")

    # Шаг 5: Вывод статистики
    read_and_print_stats()

# Запускаем игру
if __name__ == "__main__":
    play_game()