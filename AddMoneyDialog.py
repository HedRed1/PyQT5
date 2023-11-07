from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import datetime
import sqlite3


class AddMoneyDialog(QDialog):
    def __init__(self, database, func):
        super().__init__()
        uic.loadUi('add_money.ui', self)
        self.add_money_to_bd.clicked.connect(self.add_money_bd)
        self.database_test = database
        self.update_balance = func
        with open('methods.txt', 'r', encoding='utf-8') as methods_file:
            read = methods_file.read().split(',')
            self.pay_method_comboBox.addItems(read)

    def add_money_bd(self):
        time_now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        money_to_add = int(self.money_input.text())
        category = '-'
        method_to_pay = self.pay_method_comboBox.currentText()
        con = sqlite3.connect('financial_management_db.db')
        c = con.cursor()
        data = [time_now, 'Пополнение', str(money_to_add), category, method_to_pay]
        c.execute('INSERT INTO transactions VALUES (?,?,?,?,?)', data)
        con.commit()
        con.close()
        self.update_balance()