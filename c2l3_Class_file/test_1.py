# class Fish:
#     def swim (self):
#         print ('Я плаваю')

# class Girl:
#     def __init__ (self, fname, sname):
#         self.fname = fname
#         self.sname = sname

#     def sing (self):
#         print (f'Я {self.fname} {self.sname} и я пою')

# class Mermaid (Fish, Girl):
#     pass

# ariel = Mermaid ('Ариель', 'Батьковна')
# ariel.swim()
# ariel.sing()



# class Bottle:
#     def __init__(self, color, volume):
#         self.volume = float (volume)
#         self.color = color

#     def ptint_about (self):
#         print (self.color, self.volume)

# red_bottle = Bottle ('Красную', 0.7)
# white_bottle = Bottle ('Белую', 0.3)
# black_bottle = Bottle ('Черную ', '1.0')

# red_bottle.ptint_about()
# white_bottle.ptint_about()
# black_bottle.ptint_about()



# class Students:
#     def __init__(self, name, course):
#         self.name = name
#         self.course = int(course)
    
#     def print_about_student (self):
#         print (f'{self.name}, {self.course}[курс]')

# student_1 = Students ('Алиса' , 3)
# student_2 = Students ('Маргарита', 2)

# student_1.print_about_student()
# print (student_2.name, student_2.course)



# class Album:
#     def __init__(self, artist, title, tracks):
#         self.artist = artist
#         self.title = title
#         self.tracks = list (tracks)

#     def print_about_me (self):
#         print (f'''
# Исполнитель: {self.artist}
# Название: {self.title}
# Треки: {', '.join (self.tracks)}
# Всего: {len(self.tracks)} треков\n''')

# artist_1 = Album ('Queen', 'Killer Queen', ['Brighton rock', 'Killer Queen', 'Tenement Funster'])
# artist_1.print_about_me()

# artist_2 = Album ('Metallica','Black Album', ['Enter Sandman', 'Sad But True', 'Holier Than Thou'])
# print (artist_2.artist, '\n'+artist_2.title, '\n'+f"{', '.join(artist_2.tracks)}", f'\n{len(artist_2.tracks)} треков')



# class Bottle:
#     def __init__ (self, color, contains=0):
#         self.contains = contains
#         self.color = color

#     def get_content (self):
#         return self.contains
    
#     def fill (self, volume):
#         self.contains += volume

# bottle_1 = Bottle ('Красная')
# bottle_2 = Bottle ('Синяя')

# print(bottle_1.color, bottle_1.get_content())
# bottle_1.fill(100)
# print(bottle_1.color, bottle_1.get_content())

# print(bottle_2.color, bottle_2.get_content())
# bottle_2.fill(500)
# print(bottle_2.color, bottle_2.get_content())



# class TodoList:
#     def __init__(self, tasks=[]):
#         self.tasks = tasks

#     def add_task (self, name_task):
#         self.tasks.append(name_task)

# todo_list_1 = TodoList(['Купить лампочку', 'Поменять лампочку'])
# todo_list_1.add_task('Выкинуть лампочку')
# print (', '.join (todo_list_1.tasks))

# todo_list_2 = TodoList()
# todo_list_2.add_task ('Купить лампочку')
# todo_list_2.add_task ('Выключить свет')
# todo_list_2.add_task ('Поменять лампочку')
# todo_list_2.add_task ('Выкинуть лампочку')
# print (', '.join (todo_list_2.tasks))



# class Player:
#     def __init__(self, name, score=0):
#         self.name = name
#         self.score = score

#     def get_score (self):
#         return self.score
    
#     def set_score (self, score):
#         self.score = int (score)

# player_1 = Player ('Алиса')
# print(player_1.name, player_1.get_score()) 
# player_1.set_score(200)
# print(player_1.name, player_1.get_score()) 
# player_1.set_score(500) 
# print(player_1.name, player_1.get_score())



# class Number:
#     def __init__(self, value):
#         self.value = value

#     def add (self, num):
#         self.value += int (num)

#     def subtract (self, num):
#         self.value -= int (num)

#     def get (self):
#         return self.value
    
# n = Number(7)
# print(n.get())
# n.add(3)
# print(n.get())
# n.subtract(5)
# print(n.get())



# import math
# class Circle:
#     def __init__(self, radius):
#         self.radius = radius

#     def get_radius (self):
#         return self.radius

#     def get_diameter (self):
#         return self.radius*2

#     def get_perimeter (self):
#         return self.radius*2*math.pi

# circle_1 = Circle(7)
# print("радиус", circle_1.get_radius() )
# print("диаметр", circle_1.get_diameter() )
# print("периметр", round(circle_1.get_perimeter(),1))



# class Square:
#     def __init__ (self, side_length, color='white'):
#         self.side_length = side_length
#         self.color = color

#     def set_side(self, length):
#         self.side_length = length

#     def set_color(self, color):
#         self.color = color

#     def get_side(self):
#         return self.side_length

#     def get_color(self):
#         return self.color
    
#     def get_perimeter (self):
#         return self.side_length*4

# square_1 = Square(2)
# print(square_1.get_side())
# print(square_1.get_perimeter())
# print(square_1.get_color())
# print("---")
# square_1.set_side(3)
# square_1.set_color("red")
# print(square_1.get_side())
# print(square_1.get_perimeter())
# print(square_1.get_color())
# print("---")
# square_1 = Square(1, "black")
# print(square_1.get_side())
# print(square_1.get_perimeter())
# print(square_1.get_color())



# class Room:

#     def __init__(self, number, is_free):
#         self.number = number
#         self.is_free = is_free


# def get_free_rooms(rooms):
#     free_rooms = [room for room in rooms if room.is_free]

#     return free_rooms


# rooms = [Room(14, True), Room(15, False), Room(16, True)]
# room_1 = Room(1, True)
# rooms_free = get_free_rooms(rooms)

# # Не удаляйте этот код, он нужен для проверки

# [print(r.number) for r in rooms if r.is_free]
# print (room_1.number, room_1.is_free)




# class Room:
#     def __init__ (self, number, type, price):
#         self.number = number
#         self.type = type
#         self.price = price

# rooms = {12: Room(12, 'standard', 2000), 13: Room(13, 'standard', 2000), 14: Room(14, 'joint', 2500), 15: Room(15, 'suite', 3000)}

# user_input = int(input('Введите номер номера:\n->'))
# room = rooms [user_input]
# print (f'''Номер: {room.number}
# Тип номера: {room.type}
# Цена за сутки: {room.price}''')



class Bottle:
    def __init__ (self, color, volume):
        self.color = color
        self.volume = volume

    def get_color(self):
        return self.color

    def get_volume(self):
        return self.volume

class Shelve:
    def __init__(self, bottles=[]):
        self.bottles = bottles

    def add_bottle(self, bottle):
        self.bottles.append(bottle)

    def get_number_of_bottles(self):
        return len(self.bottles)

bottle_1= Bottle('Red', 0.7)
bottle_2= Bottle('Green', 0.3)
bottle_3= Bottle('White', 0.5)

shelve_1= Shelve()
shelve_1.add_bottle(bottle_1)
shelve_1.add_bottle(bottle_2)
shelve_1.add_bottle(bottle_3)

for bottle in shelve_1.bottles:
    print (bottle.color, bottle.get_volume())
