import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt

from constants import ASSETS_PATH, VICTORY_BG, DEFEAT_BG


class ResultWindow(QWidget):
    def __init__(self, parent=None, victory=False, game_completed=False):
        super().__init__(parent)
        self.parent = parent
        self.victory = victory
        self.game_completed = game_completed
        self.setWindowTitle("Победа!" if victory else "Поражение")
        self.setFixedSize(600, 400)
        self.setAutoFillBackground(True)
        self.bg_image = VICTORY_BG if victory else DEFEAT_BG
        self.init_ui()
        self.update_background()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        title = QLabel("ПОБЕДА!" if self.victory else "ПОРАЖЕНИЕ")
        title.setStyleSheet("""
            font-size: 48px; font-weight: bold; color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px; border-radius: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)

        if self.game_completed:
            message = "Вы полностью прошли игру! Поздравляем!"
        elif self.victory:
            message = "Вы победили монстра и стали сильнее!"
        else:
            message = "Вы проиграли в схватке с монстром..."

        msg_label = QLabel(message)
        msg_label.setStyleSheet("""
            font-size: 20px; color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 15px; border-radius: 10px;
        """)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignCenter)

        buttons_layout = QHBoxLayout()

        if self.game_completed or not self.victory:
            new_game_btn = QPushButton("Новая игра")
            new_game_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px; color: white; background-color: rgba(0, 170, 0, 0.7);
                    border: 2px solid white; border-radius: 10px; padding: 10px;
                }
                QPushButton:hover { background-color: rgba(0, 170, 0, 0.9); }
            """)
            new_game_btn.clicked.connect(self.new_game)
            buttons_layout.addWidget(new_game_btn)

        if self.victory and not self.game_completed:
            continue_btn = QPushButton("Продолжить")
            continue_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px; color: white; background-color: rgba(0, 170, 0, 0.7);
                    border: 2px solid white; border-radius: 10px; padding: 10px;
                }
                QPushButton:hover { background-color: rgba(0, 170, 0, 0.9); }
            """)
            continue_btn.clicked.connect(self.continue_game)
            buttons_layout.addWidget(continue_btn)

        exit_btn = QPushButton("Выйти")
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; color: white; background-color: rgba(170, 0, 0, 0.7);
                border: 2px solid white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: rgba(170, 0, 0, 0.9); }
        """)
        exit_btn.clicked.connect(self.exit_game)
        buttons_layout.addWidget(exit_btn)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(msg_label)
        self.main_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)

    def update_background(self):
        palette = QPalette()
        bg_path = os.path.join(ASSETS_PATH, self.bg_image)
        if os.path.exists(bg_path):
            pixmap = QPixmap(bg_path)
        else:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.darkRed if not self.victory else Qt.darkGreen)

        scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def new_game(self):
        if self.parent:
            self.parent.restart_game()
        self.close()

    def continue_game(self):
        self.close()

    def exit_game(self):
        if self.parent:
            self.parent.close()
        self.close()


class VictoryWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Победа!")
        self.setFixedSize(500, 300)
        self.setAutoFillBackground(True)
        self.init_ui()
        self.update_background()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        title = QLabel("ПОЗДРАВЛЯЕМ!")
        title.setStyleSheet("""
            font-size: 36px; font-weight: bold; color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px; border-radius: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)

        msg_label = QLabel("Вы достигли 10 уровня и победили в игре!")
        msg_label.setStyleSheet("""
            font-size: 20px; color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 15px; border-radius: 10px;
        """)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignCenter)

        buttons_layout = QHBoxLayout()

        new_game_btn = QPushButton("Новая игра")
        new_game_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; color: white; background-color: rgba(0, 170, 0, 0.7);
                border: 2px solid white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: rgba(0, 170, 0, 0.9); }
        """)
        new_game_btn.clicked.connect(self.new_game)
        buttons_layout.addWidget(new_game_btn)

        exit_btn = QPushButton("Выйти")
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; color: white; background-color: rgba(170, 0, 0, 0.7);
                border: 2px solid white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: rgba(170, 0, 0, 0.9); }
        """)
        exit_btn.clicked.connect(self.exit_game)
        buttons_layout.addWidget(exit_btn)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(msg_label)
        self.main_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)

    def update_background(self):
        palette = QPalette()
        bg_path = os.path.join(ASSETS_PATH, VICTORY_BG)
        if os.path.exists(bg_path):
            pixmap = QPixmap(bg_path)
        else:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.darkGreen)

        scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def new_game(self):
        if self.parent:
            self.parent.restart_game()
        self.close()

    def exit_game(self):
        if self.parent:
            self.parent.close()
        self.close()


class DefeatWindow(QWidget):
    def __init__(self, parent=None, monster_name="", level_lost=0, game_over=False):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Поражение")
        self.setFixedSize(500, 300)
        self.setAutoFillBackground(True)
        self.init_ui(monster_name, level_lost, game_over)
        self.update_background()

    def init_ui(self, monster_name, level_lost, game_over):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        if game_over:
            title = QLabel("ИГРА ОКОНЧЕНА")
            message = f"Вы проиграли в схватке с {monster_name}!\nВаш уровень упал ниже 1."
        else:
            title = QLabel("ПОРАЖЕНИЕ")
            message = f"{monster_name} победил вас!\nВы теряете {level_lost} уровней."

        title.setStyleSheet("""
            font-size: 36px; font-weight: bold; color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px; border-radius: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)

        msg_label = QLabel(message)
        msg_label.setStyleSheet("""
            font-size: 20px; color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 15px; border-radius: 10px;
        """)
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignCenter)

        buttons_layout = QHBoxLayout()

        new_game_btn = QPushButton("Новая игра")
        new_game_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; color: white; background-color: rgba(0, 170, 0, 0.7);
                border: 2px solid white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: rgba(0, 170, 0, 0.9); }
        """)
        new_game_btn.clicked.connect(self.new_game)
        buttons_layout.addWidget(new_game_btn)

        # If the game is not over, allow the player to continue.
        if not game_over:
            continue_btn = QPushButton("Продолжить")
            continue_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px; color: white; background-color: rgba(0, 85, 170, 0.7);
                    border: 2px solid white; border-radius: 10px; padding: 10px;
                }
                QPushButton:hover { background-color: rgba(0, 85, 170, 0.9); }
            """)
            continue_btn.clicked.connect(self.close)
            buttons_layout.addWidget(continue_btn)

        exit_btn = QPushButton("Выйти")
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px; color: white; background-color: rgba(170, 0, 0, 0.7);
                border: 2px solid white; border-radius: 10px; padding: 10px;
            }
            QPushButton:hover { background-color: rgba(170, 0, 0, 0.9); }
        """)
        exit_btn.clicked.connect(self.exit_game)
        buttons_layout.addWidget(exit_btn)

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(msg_label)
        self.main_layout.addStretch()
        self.main_layout.addLayout(buttons_layout)

    def update_background(self):
        palette = QPalette()
        bg_path = os.path.join(ASSETS_PATH, DEFEAT_BG)
        if os.path.exists(bg_path):
            pixmap = QPixmap(bg_path)
        else:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.darkRed)
        scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def new_game(self):
        if self.parent:
            self.parent.restart_game()
        self.close()

    def exit_game(self):
        if self.parent:
            self.parent.close()
        self.close()