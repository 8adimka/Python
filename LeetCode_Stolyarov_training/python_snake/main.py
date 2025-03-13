# import keyboard


# def get_key():
#     """Другой вариант — использовать keyboard (сторонняя библиотека, pip install keyboard):"""
#     return keyboard.read_event().name


import sys 
import termios
import threading
import tty
import time
import threading  # Добавляем для работы с потоками


# Размеры поля
WIDTH, HEIGHT = 98, 10

edge = '-'*(WIDTH+2)

class Point:
    def __init__  (self, x= WIDTH // 2, y= HEIGHT // 2, play_ground = [list(' '*WIDTH) for row in range(HEIGHT)]): # Начальная позиция змейки по умолч.
        self.__x = x
        self.__y = y
        self.play_ground = play_ground
    @property
    def y(self):
        return self.__y
    
    @property
    def x(self):
        return self.__x

    def show_head (self):
        self.play_ground[self.__y][self.__x] = "O"

    def hide_head (self):
        self.play_ground[self.__y][self.__x] = ' '
    
    def draw_playground(self):
        # print("\033c", end="")  # Очищаем экран перед рисованием
        sys.stdout.write("\033[H\033[J")  # Очистка экрана (универсальный способ)
        self.show_head()

        print (edge)
        for row in self.play_ground:
            print ('|'+''.join(row)+'|')
        print (edge)

        self.hide_head()

    def move_up (self):
        self.__y -=1

    def move_down (self):
        self.__y +=1

    def move_left (self):
        self.__x -=1

    def move_right (self):
        self.__x +=1

def get_key():
    """Считывает нажатие клавиши (кроссплатформенно)"""
    if sys.platform == "win32": # Проверяем, работает ли код на Windows:
        key = msvcrt.getch() # получает один символ с клавиатуры
        return key.decode("utf-8") if key else None # decode("utf-8") - преобразует bytes в строку (Python3 выдаёт bytes, а нам нужна строка)
            # Иначе считаем, что работаем с Unix-системой
    else:
        fd = sys.stdin.fileno()  # Получаем файловый дескриптор stdin
        old_settings = termios.tcgetattr(fd)  # Сохраняем текущие настройки терминала
        try:
            tty.setraw(fd)  # Переводим терминал в "сырой" режим (raw mode)
            key = sys.stdin.read(1)  # Читаем 1 символ с клавиатуры
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Восстанавливаем настройки терминала
        return key
    
def listen_for_keys():
    """Функция, работающая в отдельном потоке – слушает ввод пользователя"""
    global current_direction, game_on
    while game_on:
        key = get_key()
        if key == 'w':
            current_direction = 'up'
        elif key == 's':
            current_direction = 'down'
        elif key == 'a':
            current_direction = 'left'
        elif key == 'd':
            current_direction = 'right'
        elif key == 'q':  # Выход из игры
            game_on = False
    
def game_loop ():
    global current_direction, game_on
    print("\033c", end="")  # Очищаем экран (работает в большинстве терминалов)

    point = Point()
    # point.draw_playground()

    # Запуск потока для чтения клавиш
    key_listener = threading.Thread(target=listen_for_keys, daemon=True)
    key_listener.start()
    while game_on:
        # Проверяем столкновение с границами
        if point.x < 0 or point.x >= WIDTH or point.y < 0 or point.y >= HEIGHT:
            print("Game Over!")
            game_on = False
            break

        point.draw_playground()

        # Двигаем змейку в текущем направлении
        if current_direction == 'up':
            point.move_up()
        elif current_direction == 'down':
            point.move_down()
        elif current_direction == 'left':
            point.move_left()
        elif current_direction == 'right':
            point.move_right()

        time.sleep(0.2)  # Скорость движения змейки

# Глобальные переменные для управления игрой
current_direction = None
game_on = True  # Флаг работы игры

game_loop()
    




