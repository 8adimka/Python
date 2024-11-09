import json
import requests
import random
import os

def get_data (url):
    """Получает данные в виде 'json'-файла по передаваемому адресу - url"""
    resp = requests.get (url)
    if resp.status_code == 200:
        word_dict = resp.json()
        return word_dict
    else:
        print ('Ошибка загрузки данных')
        return None

def get_random_dict (data):
    '''Получает рандомный словарь из списка словарей'''
    if data:
        return random.choice(data)
    else:
        print ('Нет данных для обработки')
        return None
    
def word_is_correct (player_answer, subwords, answers):
    if player_answer not in answers:
        if player_answer in subwords:
            print ('Верно!')
            return True
        else:
            print ('Неверно')
            return False
    print ('Такое слово уже было')
    return False
    
    
def main ():
    # Получаем данные для работы
    data = get_data ('https://api.npoint.io/0e3ac92f25cd629e3fd4')
    random_dict = get_random_dict (data)
    word = random_dict['word']
    subwords = random_dict['subwords']

    # Начинаем цикл игры
    player_name = input ('Ввведите имя игрока\n->')

    print (f'Привет, {player_name}!\nСоставьте {len(subwords)} слов из слова {word.upper()}\nСлова должны быть не короче 3 букв\nЧтобы закончить игру, угадайте все слова или напишите "стоп"\nПоехали, ваше первое слово?')
    answers= []
    while True:
        if len(answers) < len(subwords):
            player_answer = (input ('->')).lower()
            if player_answer == 'стоп'.lower():
                print ('Ну вот и всё!')
                break
            else:    
                if word_is_correct (player_answer, subwords, answers):
                    answers.append (player_answer)
        else:
            break
    print (f'Игра завершена, вы угадали {len(answers)} слов!')

main()

class Player:
    def __init__ (self, name, score):
        self.name = name


