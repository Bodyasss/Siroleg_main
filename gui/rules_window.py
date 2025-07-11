import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

from constants import ASSETS_PATH, RULES_BG


class RulesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Правила игры")
        self.resize(800, 600)
        self.setAutoFillBackground(True)
        self.parent = parent

        self.init_ui()
        self.update_background()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Правила игры")
        title_label.setStyleSheet("""
            font-size: 36px; color: white; font-weight: bold;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 15px; border-radius: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)

        rules_text = """
        <h2>Основные правила:</h2>
        <p>1. В начале игры вы получаете 2 случайных предмета.</p>
        <p>2. Нажмите "Выбить дверь", чтобы встретиться с монстром.</p>
        <p>3. Ваша сила = ваш уровень + бонусы от экипировки.</p>
        <p>4. Если ваша сила ≥ уровня монстра - вы побеждаете:</p>
        <ul>
            <li>Ваш уровень увеличивается на награду монстра</li>
            <li>Вы получаете право взять столько сокровищ, сколько указано в награде</li>
        </ul>
        <p>5. Если ваша сила < уровня монстра - вы проигрываете:</p>
        <ul>
            <li>Ваш уровень уменьшается на штраф монстра</li>
            <li>Если уровень падает ниже 1 - игра заканчивается</li>
        </ul>
        <h2>Экипировка:</h2>
        <p>- Можно экипировать предметы из инвентаря (клик по карте)</p>
        <p>- Двуручное оружие занимает один слот</p>
        <p>- Максимум 8 предметов в инвентаре</p>
        <h2>Цель игры:</h2>
        <p>Достичь 10 уровня!</p>
        """
        rules_label = QLabel(rules_text)
        rules_label.setStyleSheet("""
            font-size: 16px; color: white; background-color: rgba(0, 0, 0, 0.5);
            padding: 20px; border-radius: 10px;
        """)
        rules_label.setWordWrap(True)

        self.back_button = QPushButton("Вернуться в меню")
        button_style = """
            QPushButton {
                font-size: 18px; color: white; background-color: rgba(0, 85, 170, 0.7);
                border: 2px solid white; border-radius: 10px;
                padding: 10px; min-width: 200px;
            }
            QPushButton:hover { background-color: rgba(0, 85, 170, 0.9); }
        """
        self.back_button.setStyleSheet(button_style)
        self.back_button.clicked.connect(self.close)

        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(rules_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

    def update_background(self):
        palette = QPalette()
        bg_path = os.path.join(ASSETS_PATH, RULES_BG)

        if os.path.exists(bg_path):
            pixmap = QPixmap(bg_path)
        else:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.darkGreen)

        scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def closeEvent(self, event):
        if self.parent:
            self.parent.show()
        event.accept()

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)