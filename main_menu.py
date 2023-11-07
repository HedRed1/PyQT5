from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog
from DeleteMoneyDialog import DeleteMoneyDialog
from AddMoneyDialog import AddMoneyDialog
from settings import Settings
import matplotlib.pyplot as plt
import datetime
from currency_converter import CurrencyConverter
from datetime import date
import sqlite3


class MainMenu(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('main_menu.ui', self)
            with open('currency_now.txt', 'r', encoding='utf-8') as currency_now_file:
                read = currency_now_file.read()
            self.update_balance(conversion_from='RUB', conversion_to=read)
            self.database_test = ['Time', 'Type', 'Money', 'Category', 'Method']
            self.numbers_category_list = []
            self.database_test = [self.database_test]
            self.setFixedSize(290, 550)
            self.dialog_add_money = AddMoneyDialog(self.database_test, self.update_balance)
            self.dialog_del_money = DeleteMoneyDialog(self.database_test, self.update_balance)
            self.dialog_settings = Settings()
            self.dialog_information = Info_For_Money()
            self.dialog_add_money_to_mission = Add_Money_Mission(self.update_balance())
            self.dialog_currency = Currency(self.update_balance)
            self.add_money.clicked.connect(self.dialog_add_money.show)
            self.del_money.clicked.connect(self.dialog_del_money.show)
            self.settings_button.clicked.connect(self.dialog_settings.show)
            self.information.clicked.connect(self.dialog_information.show)
            self.currency_button.clicked.connect(self.dialog_currency.show)
            self.add_money_to_mission.clicked.connect(self.dialog_add_money_to_mission.show)
        except Exception as e:
            print(e)

    def update_balance(self, conversion_from='RUB', conversion_to='RUB'):
        with open('currency_now.txt', 'r', encoding='utf-8') as currency_now_file:
            conversion_from = currency_now_file.read()
        with open('currency_now.txt', 'w', encoding='utf-8') as currency_now_file:
            currency_now_file.write(conversion_to)
        new_balance = 0
        new_balance_add = 0
        new_balance_del = 0
        conv = CurrencyConverter()
        con = sqlite3.connect('financial_management_db.db')
        c = con.cursor()
        c.execute('SELECT * FROM transactions')
        elements = c.fetchall()
        for elem in elements:
            if elem[1] == 'Пополнение':
                new_balance_add += float(elem[2])
                new_balance += float(elem[2])
                self.sum_add_money.setText(
                    str(round(conv.convert(new_balance_add,
                                           conversion_from, conversion_to, date(2022, 3, 1)), 1)))
            elif elem[1] == 'Расход':
                new_balance_del += float(elem[2])
                new_balance -= float(elem[2])
                self.sum_del_money.setText(
                    str(round(conv.convert(new_balance_del,
                                           conversion_from, conversion_to, date(2022, 3, 1)), 1)))
        self.balance_sum_label.setText(
            str(round(conv.convert(new_balance,
                                   conversion_from, conversion_to, date(2022, 3, 1)), 1)))
        con.close()


class Info_For_Money(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('info_date_money.ui', self)
            self.info_button.clicked.connect(self.sum_money_labels)
            self.del_info_money.clicked.connect(self.information_for_del_money)
            self.add_info_money.clicked.connect(self.information_for_add_money)
        except Exception as e:
            print(e)

    def sum_money_labels(self):
        try:
            add_sum = self.add_money_label()
            self.sum_add_money.setText(str(add_sum))
            del_sum = self.del_money_label()
            self.sum_del_money.setText(str(del_sum))
        except Exception as e:
            print(e)

    def add_money_label(self):
        try:
            start_date = self.data_start.date().toString("dd-MM-yyyy") + ' 00:00:00'
            end_date = self.data_stop.date().toString("dd-MM-yyyy") + ' 23:59:59'
            con = sqlite3.connect('financial_management_db.db')
            cur = con.cursor()
            cur.execute('SELECT SUM(Money) FROM transactions WHERE Time>=? AND Time <=?',
                        (start_date, end_date,))
            result = cur.fetchone()
            return result[0]
        except Exception as e:
            print(e)

    def del_money_label(self):
        try:
            start_date = self.data_start.date().toString("dd-MM-yyyy") + ' 00:00:00'
            end_date = self.data_stop.date().toString("dd-MM-yyyy") + ' 23:59:59'
            con = sqlite3.connect('financial_management_db.db')
            cur = con.cursor()
            cur.execute(
                'SELECT SUM(Money) FROM transactions WHERE Type=? AND Time>=? AND '
                'Time<=?', ('Расход', start_date, end_date,))
            result = cur.fetchone()
            return result[0]
        except Exception as e:
            print(e)

    def information_for_del_money(self):
        try:
            start_date = self.data_start.date().toString("dd-MM-yyyy") + ' 00:00:00'
            end_date = self.data_stop.date().toString("dd-MM-yyyy") + ' 23:59:59'
            self.numbers_category_list = []
            con = sqlite3.connect('financial_management_db.db')
            cur = con.cursor()
            cur.execute('SELECT DISTINCT Category FROM transactions WHERE Time>=? AND Time <=?',
                        (start_date, end_date,))
            result = cur.fetchall()
            result = [elem[0] for elem in result if elem[0] != '-']
            self.numbers_category(result)
            plt.pie(self.numbers_category_list, labels=result,
                    autopct=lambda p: '{:.2f}%  ({:,.0f})'.format(p, p * sum(self.numbers_category_list) / 100))
            plt.title("Траты по категориям")
            plt.show()
        except Exception as e:
            print(e)

    def numbers_category(self, lists_of_category):
        try:
            start_date = self.data_start.date().toString("dd-MM-yyyy") + ' 00:00:00'
            end_date = self.data_stop.date().toString("dd-MM-yyyy") + ' 23:59:59'
            for category in lists_of_category:
                con = sqlite3.connect('financial_management_db.db')
                cur = con.cursor()
                cur.execute('SELECT SUM(Money) FROM transactions WHERE Category=? AND Time>=? AND Time<=?',
                            (category, start_date, end_date,))
                self.numbers_category_list.append(cur.fetchone()[0])
        except Exception as e:
            print(e)

    def information_for_add_money(self):
        try:
            start_date = self.data_start.date().toString("dd-MM-yyyy") + ' 00:00:00'
            end_date = self.data_stop.date().toString("dd-MM-yyyy") + ' 23:59:59'
            self.numbers_methods_list = []
            con = sqlite3.connect('financial_management_db.db')
            cur = con.cursor()
            cur.execute('SELECT DISTINCT Method FROM transactions WHERE Time>=? AND Time <=?',
                        (start_date, end_date,))
            result = cur.fetchall()
            result = [elem[0] for elem in result if elem[0] != '-']
            self.numbers_methods(result)
            print(result)
            plt.pie(self.numbers_methods_list, labels=result,
                    autopct=lambda p: '{:.2f}%  ({:,.0f})'.format(p, p * sum(self.numbers_methods_list) / 100))
            plt.title("Доходы по методам")
            plt.show()
        except Exception as e:
            print(e)

    def numbers_methods(self, lists_of_methods):
        try:
            start_date = self.data_start.date().toString("dd-MM-yyyy") + ' 00:00:00'
            end_date = self.data_stop.date().toString("dd-MM-yyyy") + ' 23:59:59'
            con = sqlite3.connect('financial_management_db.db')
            cur = con.cursor()
            for method in lists_of_methods:
                cur.execute('SELECT SUM(Money) FROM transactions WHERE Method=? AND Time>=? AND Time<=?',
                            (method, start_date, end_date,))
                self.numbers_methods_list.append(cur.fetchone()[0])
            return str(sum(self.numbers_methods_list))
        except Exception as e:
            print(e)


class Currency(QDialog):
    def __init__(self, func):
        try:
            super().__init__()
            self.update_balance = func
            uic.loadUi('currency_convertator.ui', self)
            self.conventator_button.clicked.connect(self.convertator)
            with open('currency_now.txt', 'r', encoding='utf-8') as currency_now_file:
                read = currency_now_file.read()
            self.before_box.addItems([read])
            with open('currency_all.txt', 'r', encoding='utf-8') as currency_all_file:
                read = [currency.strip('\n') for currency in currency_all_file]
                print(read)
            self.after_box.addItems(read)
        except Exception as e:
            print(e)

    def convertator(self):
        try:
            conversion_from = self.before_box.currentText()
            conversion_to = self.after_box.currentText()
            with open('currency_now.txt', 'w', encoding='utf-8') as currency_now_file:
                currency_now_file.write(conversion_to)
            self.redactor_bd(conversion_from, conversion_to)
            self.update_balance(conversion_from, conversion_to)
            self.before_box.clear()
            self.before_box.addItems([conversion_to])
        except Exception as e:
            print(e)

    def redactor_bd(self, conv_from, conv_to):
        con = sqlite3.connect('financial_management_db.db')
        cursor = con.cursor()
        c = CurrencyConverter()
        c.execute("SELECT * FROM transactions")
        elements_bd = c.fetchall()
        for elem in elements_bd:
            Time = elem[0]
            Money = elem[2]
            Currency_Money = c.convert(Money, conv_from, conv_to, date(2022, 3, 1))
            c.execute('UPDATE transactions SET Money=? WHERE Time=?', (round(Currency_Money, 3), Time))
        con.commit()
        con.close()


class Add_Money_Mission(QDialog):
    def __init__(self, func):
        try:
            self.update_balance = func
            super().__init__()
            uic.loadUi('add_money_mission.ui', self)
            with open('mission.txt', 'r', encoding='utf-8') as mission_file:
                self.read = mission_file.read().strip().split(',')
                self.read = [elem for elem in self.read if elem != '']
                self.mission_Box.addItems(self.read)
            with open('methods.txt', 'r', encoding='utf-8') as method_file:
                self.read = method_file.read().strip().split(',')
                self.read = [elem for elem in self.read if elem != '']
                self.method_Box.addItems(self.read)
            self.add_money_button.clicked.connect(self.add_money)
        except Exception as e:
            print(e)

    def add_money(self):
        try:
            if not (self.sum_edit.text().isdigit()):
                self.error_label.setText('Ошибка в поле суммы!')
                return False
            name_mission = self.mission_Box.currentText()
            time_now = datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')
            money = self.sum_edit.text()
            method = self.method_Box.currentText()
            data = [time_now, 'Пополнение', money, method, '-']
            con = sqlite3.connect('financial_management_db.db')
            c = con.cursor()
            c.execute(f'INSERT INTO {name_mission} VALUES(?,?,?,?,?)', data)
            self.error_label.setText('Успешное добавление операции!')
            con.commit()
            con.close()
            con = sqlite3.connect('financial_management_db.db')
            c = con.cursor()
            data = [time_now, 'Расход', money, name_mission, method]
            c.execute('INSERT INTO transactions VALUES(?,?,?,?,?)', data)
            con.commit()
            con.close()
        except Exception as e:
            self.error_label.setText('Ошибка!')
            print(e)