import os
import random
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QScrollArea, QVBoxLayout,
                             QHBoxLayout, QFrame, QMessageBox)
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QBrush, QWheelEvent
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QTimer, QPoint

from constants import ASSETS_PATH, BACKGROUND_IMAGE
from game_data import MONSTERS, ITEMS
from gui.result_windows import ResultWindow, VictoryWindow, DefeatWindow



class CardGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Карточная RPG")
        self.showFullScreen()
        self.setAutoFillBackground(True)

        self.player = {}
        self.current_monster = None
        self.treasures_to_take = 0
        self.first_monster_defeated = False
        self.available_monsters = []
        self.available_items = []

        self.result_window = None
        self.victory_window = None
        self.defeat_window = None
        self.menu = None

        self.init_ui()
        self.restart_game()

    def init_ui(self):

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.decks_layout = QHBoxLayout()
        self.decks_layout.setContentsMargins(0, 0, 0, 0)
        self.decks_layout.setSpacing(20)

        self.treasure_button = self.create_deck_button("back_treasure.png", self.handle_treasure)
        self.door_button = self.create_deck_button("back_door.png", self.handle_door)

        self.monster_display = QLabel(self)
        self.monster_display.setFixedSize(200, 300)
        self.monster_display.setAlignment(Qt.AlignCenter)
        self.monster_display.hide()

        self.decks_layout.addWidget(self.treasure_button)
        self.decks_layout.addWidget(self.monster_display)
        self.decks_layout.addWidget(self.door_button)
        self.main_layout.addLayout(self.decks_layout)

        self.fight_area_container = QFrame()
        self.fight_area_container.setContentsMargins(0, 0, 0, 0)
        self.fight_area_container.setStyleSheet("background-color: transparent; border: none;")
        self.fight_area_layout = QHBoxLayout(self.fight_area_container)
        self.fight_area_layout.setContentsMargins(0, 0, 0, 0)
        self.fight_area_layout.setSpacing(20)
        self.fight_button = QPushButton("БИТВА")
        self.fight_button.setFixedSize(200, 80)
        self.fight_button.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: white; background-color: #8B0000; border-radius: 10px;")
        self.fight_button.clicked.connect(self.handle_fight)
        self.fight_area_layout.addStretch()
        self.fight_area_layout.addWidget(self.fight_button)
        self.fight_area_layout.addStretch()
        self.main_layout.addWidget(self.fight_area_container)
        self.main_layout.addStretch(1)

        self.play_area_frame = QFrame()
        self.play_area_frame.setStyleSheet(
            "border: 3px solid red; border-radius: 10px; background-color: rgba(0, 0, 0, 0.3);")
        self.play_area_layout = QHBoxLayout(self.play_area_frame)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")

        self.hand_container = QWidget()
        self.hand_layout = QHBoxLayout(self.hand_container)
        self.hand_layout.setSpacing(15)
        self.hand_layout.setContentsMargins(10, 5, 10, 5)

        self.scroll_area.setWidget(self.hand_container)
        self.play_area_layout.addWidget(self.scroll_area, 4)

        self.equipped_layout = QHBoxLayout()
        self.equipped_layout.setSpacing(15)
        self.play_area_layout.addLayout(self.equipped_layout, 3)

        self.description_label = QLabel()
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.description_label.setStyleSheet(
            "font-size: 20px; color: white; background-color: rgba(0, 51, 102, 0.8); "
            "border: 2px solid lightblue; border-radius: 5px; padding: 15px;")
        self.play_area_layout.addWidget(self.description_label, 2)

        self.main_layout.addWidget(self.play_area_frame, 1)

        self.stats_label = QLabel()
        self.stats_label.setStyleSheet(
            "font-size: 28px; color: white; font-weight: bold; background-color: rgba(0, 0, 0, 0.5);")
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.stats_label)

        self.scroll_anim = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value")
        self.scroll_anim.setDuration(300)
        self.scroll_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.current_scroll_pos = 0

    def restart_game(self):
        self.player = {
            "level": 1,
            "inventory": [],
            "equipped": {"helmet": None, "armor": None, "weapon": None, "boots": None}
        }
        self.current_monster = None
        self.treasures_to_take = 0
        self.first_monster_defeated = False
        self.available_monsters = MONSTERS.copy()
        self.available_items = ITEMS.copy()

        if self.monster_display:
            self.monster_display.hide()

        self.give_initial_treasures()
        self.update_ui()

    def give_initial_treasures(self):
        for _ in range(2):
            if len(self.player["inventory"]) < 8 and self.available_items:
                item = self.get_random_item()
                if item:
                    self.player["inventory"].append(item)
        self.update_ui()


    def wheelEvent(self, event: QWheelEvent):
        if self.hand_layout.count() == 0:
            return
        scroll_bar = self.scroll_area.horizontalScrollBar()
        max_pos = scroll_bar.maximum()
        delta = event.angleDelta().y()
        if delta > 0:
            new_pos = max(0, self.current_scroll_pos - 160)
        else:
            new_pos = min(max_pos, self.current_scroll_pos + 160)
        if new_pos != self.current_scroll_pos:
            self.scroll_anim.stop()
            self.scroll_anim.setStartValue(self.current_scroll_pos)
            self.scroll_anim.setEndValue(new_pos)
            self.scroll_anim.start()
            self.current_scroll_pos = new_pos

    def resizeEvent(self, event):
        palette = QPalette()
        background_path = os.path.join(ASSETS_PATH, BACKGROUND_IMAGE)
        if os.path.exists(background_path):
            pixmap = QPixmap(background_path)
            scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            self.setPalette(palette)
        super().resizeEvent(event)

    def closeEvent(self, event):
        from gui.main_menu import MainMenu
        self.menu = MainMenu()
        self.menu.show()
        event.accept()


    def create_deck_button(self, image_file, on_click):
        button = QPushButton()
        button.setFixedSize(200, 300)
        button.clicked.connect(on_click)
        path = os.path.join(ASSETS_PATH, image_file)
        if os.path.exists(path):
            button.setIcon(QIcon(path))
            button.setIconSize(QSize(200, 300))
            button.setStyleSheet("background-color: transparent; border: none;")
        else:
            button.setText("Нет\nизображения")
            button.setStyleSheet("font-size: 20px; color: white;")
        return button

    def create_card_widget(self, item, on_click=None, on_discard=None):
        card = QPushButton()
        card.setFixedSize(150, 225)

        folder = "treasures" if item in ITEMS else "doors"
        path = os.path.join(ASSETS_PATH, folder, item["image"])

        if os.path.exists(path):
            card.setIcon(QIcon(path))
            card.setIconSize(QSize(150, 225))
            card.setStyleSheet("background-color: transparent; border: none;")
        else:
            card.setText(item['name'])
            card.setStyleSheet(
                "font-size: 16px; color: white; background-color: #555; "
                "border-radius: 10px; padding: 10px;")

        if on_click:
            card.clicked.connect(lambda: on_click(item))

        if on_discard:
            card.setContextMenuPolicy(Qt.CustomContextMenu)
            card.customContextMenuRequested.connect(lambda pos: on_discard(item))

        return card

    def create_card_placeholder(self):
        placeholder = QLabel()
        placeholder.setFixedSize(150, 225)
        placeholder.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2); 
            border: 2px dashed #888; border-radius: 10px;
        """)
        return placeholder


    def get_random_monster(self):
        if not self.available_monsters:
            self.available_monsters = MONSTERS.copy()
        monster = random.choice(self.available_monsters)
        self.available_monsters.remove(monster)
        return monster

    def get_random_item(self):
        if not self.available_items:
            self.available_items = ITEMS.copy()
        if not self.available_items: return None
        item = random.choice(self.available_items)
        self.available_items.remove(item)
        return item

    def get_total_bonus(self):
        return sum(item["bonus"] for item in self.player["equipped"].values() if item)

    def equip_item(self, item):
        slot = item.get("slot")
        if not slot or slot not in self.player["equipped"]:
            return False

        if self.player["equipped"][slot]:
            self.unequip_item(self.player["equipped"][slot])

        self.player["equipped"][slot] = item
        self.player["inventory"].remove(item)
        return True

    def unequip_item(self, item):
        if len(self.player["inventory"]) >= 8:
            QMessageBox.information(self, "Инвентарь полон", "Нет места в инвентаре, чтобы снять предмет!")
            return False

        for slot, equipped_item in self.player["equipped"].items():
            if equipped_item == item:
                self.player["equipped"][slot] = None
                self.player["inventory"].append(item)
                return True
        return False


    def handle_door(self):
        if self.current_monster:
            QMessageBox.information(self, "Внимание", "Сначала разберитесь с текущим монстром!")
            return

        self.current_monster = self.get_random_monster()
        path = os.path.join(ASSETS_PATH, "doors", self.current_monster["image"])
        if os.path.exists(path):
            self.monster_display.setPixmap(
                QPixmap(path).scaled(200, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        center_x = self.width() // 2 - 100
        self.monster_display.move(center_x, 50)
        self.monster_display.show()
        self.monster_display.raise_()
        self.update_ui()

    def handle_treasure(self):
        if self.treasures_to_take <= 0:
            QMessageBox.information(self, "Нет сокровищ", "Сейчас нет сокровищ, которые можно взять.")
            return

        if len(self.player["inventory"]) >= 8:
            QMessageBox.information(self, "Инвентарь полон", "У вас нет места в инвентаре для нового сокровища!")
            return

        item = self.get_random_item()
        if item:
            self.player["inventory"].append(item)
            self.treasures_to_take -= 1
        self.update_ui()

    def handle_inventory_click(self, item_to_equip):
        self.equip_item(item_to_equip)
        self.update_ui()

    def handle_equipped_click(self, item_to_unequip):
        self.unequip_item(item_to_unequip)
        self.update_ui()

    def handle_discard_card(self, item_to_discard):
        reply = QMessageBox.question(self, 'Сбросить карту',
                                     f"Вы уверены, что хотите сбросить '{item_to_discard['name']}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if item_to_discard in self.player["inventory"]:
                self.player["inventory"].remove(item_to_discard)
                self.update_ui()

    def handle_fight(self):
        if not self.current_monster:
            return
        player_power = self.player["level"] + self.get_total_bonus()
        self.check_fight_result(player_power)

    def check_fight_result(self, player_power):
        if player_power >= self.current_monster["level"]:
            self.player["level"] += self.current_monster["reward"]
            self.treasures_to_take = self.current_monster["reward"]
            self.first_monster_defeated = True

            if self.player["level"] >= 10:
                self.victory_window = VictoryWindow(self)
                self.victory_window.show()
            else:
                self.result_window = ResultWindow(self, victory=True)
                self.result_window.show()
        else:
            level_before = self.player["level"]
            self.player["level"] -= self.current_monster["penalty"]
            level_lost = level_before - self.player["level"]

            if self.player["level"] < 1:
                self.defeat_window = DefeatWindow(self, monster_name=self.current_monster["name"],
                                                  level_lost=level_lost, game_over=True)
                self.defeat_window.show()
            else:
                self.defeat_window = DefeatWindow(self, monster_name=self.current_monster["name"],
                                                  level_lost=level_lost, game_over=False)
                self.defeat_window.show()

        self.current_monster = None
        self.update_ui()


    def update_ui(self):
        for i in reversed(range(self.hand_layout.count())):
            self.hand_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.equipped_layout.count())):
            self.equipped_layout.itemAt(i).widget().setParent(None)

        for item in self.player["inventory"]:
            card_widget = self.create_card_widget(item, self.handle_inventory_click, self.handle_discard_card)
            self.hand_layout.addWidget(card_widget)
        for _ in range(8 - len(self.player["inventory"])):
            self.hand_layout.addWidget(self.create_card_placeholder())

        slots_order = ["helmet", "armor", "weapon", "boots"]
        slot_names = {"helmet": "Шлем", "armor": "Броня", "weapon": "Оружие", "boots": "Ботинки"}

        for slot_key in slots_order:
            slot_frame = QFrame()
            slot_frame.setStyleSheet("background-color: rgba(0,0,0,0.3); border-radius: 5px;")
            slot_layout = QVBoxLayout(slot_frame)
            slot_layout.setAlignment(Qt.AlignCenter)
            slot_label = QLabel(slot_names[slot_key])
            slot_label.setStyleSheet("font-size: 14px; color: white;")
            slot_layout.addWidget(slot_label)

            item = self.player["equipped"].get(slot_key)
            if item:
                card_widget = self.create_card_widget(item, self.handle_equipped_click, on_discard=None)
                slot_layout.addWidget(card_widget)
            else:
                slot_layout.addWidget(self.create_card_placeholder())
            self.equipped_layout.addWidget(slot_frame)

        if self.current_monster:
            self.fight_area_container.show()
            self.door_button.hide()
            self.treasure_button.hide()
            self.description_label.setText(
                f"<b>МОНСТР:</b> {self.current_monster['name']}<br><br>"
                f"<b>Уровень:</b> {self.current_monster['level']}<br><br>"
                f"{self.current_monster['desc']}<br><br>"
                f"<b>Награда:</b> +{self.current_monster['reward']} уровень<br>"
                f"<b>Штраф:</b> -{self.current_monster['penalty']} уровень")
        else:
            self.monster_display.hide()
            self.fight_area_container.hide()
            self.door_button.show()
            self.treasure_button.show()
            if self.treasures_to_take > 0:
                self.description_label.setText(
                    f"<b>ПОБЕДА!</b><br><br>Вы можете взять {self.treasures_to_take} сокровищ(е).")
            else:
                self.description_label.setText(
                    "<b>Исследуйте подземелье.</b><br><br>"
                    "Выбейте дверь, чтобы найти приключения, или возьмите сокровища, если заслужили.")

        bonus = self.get_total_bonus()
        self.stats_label.setText(
            f"Уровень: {self.player['level']} | Бонусы: +{bonus} | Общая сила: {self.player['level'] + bonus}")

        self.scroll_area.horizontalScrollBar().setValue(self.current_scroll_pos)