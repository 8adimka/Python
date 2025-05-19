import ctypes
import time
from ctypes import wintypes

# Константы Windows API
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
WS_POPUP = 0x80000000
ULW_ALPHA = 0x00000002

# Настройки прицела
CROSSHAIR_COLOR = 0x0000FF  # Красный (BGR)
CROSSHAIR_SIZE = 20
CROSSHAIR_WIDTH = 2

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ("BlendOp", ctypes.c_byte),
        ("BlendFlags", ctypes.c_byte),
        ("SourceConstantAlpha", ctypes.c_byte),
        ("AlphaFormat", ctypes.c_byte)
    ]

def draw_crosshair():
    # Получаем дескриптор рабочего стола
    hwnd = user32.GetDesktopWindow()
    hdc = user32.GetDC(hwnd)
    
    # Получаем размеры экрана
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    # Создаём буфер для рисования
    hdc_buffer = gdi32.CreateCompatibleDC(hdc)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc, screen_width, screen_height)
    gdi32.SelectObject(hdc_buffer, hbitmap)
    
    # Заливаем прозрачным цветом
    gdi32.PatBlt(hdc_buffer, 0, 0, screen_width, screen_height, 0x00FFFFFF)
    
    # Рисуем круг
    pen = gdi32.CreatePen(0, CROSSHAIR_WIDTH, CROSSHAIR_COLOR)
    old_pen = gdi32.SelectObject(hdc_buffer, pen)
    
    center_x = screen_width // 2
    center_y = screen_height // 2
    gdi32.Ellipse(hdc_buffer, 
        center_x - CROSSHAIR_SIZE, 
        center_y - CROSSHAIR_SIZE, 
        center_x + CROSSHAIR_SIZE, 
        center_y + CROSSHAIR_SIZE
    )
    
    # Создаём прозрачное окно
    hwnd = user32.CreateWindowExW(
        WS_EX_LAYERED | WS_EX_TRANSPARENT,
        "Static",
        None,
        WS_POPUP,
        0, 0, screen_width, screen_height,
        None, None, None, None
    )
    
    # Настраиваем прозрачность
    blend = BLENDFUNCTION()
    blend.BlendOp = 0
    blend.BlendFlags = 0
    blend.SourceConstantAlpha = 255
    blend.AlphaFormat = 1  # AC_SRC_ALPHA
    
    # Обновляем окно
    user32.UpdateLayeredWindow(
        hwnd, hdc,
        ctypes.byref(wintypes.POINT(0, 0)),
        ctypes.byref(wintypes.SIZE(screen_width, screen_height)),
        hdc_buffer,
        ctypes.byref(wintypes.POINT(0, 0)),
        0,
        ctypes.byref(blend),
        ULW_ALPHA
    )
    
    # Устанавливаем окно поверх всех
    user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    
    # Освобождаем ресурсы
    gdi32.SelectObject(hdc_buffer, old_pen)
    gdi32.DeleteObject(pen)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(hdc_buffer)
    user32.ReleaseDC(hwnd, hdc)
    
    # Оставляем окно открытым
    print("Прицел активен. Нажмите ESC для выхода.")
    while True:
        if user32.GetAsyncKeyState(0x1B) & 0x8000:  # ESC для выхода
            break
        time.sleep(0.1)
    
    # Закрываем окно при выходе
    user32.DestroyWindow(hwnd)

if __name__ == "__main__":
    draw_crosshair()
    