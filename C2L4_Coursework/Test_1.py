# class Player:
#     def __init__ (self, name, score=0):
#         self.name = name
#         self.score = score

#     def score_up(self):
#         self.score += 1

#     def score_down(self):
#         self.score -= 1

#     def __repr__(self):
#         return f"Player(name={self.name}, score={self.score})"

# player_1 = Player ('Nick')
# print (player_1)
# player_1.score_up()
# print (player_1)
# player_1.score_down()
# print (player_1)



# class WordStorage:
#     def __init__(self, words = None):
#         if words == None:
#             words = []
#         self.words = words

#     def add_word(self, word):
#         self.words.append(word)

#     def remove_word(self, word):
#         if word in self.words:
#             self.words.remove(word)

#     def fetch_words(self):
#         return self.words
    
#     def __repr__(self):
#         if self.words != []:
#             return f'В списке слов есть слежующие слова: {self.words}'
#         return f'В нашем списке слов ничего нет'
    
# word_list = WordStorage ()
# print (word_list)
# word_list.add_word ('Roof')
# word_list.add_word ('Move')
# words = word_list.fetch_words()
# for word in words:
#     print (word)
# word_list.remove_word('Move')
# print (word_list)

# storage = WordStorage()
# print(storage.fetch_words())
# storage.add_word("snake")
# print(storage.fetch_words())
# storage.add_word("bird")
# print(storage.fetch_words())
# storage.remove_word("bird")
# print(storage.fetch_words())



# import random
# class Word:
#     def __init__(self, value):
#         self.value = value

#     def get_value(self):
#         return self.value
    
#     def set_value(self, new_value):
#         self.value = new_value

#     def get_letters(self):
#         list_ = list(self.value)
#         random.shuffle (list_)
#         return ''.join(list_)
    
#     def has_letter(self, letter):
#         if letter in self.value:
#             return True
#         return False  
    
#     def __repr__(self):
#         return f'Внутри слово: {self.value}'

# word_1 = Word ('Карбофос')  
# print (word_1.get_value())
# print (word_1.get_letters())
# print(word_1.has_letter("К"))

# word_1.set_value('Абырвалг')
# print (word_1.get_value())
# print(word_1.has_letter("К"))



# class Lesson:

# 	def __init__(self, lesson_name=""):
# 		self.name = lesson_name

# 	def __repr__(self):
# 		return f"Lesson('{self.name}')"
	
# lessons_titles = [
# 	"Архитектура ЭВМ", 
# 	"Дискретная математика", 
# 	"Алгоритмы", 
# 	"Компьютерные сети"
# 	]

# lessons_list = [Lesson(lesson) for lesson in lessons_titles]

# for lesson in lessons_list:
# 	print (lesson)



# class Product:

#   def __init__(self, name="", category="", price=0):
#     self.name = name
#     self.category = category
#     self.price = price

#   def __repr__(self):
#     return f"Product('{self.name}', '{self.category}', {self.price})"

# products_data = [  
#   {"name": "Вафельки", "category": "sweets", "price": 150},
#   {"name": "Яблоки", "category": "fruits", "price": 100},
#   {"name": "Минералка", "category": "drinks", "price": 200},
# ]	

# products_data_list = [Product(name=product["name"], category=product['category'], price=product['price']) for product in products_data]

# for product in products_data_list:
#     print (product)



# import json
# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 4Coursework\words.json', 'w') as file:
#     json.dump (["owl", "cat", "dog"], file)

# class Word:
#     def __init__(self, value):
#         self.value = value

#     def __repr__(self):
#         return f'Внутри слово: {self.value}'
    
# def load_words (file_path):
#     with open (file_path) as file:
#         words = json.load (file)
#     return [Word(word) for word in words]
    
# words = load_words (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 4Coursework\words.json')

# for word in words:
#     print (word)
    


# import json
# class BasicWord:
#     def __init__(self, word, subwords):
#         self.word=word
#         self.subwords=subwords

#     def __repr__(self):
#         return f'Внутри слово {self.word} и подстрока - {self.subwords}'

# def data_to_basic_word (file_path):
#     with open (file_path, 'r', encoding='utf-8') as file:
#         data_dict = json.load (file)
#         return BasicWord (data_dict['word'], data_dict["subwords"])
    
# basic_w1 = data_to_basic_word (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 4Coursework\data.json')
# print (basic_w1)



