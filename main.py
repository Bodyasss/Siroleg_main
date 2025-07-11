import sys
import os
from PyQt5.QtWidgets import QApplication
from constants import ASSETS_PATH
from gui.main_menu import MainMenu

def main():
    app = QApplication(sys.argv)

    os.makedirs(ASSETS_PATH, exist_ok=True)

    main_menu = MainMenu()
    main_menu.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()