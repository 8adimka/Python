import os
import json
import random

class Questions:
    def __init__(self, question, answer, difficulty):
        self.question = question
        self.answer = answer
        self.difficulty = int(difficulty)
        self.guess = None
        self.is_right = False

    def build_question(self):
        print(f'Вопрос: {self.question}\nСложность: {self.difficulty}/5')

    def get_points(self):
        return self.difficulty * 10

    def is_correct(self, user_answer):
        self.guess = user_answer
        if self.guess.lower() == self.answer.lower():
            self.is_right = True
            return True
        return False

    def build_positive_feedback(self):
        print(f'Ответ верный, получено {self.get_points()} баллов\n')

    def build_negative_feedback(self):
        print(f'Ответ неверный, верный ответ -> {self.answer}\n')


def load_data_from_file(file_path):
    try:
        with open(file_path) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка в структуре файла.")
        return []

def main():
    file_path = os.path.join ('C:\\', 'Users','m8adi','Desktop','Python','Curs 2.Lecture 3','home_work_lect3.json')  # путь к файлу с вопросами
    quest_list = load_data_from_file(file_path)

    if not quest_list:
        return  # завершение программы, если нет данных

    random.shuffle(quest_list)
    class_list = [Questions(quest[0], quest[1], quest[2]) for quest in quest_list]

    print('Игра начинается!')
    score = 0

    for quest in class_list:
        quest.build_question()
        user_answer = input('Введите ваш ответ:\n-> ')
        if quest.is_correct(user_answer):
            quest.build_positive_feedback()
            score += quest.get_points()
        else:
            quest.build_negative_feedback()

    right_answers = sum(1 for quest in class_list if quest.is_right)

    print(f'Вот и все!\nОтвечено {right_answers} вопроса из {len(class_list)}\nНабрано {score} баллов')

main()

