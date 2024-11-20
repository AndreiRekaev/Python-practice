import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor
from brick_game.race.race import Game, user_input, update_current_state, Action, CurrentState

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Race Game")
        self.setGeometry(100, 100, 470, 605)  # Размеры окна совпадают с C++ кодом

        self.game_widget = GameWidget(self)
        self.setCentralWidget(self.game_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_widget.update)
        self.timer.start(20)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Left:
            user_input(Action.LEFT.value, False)
        elif key == Qt.Key.Key_Right:
            user_input(Action.RIGHT.value, False)
        elif key == Qt.Key.Key_Up:
            user_input(Action.UP.value, False)
        elif key == Qt.Key.Key_Down:
            user_input(Action.DOWN.value, False)
        elif key == Qt.Key.Key_P:
            user_input(Action.PAUSE.value, False)
        elif key == Qt.Key.Key_Space:
            user_input(Action.ACTION.value, False)
        elif key == Qt.Key.Key_Escape:
            self.close()

        # Начало игры
        if key == Qt.Key.Key_Enter or key == Qt.Key.Key_Return:
            user_input(Action.START.value, False)


class GameWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(470, 605)  # Установка фиксированного размера виджета
        self.game = Game()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Установка политики фокуса

    def paintEvent(self, event):
        painter = QPainter(self)
        game_state = update_current_state()

        self.draw_field(painter, game_state.field)
        self.draw_next(painter, game_state.next)
        self.draw_info(painter, game_state)

    def draw_field(self, painter, field):
        for i in range(20):
            for j in range(10):
                if field[i][j]:
                    painter.setBrush(QColor(0, 0, 0))
                else:
                    painter.setBrush(QColor(255, 255, 255))
                painter.drawRect(30 * j, 30 * i, 30, 30)

    def draw_next(self, painter, next_piece):
        for i in range(4):
            for j in range(4):
                if next_piece[i][j]:
                    painter.setBrush(QColor(0, 0, 0))
                else:
                    painter.setBrush(QColor(255, 255, 255))
                painter.drawRect(310 + 30 * j, 35 + 30 * i, 30, 30)

    def draw_info(self, painter, game_state):
        painter.drawText(305, 25, "Next:")
        painter.drawText(305, 185, f"Score: {game_state.score}")
        painter.drawText(305, 205, f"High score: {game_state.high_score}")
        painter.drawText(305, 225, f"Level: {game_state.level}")
        painter.drawText(305, 245, f"Speed: {game_state.speed}")
        if game_state.pause:
            painter.drawText(305, 265, "Pause")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
