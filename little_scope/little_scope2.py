import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen

class Crosshair(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.X11BypassWindowManagerHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 3)  # Красная точка
        painter.setPen(pen)

        center_x = self.width() // 2
        center_y = self.height() // 2

        # Нарисовать маленький крест
        painter.drawLine(center_x - 5, center_y, center_x + 5, center_y)
        painter.drawLine(center_x, center_y - 5, center_x, center_y + 5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    crosshair = Crosshair()
    sys.exit(app.exec_())
    