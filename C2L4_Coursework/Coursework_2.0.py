import random
import requests

class BasicWord:
    def __init__(self, word, subwords):
        self.word = word
        self.subwords = subwords

    def __repr__(self):
        return f'Слово - {self.word}\nнабор возможных слов:\n{self.subwords}'

    def word_is_right(self, player_input, player):
        if len(player_input) <= 2:
            print('Слишком короткое слово')
            return False
        elif player_input in player.player_words:
            print('Такое слово уже было')
            return False
        elif player_input in self.subwords:
            print('Верно!')
            return True
        else:
            print('Неверно')
            return False

    def get_num_subwords(self):
        return len(self.subwords)

class Player:
    def __init__(self, player_name, player_words=None):
        self.player_name = player_name
        self.player_words = player_words if player_words is not None else []

    def __repr__(self):
        return f'Имя игрока {self.player_name}\nПеречисленные слова:\n{self.player_words}'

    def get_num_player_words(self):
        return len(self.player_words)

    def word_to_player_words(self, word):
        self.player_words.append(word)

def load_random_word(path):
    """
- Получает данные в виде 'json'-файла по передаваемому адресу - path,
- выберет случайное слово,
- создаст экземпляр класса `BasicWord`,
- вернет этот экземпляр.
    """
    try:
        resp = requests.get(path)
        if resp.status_code == 200:
            word_dicts = resp.json()
        else:
            print('Ошибка загрузки данных')
            return None

        if word_dicts:
            random_dict = random.choice(word_dicts)
            return BasicWord(random_dict['word'], random_dict['subwords'])
        else:
            print('Нет данных для обработки')
            return None

    except requests.RequestException as e:
        print(f'Ошибка загрузки данных: {e}')
        return None

def main():
    # Получаем данные для работы
    DATA_SOURCE = 'https://api.npoint.io/0e3ac92f25cd629e3fd4'
    basic_word = load_random_word(DATA_SOURCE)
    if basic_word is None:
        return
    player_name = input('Ввведите имя игрока\n->')
    player = Player(player_name)

    # Начинаем цикл игры
    print(f'Привет, {player_name}!\nСоставьте {basic_word.get_num_subwords()} слов из слова {basic_word.word.upper()}\nСлова должны быть не короче 3 букв\nЧтобы закончить игру, угадайте все слова или напишите "стоп"\nПоехали, ваше первое слово?')
    while True:
        if player.get_num_player_words() < basic_word.get_num_subwords():
            player_input = (input('->')).lower()
            if player_input == 'стоп':
                print('Ну вот и всё!')
                break
            else:
                if basic_word.word_is_right(player_input, player):
                    player.word_to_player_words(player_input)
        else:
            break
    print(f'Игра завершена, вы угадали {player.get_num_player_words()} слов!')

main()
