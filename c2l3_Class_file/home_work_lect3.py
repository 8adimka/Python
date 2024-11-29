import os
import json
import random

class Questions:
    def __init__(self, question, answer, difficulty, is_right = False):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.is_right = is_right

    def build_question (self):
        print (f'Вопрос: {self.question}\nСложность: {self.difficulty}/5')
    
    def get_points (self):
        return self.difficulty*10
    
    def is_correct (self, guess):
        if guess.lower() == self.answer.lower():
            return True
        return False
    
    def build_positive_feedback(self):
        print (f'Ответ верный, получено {self.get_points()} баллов\n')
        self.is_right = True

    def build_negative_feedback(self):
        print(f'Ответ неверный, верный ответ -> {self.answer}\n')

questions = (('Which planet is known as the Red Planet?', 'Mars', 2),
             ('How many years are there in a century?', '100', 1),
             ('How many strings does a violin have?', '4', 4),
             ('What do people often call American flag?','stars and stripes',4),
             ('How many years are there in one Millennium?','1000',2),
             ('How many days do we have in a week?','7',1),
             ('How many letters are there in the English alphabet?','26',3),
             ('How many sides are there in a triangle?','3',1),
             ('How many sides does hexagon have?','6',4),
             ('Which planet is closest to the sun?','Mercury',4))

file_path = os.path.join ('C:\\', 'Users','m8adi','Desktop','Python','Curs 2.Lecture 3','home_work_lect3.json')
def corvert_data_to_file (data):
    with open (file_path, 'w') as file:
        json.dump(data, file)
corvert_data_to_file (questions)

def load_data_from_file ():
    with open (file_path) as file:
        return json.load(file)

def main ():
    quest_list = load_data_from_file()
    random.shuffle(quest_list)
    class_list = [Questions(quest[0], quest[1], quest[2]) for quest in quest_list]

    print ('Игра начинается!\n')
    score = 0
    for quest in class_list:
        quest.build_question()
        user_guess = input('Введите ваш ответ:\n->')
        if quest.is_correct(user_guess):
            quest.build_positive_feedback()
            score += quest.get_points()
        else:
            quest.build_negative_feedback()

    right_answers  = sum(1 for question in class_list if question.is_right)

    print (f'Вот и все!\nОтвечено {right_answers} вопроса из {len(class_list)}\nНабранно {score} баллов')

main()
