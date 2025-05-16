import ctypes
import time

# Константы Windows API
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_POPUP = 0x80000000
ULW_COLORKEY = 0x00000001

# Настройки прицела
CROSSHAIR_COLOR = 0x0000FF  # Красный (BGR)
CROSSHAIR_SIZE = 20
CROSSHAIR_WIDTH = 2

# Получаем дескрипторы Windows API
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

def draw_crosshair():
    # Получаем размеры экрана
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Создаём прозрачное окно
    hwnd = user32.CreateWindowExW(
        WS_EX_LAYERED | WS_EX_TRANSPARENT,
        "STATIC",  # Простейший класс окна
        None,
        WS_POPUP,
        0, 0, screen_width, screen_height,
        None, None, None, None
    )

    # Устанавливаем окно поверх всех
    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

    # Получаем контекст устройства
    hdc = user32.GetDC(hwnd)
    
    # Создаём перо для рисования круга
    pen = gdi32.CreatePen(0, CROSSHAIR_WIDTH, CROSSHAIR_COLOR)
    old_pen = gdi32.SelectObject(hdc, pen)

    # Рисуем круг в центре экрана
    center_x = screen_width // 2
    center_y = screen_height // 2
    gdi32.Ellipse(hdc, 
        center_x - CROSSHAIR_SIZE, 
        center_y - CROSSHAIR_SIZE, 
        center_x + CROSSHAIR_SIZE, 
        center_y + CROSSHAIR_SIZE
    )

    # Освобождаем ресурсы
    gdi32.SelectObject(hdc, old_pen)
    gdi32.DeleteObject(pen)
    user32.ReleaseDC(hwnd, hdc)

    # Оставляем окно открытым
    while True:
        time.sleep(1)

if __name__ == "__main__":
    draw_crosshair()
    