# import random
# import json
# import os
# class WordManager:
#     def __init__(self, words):
#         self.words=words

#     def get_random_word(self):
#         if self.words:
#             return random.choice(self.words)
#         return None

# def create_word_manager_from_json(path):
#     try:
#         with open (path, 'r', encoding= 'utf-8') as file:
#             word_list = json.load (file)
#         return WordManager(word_list)
#     except (FileNotFoundError, json.JSONDecodeError) as e:
#         print(f"Error reading file: {e}")
#         return None

# word_manager = create_word_manager_from_json (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 4Coursework\data2.json')
# print (word_manager.get_random_word())



class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"Player(name={self.name}, score={self.score})"

    def get_score(self):
        return self.score
    
# # pl_1 = Player('Alex', 700)
# # pl_2 = Player('Mary', 950)
# # pl_3 = Player('Ann', 890)
# # players = [pl_1,pl_2,pl_3]

# # def total_score (players):
# #     return sum ([pl.score for pl in players])

# # scores = total_score (players)
# # print (scores)

# # def avg_score (players):
# #     return sum ([pl.score for pl in players])/len (players)

# # avg_scores = round (avg_score (players), 1)
# # print (avg_scores)

# def get_leader (players):
#     max_score = max([pl.score for pl in players])
#     for pl in players:
#         if pl.score == max_score:
#             return pl

# # print (get_leader (players))

# def get_player_scored_over (players, value):
#     return [pl for pl in players if pl.score >= value]

# leaders_list = get_player_scored_over (players, 890)
# for leader in leaders_list:
#     print (leader)

import requests
resp = requests.get('https://api.npoint.io/0e3ac92f25cd629e3fd4')

if resp.status_code == 200:
    players = resp.json()
    class_list = [Player(**player) for player in players]
else:
    print ('"Ошибка при загрузке данных"')

total_score = sum ([pl.score for pl in class_list])
print (total_score)


# class Coin:

#     def __init__(self, value=0):
#         self.value = value

#     def __repr__(self):
#         return f"Coin({self.value})"

# coins = [
#    Coin(10), Coin(20), Coin(25), Coin(50), Coin(25), Coin(50), Coin(100)
# ]

# def get_coins_over (coins, value):
#     return [coin for coin in coins if coin.value > value]

# print (get_coins_over (coins, 20))



# class Product:

#   def __init__(self, name="", category="", price=0):
#     self.name = name
#     self.category = category
#     self.price = price

#   def __repr__(self):
#     return f"Product({self.name}, {self.category}, {self.price})"

# product_data = [  
#   {"name": "Вафельки", "category": "sweets", "price": 150},
#   {"name": "Яблоки", "category": "fruits", "price": 100},
#   {"name": "Апельсины", "category": "fruits", "price": 150},
#   {"name": "Гранаты", "category": "fruits", "price": 350},
#   {"name": "Минералка", "category": "drinks", "price": 200},
# ]
# products = [Product(**item) for item in product_data]
# #Идентичная запись **
# products = [Product(name = item['name'], category = item['category'], price = item['price']) for item in product_data]

# products_fruit = [product for product in products if product.category == 'fruits']
# print (products_fruit)

# lower_price = [product for product in products if product.price < 200]
# higher_proce = [product for product in products if product.price >= 200]
# print (f'{lower_price}\n{higher_proce}')



# import requests
# import random

# class Lessons:
#     def __init__(self, lesson_name=""):
#         self.lesson_name=lesson_name
#     def __repr__(self):
#         return f"Lesson('{self.lesson_name}')"

# response = requests.get ('https://api.npoint.io/0e3ac92f25cd629e3fd4')

# if response.status_code == 200:
#     lesson_list = response.json()
#     print (type(lesson_list))
#     lessons = [Lessons(lesson) for lesson in lesson_list]
#     print (random.choice(lessons))
# else:
#     print ('"Ошибка при загрузке данных"')



# class A:
#     def greet(self):
#         print("Hello from A")

# class B(A):
#     def greet(self):
#         super().greet()  # Вызов метода родительского класса
#         print("Hello from B")

# cb = B()

# cb.greet()

# class R:
#     def __init__(cls):
#         pass



d = {1: "one", 2: "two", 3: "three", 4: "four"}
filtered_d = {k: v for k, v in d.items() if len(v) == 3}
print(filtered_d)  # вывод: {1: 'one', 2: 'two'}
