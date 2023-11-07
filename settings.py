from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem
from DeleteMoneyDialog import DeleteMoneyDialog
from AddMoneyDialog import AddMoneyDialog
import sqlite3
import bcrypt


class Settings(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        # self.edit_method_dialog = None
        # self.edit_category_dialog = None
        # self.edit_base_window = None
        # self.edit_pin_code = None
        # self.verify_window = None
        self.setFixedSize(357, 219)
        # self.edit_method_dialog = EditMethod()
        # self.edit_category_dialog = EditCategory()
        self.method_button.clicked.connect(self.show_edit_method)
        self.category_button.clicked.connect(self.show_edit_category)
        self.datebase_button.clicked.connect(self.show_edit_base)
        self.pin_code_button.clicked.connect(self.show_edit_pin_code)
        self.mission_button.clicked.connect(self.show_edit_mission)

    def show_edit_method(self):
        self.edit_method_dialog = EditMethod()
        self.edit_method_dialog.show()

    def show_edit_category(self):
        self.edit_category_dialog = EditCategory()
        self.edit_category_dialog.show()

    def show_edit_base(self):
        self.edit_base_window = Base_Del()
        self.edit_base_window.exec_()

    def show_edit_pin_code(self):
        self.edit_pin_code_dialog = Pin_Code_Edit()
        self.edit_pin_code_dialog.show()

    def show_edit_mission(self):
        self.edit_mission_dialog = EditMission()
        self.edit_mission_dialog.show()


class EditMethod(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_or_del_method.ui', self)
        self.AddMethodDialog = Add_Method_Class()
        self.DelMethodDialog = Del_Method_Class()
        self.add_method_button.clicked.connect(self.AddMethodDialog.show)
        self.del_method_button.clicked.connect(self.DelMethodDialog.show)


class Add_Method_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_method.ui', self)
        self.info_label.setText('Добавление метода оплаты')
        self.add_method.clicked.connect(self.check_card)

    def check_card(self):
        try:
            self.card = self.card_number.text().strip().replace(' ', '')
            if len(self.card) != 16 or not (self.card.isdigit()):
                self.info_label.setText('Неверный номер карты!\nПопробуйте снова.')
            else:
                self.formated_card = f'Карта *{self.card[-4:]}'
                with open('methods.txt', 'a', encoding='utf-8') as method_file:
                    method_file.write(f',{self.formated_card}')
                self.info_label.setText('Успешное добавление карты!')
        except:
            self.info_label.setText('Неверный номер карты!\nПопробуйте снова.')


class Del_Method_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('del_method.ui', self)
        with open('methods.txt', 'r', encoding='utf-8') as methods_file:
            self.read = methods_file.read().split(',')
            self.ComboMethod.addItems(self.read)
        self.checkButton.clicked.connect(self.Del_Method_func)

    def Del_Method_func(self):
        method_to_del = self.ComboMethod.currentText()
        with open('methods.txt', 'r', encoding='utf-8') as methods_file:
            try:
                self.read = methods_file.read().split(',')
                self.list_to_write_file = [method for method in self.read if method_to_del != method]
            except:
                self.info_del_method.setText('Ошибка. Попробуйте еще раз.')
        with open('methods.txt', 'w', encoding='utf-8') as methods_file:
            methods_file.write(','.join(self.list_to_write_file))
            self.info_del_method.setText('Метод успешно удален!')


class EditCategory(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_or_del_category.ui', self)
        self.AddCategoryDialog = Add_Category_Class()
        self.DelCategoryDialog = Del_Category_Class()
        self.add_category_button.clicked.connect(self.AddCategoryDialog.show)
        self.del_category_button.clicked.connect(self.DelCategoryDialog.show)


class Add_Category_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('add_category.ui', self)
        self.add_category.clicked.connect(self.add_category_func)

    def add_category_func(self):
        category = self.input_category.text()
        with open('category.txt', 'a', encoding='utf-8') as category_file:
            category_file.write(f',{category}')
        self.info_label_2.setText('Категория успешно добавлена!')


class Del_Category_Class(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('del_category.ui', self)
        with open('category.txt', 'r', encoding='utf-8') as category_file:
            self.read = category_file.read().split(',')
            self.ComboCategory.addItems(self.read)
        self.del_category.clicked.connect(self.del_category_func)

    def del_category_func(self):
        category_to_del = self.ComboCategory.currentText()
        self.list_to_write_file = []
        self.read = []
        with open('category.txt', 'r', encoding='utf-8') as category_file:
            try:
                self.read = category_file.read().split(',')
                self.list_to_write_file = [category for category in self.read if category_to_del != category]
            except:
                self.info_label_2.setText('Ошибка, попробуйте еще раз!')
        with open('category.txt', 'w', encoding='utf-8') as category_file:
            category_file.write(','.join(self.list_to_write_file))
            self.info_label_2.setText('Категория успешно удалена!')


class Base_Del(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('data.ui', self)
        self.pushButton.clicked.connect(self.delete_base)
        con = sqlite3.connect('financial_management_db.db')
        cur = con.cursor()
        res = 'SELECT * FROM transactions'
        result = cur.execute(res).fetchall()
        self.Widget.setRowCount(len(result))
        for x, row in enumerate(result):
            for y, col in enumerate(row):
                self.Widget.setItem(x, y, QTableWidgetItem(str(col)))

    def delete_base(self):
        con = sqlite3.connect('financial_management_db.db')
        cur = con.cursor()
        items = self.Widget.selectedItems()
        for item in items:
            row = item.row()
            time_row = self.Widget.item(row, 0)
            cur.execute(f"DELETE FROM transactions WHERE Time = '{time_row.text()}'")
            self.label_2.setText('Успешное удаление операции!')
        con.commit()


class Pin_Code_Edit(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('pin_code_setup.ui', self)
        # self.pin_code_edit.textChanged.connect(self.edit_pin)
        self.create_pin_button.clicked.connect(self.create_pin_code)

    def create_pin_code(self):
        self.pin_code_input = self.pin_code_edit.text()
        if len(self.pin_code_input) == 4 and self.pin_code_input.isdigit():
            self.hashed_pin_code = bcrypt.hashpw(self.pin_code_input.encode('utf-8'), bcrypt.gensalt())
            with open('password.txt', 'wb') as pin_code_file:
                pin_code_file.write(self.hashed_pin_code)

            self.hashed_text = bcrypt.hashpw('password=1'.encode('utf-8'), bcrypt.gensalt())
            with open('settings.txt', 'wb') as settings_file:
                settings_file.write(self.hashed_text)

            self.info_label_2.setText('Пин-код успешно создан!')
        elif len(self.pin_code_input) == 0:
            self.hashed_text = bcrypt.hashpw('password=0'.encode('utf-8'), bcrypt.gensalt())
            with open('settings.txt', 'wb') as settings_file:
                settings_file.write(self.hashed_text)
            self.info_label_2.setText('Пин-код успешно удален!')
        else:
            self.info_label_2.setText('Ошибка! Пинкод должен состоять из цифр\n и его длина должна быть 4 символа')


class EditMission(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('add_or_del_mission.ui', self)
            self.AddMissionDialog = Add_Mission_Class()
            self.DelMissionDialog = Del_Mission_Class()
            self.add_mission_button.clicked.connect(self.AddMissionDialog.show)
            self.del_mission_button.clicked.connect(self.DelMissionDialog.show)
        except Exception as e:
            print(e)


class Add_Mission_Class(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('add_mission.ui', self)
            self.create_button.clicked.connect(self.create_mission)
        except Exception as e:
            print(e)

    def create_mission(self):
        try:
            con = sqlite3.connect('financial_management_db.db')
            c = con.cursor()
            if not (self.sum_edit.text().isdigit()):
                self.error_label.setText('Ошибка в поле суммы!')
                con.close()
                return False
            name_mission = self.name_edit.text().replace(' ', '_')
            sum_mission = self.sum_edit.text()
            c.execute(
                f"""CREATE TABLE {name_mission} (Time TEXT, Type TEXT, Money TEXT, Method TEXT, Summa TEXT);""")
            c.execute(f'INSERT INTO {name_mission} VALUES (?,?,?,?,?)', ['-', '-', '-', '-', sum_mission])
            con.commit()
            con.close()
            with open('mission.txt', 'a', encoding='utf-8') as mission_file:
                mission_file.write(f'{name_mission},')
            self.error_label.setText('Цель успешно создана!')
        except Exception as e:
            print(e)


class Del_Mission_Class(QDialog):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('del_mission.ui', self)
            with open('mission.txt', 'r', encoding='utf-8') as mission_file:
                self.read = mission_file.read().strip().split(',')
                self.read = [elem for elem in self.read if elem != '']
                self.ComboMission.addItems(self.read)
            self.del_mission.clicked.connect(self.del_mission_func)
        except Exception as e:
            print(e)

    def del_mission_func(self):
        try:
            with sqlite3.connect('financial_management_db.db') as con:
                c = con.cursor()
                c.execute(f'''DROP TABLE {self.ComboMission.currentText()}''')
                con.commit()
                con.close()
            with open('mission.txt', 'r', encoding='utf-8') as mission_file:
                try:
                    self.read = mission_file.read().split(',')
                    self.list_to_write_file = [mission for mission in self.read if
                                               self.ComboMission.currentText() != mission]
                except:
                    self.error_label.setText('Ошибка, попробуйте еще раз!')
            with open('mission.txt', 'w', encoding='utf-8') as mission_file:
                mission_file.write(self.list_to_write_file)
            self.error_label.setText('Цель успешно удалена!')
        except Exception as e:
            print(e)
