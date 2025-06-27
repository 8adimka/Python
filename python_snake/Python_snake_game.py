import time
import random
import curses

# Размеры поля
WIDTH, HEIGHT = 75, 22

edge = '-' * (WIDTH + 2)

class Point:
    def __init__(self, x=WIDTH // 2, y=HEIGHT // 2):  # Начальная позиция змейки по умолч.
        self.__x = x
        self.__y = y
        self.play_ground = [list(' ' * WIDTH) for _ in range(HEIGHT)]
        self.tail = []  # Хвост змейки
        self.food = self.generate_food()  # Еда на поле

    def generate_food(self):
        """Генерация еды в случайном месте на поле."""
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if (x, y) != (self.__x, self.__y) and (x, y) not in self.tail:
                return (x, y)

    @property
    def y(self):
        return self.__y

    @property
    def x(self):
        return self.__x

    def show_head(self):
        self.play_ground[self.__y][self.__x] = "O"

    def hide_head(self):
        self.play_ground[self.__y][self.__x] = ' '

    def draw_playground(self, stdscr):
        """Отрисовка игрового поля с использованием curses."""
        stdscr.clear()

        # Отрисовка еды
        fx, fy = self.food
        stdscr.addch(fy + 1, fx + 1, 'x')  # +1 для учета границ поля

        # Отрисовка хвоста
        for segment in self.tail:
            tx, ty = segment
            stdscr.addch(ty + 1, tx + 1, 'o')

        # Отрисовка головы
        stdscr.addch(self.__y + 1, self.__x + 1, 'O')

        # Отрисовка границ поля
        stdscr.addstr(0, 0, edge)
        for i in range(1, HEIGHT + 1):
            stdscr.addstr(i, 0, '|')
            stdscr.addstr(i, WIDTH + 1, '|')
        stdscr.addstr(HEIGHT + 1, 0, edge)

        stdscr.refresh()

    def move_up(self):
        self.__y -= 1

    def move_down(self):
        self.__y += 1

    def move_left(self):
        self.__x -= 1

    def move_right(self):
        self.__x += 1

    def check_collision(self):
        """Проверка столкновений с хвостом или границами поля."""
        # Проверка столкновения с хвостом
        if (self.__x, self.__y) in self.tail:
            return True

        # Проверка столкновения с границами поля
        if self.__x < 0 or self.__x >= WIDTH or self.__y < 0 or self.__y >= HEIGHT:
            return True

        return False

    def check_food(self):
        """Проверка, съела ли змейка еду."""
        if (self.__x, self.__y) == self.food:
            # # Добавляем новый сегмент хвоста в начало (позиция головы до движения)
            # self.tail.insert(0, (self.__x, self.__y))
            self.food = self.generate_food()  # Генерируем новую еду
            return True  # Еда съедена
        return False  # Еда не съедена

def game_loop(stdscr):
    curses.curs_set(0)  # Скрываем курсор
    stdscr.nodelay(1)  # Неблокирующий ввод
    stdscr.timeout(300)  # Таймаут для getch (в миллисекундах)

    game_state = {'current_direction': None, 'game_on': True}

    point = Point()

    while game_state['game_on']:
        # Считываем клавишу
        key = stdscr.getch()
        if key == curses.KEY_UP:
            game_state['current_direction'] = 'up'
        elif key == curses.KEY_DOWN:
            game_state['current_direction'] = 'down'
        elif key == curses.KEY_LEFT:
            game_state['current_direction'] = 'left'
        elif key == curses.KEY_RIGHT:
            game_state['current_direction'] = 'right'
        elif key == ord('q'):
            game_state['game_on'] = False
            break

        # Сохраняем текущую позицию головы
        prev_x, prev_y = point.x, point.y

        # Двигаем змейку в текущем направлении
        if game_state['current_direction'] == 'up':
            point.move_up()
        elif game_state['current_direction'] == 'down':
            point.move_down()
        elif game_state['current_direction'] == 'left':
            point.move_left()
        elif game_state['current_direction'] == 'right':
            point.move_right()

        # Проверяем столкновение с хвостом или границами поля
        if point.check_collision():
            stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, "Game Over!")
            stdscr.refresh()
            time.sleep(2)
            game_state['game_on'] = False
            break

        # Проверяем, съела ли змейка еду
        ate_food = point.check_food()

        # Обновляем хвост
        if game_state['current_direction']:  # Если направление задано
            # Добавляем предыдущую позицию головы в хвост
            point.tail.insert(0, (prev_x, prev_y))
            if not ate_food:  # Если еда не съедена, удаляем последний сегмент
                point.tail.pop()

        point.draw_playground(stdscr)

if __name__ == "__main__":
    curses.wrapper(game_loop)  # Используем curses для корректной работы с терминалом

