import win32con
import win32gui
import win32api

def draw_crosshair(hdc, width, height):
    # Красный прицел с зеленой обводкой для лучшей видимости
    pen_red = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(255, 0, 0))
    pen_green = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(0, 255, 0))
    size = 10
    
    # Сначала рисуем зеленую обводку
    old_pen = win32gui.SelectObject(hdc, pen_green)
    center_x = width // 2
    center_y = height // 2
    
    # Горизонтальная линия (обводка)
    win32gui.MoveToEx(hdc, center_x - size - 1, center_y)
    win32gui.LineTo(hdc, center_x + size + 1, center_y)
    # Вертикальная линия (обводка)
    win32gui.MoveToEx(hdc, center_x, center_y - size - 1)
    win32gui.LineTo(hdc, center_x, center_y + size + 1)
    
    # Затем рисуем красный прицел поверх
    win32gui.SelectObject(hdc, pen_red)
    # Горизонтальная линия
    win32gui.MoveToEx(hdc, center_x - size, center_y)
    win32gui.LineTo(hdc, center_x + size, center_y)
    # Вертикальная линия
    win32gui.MoveToEx(hdc, center_x, center_y - size)
    win32gui.LineTo(hdc, center_x, center_y + size)
    
    # Восстанавливаем старое перо
    win32gui.SelectObject(hdc, old_pen)
    win32gui.DeleteObject(pen_red)
    win32gui.DeleteObject(pen_green)

def wndProc(hwnd, msg, wParam, lParam):
    if msg == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hwnd)
        rect = win32gui.GetClientRect(hwnd)
        draw_crosshair(hdc, rect[2], rect[3])
        win32gui.EndPaint(hwnd, paintStruct)
        return 0
    elif msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

def main():
    className = "CrosshairOverlay"
    hInstance = win32api.GetModuleHandle(None)
    
    # Регистрируем класс окна
    wndClass = win32gui.WNDCLASS()
    wndClass.hInstance = hInstance
    wndClass.lpszClassName = className
    wndClass.lpfnWndProc = wndProc
    wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wndClass.hbrBackground = win32gui.GetStockObject(win32con.HOLLOW_BRUSH)  # Прозрачный фон
    
    win32gui.RegisterClass(wndClass)
    
    # Создаем окно
    hwnd = win32gui.CreateWindowEx(
        win32con.WS_EX_LAYERED | 
        win32con.WS_EX_TRANSPARENT |
        win32con.WS_EX_TOPMOST |
        win32con.WS_EX_TOOLWINDOW,
        className,
        "Crosshair Overlay",
        win32con.WS_POPUP,
        0, 0, 
        win32api.GetSystemMetrics(win32con.SM_CXSCREEN),
        win32api.GetSystemMetrics(win32con.SM_CYSCREEN),
        None, None, hInstance, None
    )
    
    # Делаем окно прозрачным (все пиксели кроме прицела)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_COLORKEY)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    
    # Цикл сообщений
    while True:
        msg = win32gui.GetMessage(None, 0, 0)
        if msg[0] == 0: break
        win32gui.TranslateMessage(msg[1])
        win32gui.DispatchMessage(msg[1])

if __name__ == '__main__':
    main()
