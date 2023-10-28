import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from DeleteMoneyDialog import DeleteMoneyDialog
from AddMoneyDialog import AddMoneyDialog
import sqlite3


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)
        self.update_balance()
        self.database_test = ['Time', 'Type', 'Money', 'Category', 'Method']
        self.database_test = [self.database_test]
        self.setFixedSize(270, 560)
        self.dialog_add_money = AddMoneyDialog(self.database_test, self.update_balance)
        self.dialog_del_money = DeleteMoneyDialog(self.database_test, self.update_balance)
        self.add_money.clicked.connect(self.dialog_add_money.show)
        self.del_money.clicked.connect(self.dialog_del_money.show)

    def update_balance(self):
        new_balance = 0
        new_balance_add = 0
        new_balance_del = 0
        try:
            conn = sqlite3.connect('financial_management_db.db')
            c = conn.cursor()
            c.execute('SELECT * FROM transactions')
            rows = c.fetchall()
            for elem in rows:
                if elem[1] == 'Пополнение':
                    new_balance_add += int(elem[2])
                    new_balance += int(elem[2])
                    self.sum_add_money.setText(str(new_balance_add))
                elif elem[1] == 'Расход':
                    new_balance_del += int(elem[2])
                    new_balance -= int(elem[2])
                    self.sum_del_money.setText(str(new_balance_del))
            self.balance_sum.setText(str(new_balance))
            conn.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())
