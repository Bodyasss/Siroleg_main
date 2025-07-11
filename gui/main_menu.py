import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

from constants import ASSETS_PATH, MAIN_MENU_BG
from gui.rules_window import RulesWindow



class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Siroleg Game")
        self.showFullScreen()
        self.setAutoFillBackground(True)
        self.game_window = None
        self.rules_window = None

        self.init_ui()
        self.update_background()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("Siroleg Game")
        self.title_label.setStyleSheet("""
            font-size: 72px; color: white; 
            font-weight: bold; background-color: rgba(0, 0, 0, 0.5);
            padding: 20px; border-radius: 20px;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("Начать игру")
        self.rules_button = QPushButton("Правила")
        self.exit_button = QPushButton("Выход")

        button_style = """
            QPushButton {
                font-size: 32px; color: white; 
                background-color: rgba(0, 85, 170, 0.7);
                border: 2px solid white; border-radius: 15px;
                padding: 15px; min-width: 300px;
            }
            QPushButton:hover { background-color: rgba(0, 85, 170, 0.9); }
        """
        for btn in [self.start_button, self.rules_button, self.exit_button]:
            btn.setStyleSheet(button_style)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.title_label)
        buttons_layout.addSpacing(50)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.rules_button)
        buttons_layout.addWidget(self.exit_button)
        buttons_layout.addStretch()
        buttons_layout.setAlignment(Qt.AlignCenter)

        container = QWidget()
        container.setLayout(buttons_layout)
        container.setMaximumWidth(600)

        self.main_layout.addStretch()
        self.main_layout.addWidget(container)
        self.main_layout.addStretch()

        self.start_button.clicked.connect(self.start_game)
        self.rules_button.clicked.connect(self.show_rules)
        self.exit_button.clicked.connect(self.close)

    def update_background(self):
        palette = QPalette()
        bg_path = os.path.join(ASSETS_PATH, MAIN_MENU_BG)

        if os.path.exists(bg_path):
            pixmap = QPixmap(bg_path)
        else:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.darkBlue)

        scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def start_game(self):
        from gui.card_game import CardGame
        self.game_window = CardGame()
        self.game_window.show()
        self.hide()

    def show_rules(self):
        self.rules_window = RulesWindow(self)
        self.rules_window.show()

    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)