import sys
from PyQt5.QtWidgets import QApplication
from pin_code_system import Menu_Pin_Code
from main_menu import MainMenu
import bcrypt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('settings.txt', 'rb') as pin_code_file:
        text_hash = pin_code_file.read()
    if bcrypt.checkpw('password=1'.encode('utf-8'), text_hash):
        ex = Menu_Pin_Code()
    else:
        ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())
