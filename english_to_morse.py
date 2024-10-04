# Импортируем библеотеку. 
# (Вопрос - Библеотеки, которые планируем использовать, надо импортировать сразу или только там, где они нам реально понадобились?)
import random

# Объявление переменных
dict_english = {
  "0": "-----",
  "1": ".----",
  "2": "..---",
  "3": "...--",
  "4": "....-",
  "5": ".....",
  "6": "-....",
  "7": "--...",
  "8": "---..",
  "9": "----.",
  "a": ".-",
  "b": "-...",
  "c": "-.-.",
  "d": "-..",
  "e": ".",
  "f": "..-.",
  "g": "--.",
  "h": "....",
  "i": "..",
  "j": ".---",
  "k": "-.-",
  "l": ".-..",
  "m": "--",
  "n": "-.",
  "o": "---",
  "p": ".--.",
  "q": "--.-",
  "r": ".-.",
  "s": "...",
  "t": "-",
  "u": "..-",
  "v": "...-",
  "w": ".--",
  "x": "-..-",
  "y": "-.--",
  "z": "--..",
  ".": ".-.-.-",
  ",": "--..--",
  "?": "..--..",
  "!": "-.-.--",
  "-": "-....-",
  "/": "-..-.",
  "@": ".--.-.",
  "(": "-.--.",
  ")": "-.--.-",
  " ": "*"
}
word_list = ['little','husband','month','tree', 'school', 'paper', 'question', 'get', 'hear', 'remember', 'understand', 'find']
levels = {
   0: "Нулевой", 
   1: "Так себе", 
   2: "Можно лучше", 
   3: "Норм", 
   4: "Хорошо", 
   5: "Отлично",
}
dict_answers = {}

def get_secret_words (text):
    """
    Шифрует введённое слово
    """
    words_list = text.split (' ')
    secret_words = []
    for word in words_list:
        secret_word = word[0]+'*'*(len(word)-2)+word[-1]
        secret_words.append (secret_word)
    return ' '.join(secret_words)


def text_to_morse(text):
    """
    Переводит введённое слово с Английского на язык Морзе
    """
    morse_word = ' '.join([dict_english[letter] for letter in text if letter in dict_english])
    return morse_word


def morse_to_word (morse_word):
    """
    Переводит введённое слово с языка Морзе на Английский
    """
    morse_list = morse_word.split (' ')
    english_word = []
    for mor in morse_list:
        for letter, mor_sight in dict_english.items():
            if mor == mor_sight:
                english_word.append(letter)
    return ''.join(english_word)


def get_statistics (dict_answers):
    """
    Печатает статистику изходя из вводимого словаря
    """
    print ('Верно угаданные слова:')
    rang = [print (word) for word in dict_answers if dict_answers[word]==True]
    print ('Не верно угаданные слова:')
    [print(word) for word in dict_answers if dict_answers[word]==False]
    print (f'Ваш ранг: {levels[len (rang)]}')


def main ():
    # Вступление и выбор выполняемого блока
    print ('Привет!\nСегодня написал программу для перевода Английского текста в Язык морзе и обратно.\nВыбери интересующий тебя блок:')
    while True:
        is_start = int (input ('''                    
                        1 - Перевести текст с Английского на язык Морзе,
                        2 - Пересести текст с языка Морзе на Английский,
                        3 - Игра-викторина, где надо будет угадывать слово закодированное языком Морзе,
                        4 - Выход.
                        -> '''))

        if is_start == 1:
            # Переводим введённое слово с Английского на язык Морзе
            player_english = input ('Введите текст на Английском языке:\n-> ').lower()
            print ('На языке морзе это получается:\n' + text_to_morse (player_english))

        elif is_start == 2:
            # Переводим введённое слово с языка Морзе на Английский
            player_morse = input ('Введите выражение на языке Морзе:\n-> ').lower()
            print ('В переводе на Английский это будет:\n' + morse_to_word (player_morse))

        elif is_start == 3:
            # Получаем рандомный список из 5-ти слов
            random_words = random.sample (word_list, 5)
            
            # Цикл вопрос/ответ
            for word in random_words:
                print ("Угадайте какое слово было закодированно Азбукой Морзе: ", text_to_morse (word), '\nПодсказка ->', get_secret_words(word))
                player_answer = input ('Введите загаданное слово:\n-> ').lower()
                if player_answer == word:
                    print ('Верно!\n')
                    dict_answers [word] = True
                else:
                    print (f'Неверно! Это слово - {word}\n')
                    dict_answers [word] = False

            # Вывод статистики
            get_statistics (dict_answers)

        elif is_start == 4:
            # Выход из програмы
            print ('Ну что ж! Тогда хорошего тебе дня!')
            break

        else:
            # Неверная команда
            print ('Я не знаю такой команды')

main ()