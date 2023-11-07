from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import datetime
import sqlite3


class DeleteMoneyDialog(QDialog):
    def __init__(self, database, func):
        super().__init__()
        uic.loadUi('del_money.ui', self)
        self.del_money_to_bd.clicked.connect(self.del_money_bd)
        self.database_test = database
        self.update_balance = func
        with open('methods.txt', 'r', encoding='utf-8') as methods_file:
            read = methods_file.read().split(',')
            self.pay_method_comboBox.addItems(read)
        with open('category.txt', 'r', encoding='utf-8') as category_file:
            read = category_file.read().split(',')
            self.category_comboBox.addItems(read)

    def del_money_bd(self):
        time_now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        money_to_del = int(self.money_input.text())
        category = self.category_comboBox.currentText()
        method_to_pay = self.pay_method_comboBox.currentText()
        con = sqlite3.connect('financial_management_db.db')
        c = con.cursor()
        data = [time_now, 'Расход', str(money_to_del), category, method_to_pay]
        c.execute('INSERT INTO transactions VALUES (?,?,?,?,?)', data)
        con.commit()
        con.close()
        self.update_balance()
