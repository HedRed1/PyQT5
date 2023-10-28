import sys
from PyQt5.QtWidgets import QApplication
from pin_code_system import Menu_Pin_Code

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu_Pin_Code()
    ex.show()
    sys.exit(app.exec_())