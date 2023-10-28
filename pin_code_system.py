    from PyQt5 import uic
    from PyQt5.QtWidgets import QMainWindow
    from PyQt5.QtCore import QTimer
    from main_menu import MainMenu
    import bcrypt
    
    
    class Menu_Pin_Code(QMainWindow):
        def __init__(self):
            super().__init__()
            self.timer = 0
            self.times = 0
            self.pin_code_hash = ''
            uic.loadUi('Project_pin_code.ui', self)
            self.hashed_pin_code = bcrypt.hashpw('1580'.encode('utf-8'), bcrypt.gensalt())
            with open('password.txt', 'wb') as pin_code_file:
                pin_code_file.write(self.hashed_pin_code)
            self.setFixedSize(290, 550)
            self.pin_code_to_print = ''
            self.attempt_input_pin_code = 0
            self.buttons_of_keyboard = [self.pin_code_button_1, self.pin_code_button_2, self.pin_code_button_3,
                                        self.pin_code_button_4, self.pin_code_button_5, self.pin_code_button_6,
                                        self.pin_code_button_7, self.pin_code_button_8, self.pin_code_button_9,
                                        self.pin_code_button_0, self.pin_code_button_clear_last,
                                        self.pin_code_button_clear_all]
            self.buttons_of_key_pin_code = [self.pin_code_0, self.pin_code_1, self.pin_code_2, self.pin_code_3]
            # self.styleSheet_button = ["background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;",
            # "background-color: #000000; border: 1px solid black; border-radius: 22px;"]
            self.pin_code_button_1.clicked.connect(self.add_one)
            self.pin_code_button_2.clicked.connect(self.add_two)
            self.pin_code_button_3.clicked.connect(self.add_three)
            self.pin_code_button_4.clicked.connect(self.add_four)
            self.pin_code_button_5.clicked.connect(self.add_five)
            self.pin_code_button_6.clicked.connect(self.add_six)
            self.pin_code_button_7.clicked.connect(self.add_seven)
            self.pin_code_button_8.clicked.connect(self.add_eight)
            self.pin_code_button_9.clicked.connect(self.add_nine)
            self.pin_code_button_0.clicked.connect(self.add_zero)
            self.pin_code_button_clear_last.clicked.connect(self.clear_last)
            self.pin_code_button_clear_all.clicked.connect(self.clear_all)
            self.color_pin_code_buttons()
            for button in self.buttons_of_key_pin_code:
                button.setEnabled(False)
    
        def add_one(self):
            self.pin_code_to_print += '1'
            self.color_pin_code_buttons()
    
        def add_two(self):
            self.pin_code_to_print += '2'
            self.color_pin_code_buttons()
    
        def add_three(self):
            self.pin_code_to_print += '3'
            self.color_pin_code_buttons()
    
        def add_four(self):
            self.pin_code_to_print += '4'
            self.color_pin_code_buttons()
    
        def add_five(self):
            self.pin_code_to_print += '5'
            self.color_pin_code_buttons()
    
        def add_six(self):
            self.pin_code_to_print += '6'
            self.color_pin_code_buttons()
    
        def add_seven(self):
            self.pin_code_to_print += '7'
            self.color_pin_code_buttons()
    
        def add_eight(self):
            self.pin_code_to_print += '8'
            self.color_pin_code_buttons()
    
        def add_nine(self):
            self.pin_code_to_print += '9'
            self.color_pin_code_buttons()
    
        def add_zero(self):
            self.pin_code_to_print += '0'
            self.color_pin_code_buttons()
    
        def clear_last(self):
            self.pin_code_to_print = self.pin_code_to_print[:-1]
            self.color_pin_code_buttons()
    
        def clear_all(self):
            self.pin_code_to_print = ''
            self.color_pin_code_buttons()
    
        def color_pin_code_buttons(self):
            if len(self.pin_code_to_print) == 0:
                self.pin_code_0.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
                self.pin_code_1.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
                self.pin_code_2.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
                self.pin_code_3.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
            elif len(self.pin_code_to_print) == 1:
                self.input_pin_code.resize(230, 40)
                self.input_pin_code.setText('ВВЕДИТЕ ПИН-КОД')
                self.input_pin_code.setStyleSheet("font-size: 14pt; color: #000000;")
                self.pin_code_0.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_1.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
                self.pin_code_2.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
                self.pin_code_3.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
            elif len(self.pin_code_to_print) == 2:
                self.pin_code_0.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_1.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_2.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
                self.pin_code_3.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
            elif len(self.pin_code_to_print) == 3:
                self.pin_code_0.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_1.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_2.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_3.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
            elif len(self.pin_code_to_print) == 4:
                self.pin_code_0.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_1.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_2.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.pin_code_3.setStyleSheet("background-color: #000000; border: 1px solid black; border-radius: 22px;")
                self.check_the_pin_code()
    
        def return_to_default(self):
            self.pin_code_to_print = ''
            for button in self.buttons_of_key_pin_code:
                button.setStyleSheet("background-color: #FFFFFF; border: 1px solid black; border-radius: 22px;")
    
        def many_attempts_pin_code(self):
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_wrong_pin_message)
            self.timer.start(1000)
            self.times = 30
    
        def update_wrong_pin_message(self):
            self.wrong_pin_code.setText(f'ВЫ ВВЕЛИ НЕВЕРНЫЙ ПАРОЛЬ 3 РАЗА ПОДРЯД!\nПОПРОБУЙТЕ ЧЕРЕЗ {self.times} СЕКУНД')
            self.times -= 1
            if self.times < 0:
                self.wrong_pin_code.setText('')
                for buttons in self.buttons_of_keyboard:
                    buttons.setEnabled(True)
                self.input_pin_code.setText('ПОПРОБУЙТЕ ЕЩЕ РАЗ')
                self.input_pin_code.move(40, 60)
                self.input_pin_code.resize(230, 40)
                self.input_pin_code.setStyleSheet("font-size: 14pt; color: #000000")
                self.timer.stop()
    
        def check_the_pin_code(self):
            with open('password.txt', 'rb') as pin_code_file:
                self.pin_code_hash = pin_code_file.read()
            if bcrypt.checkpw(self.pin_code_to_print.encode('utf-8'), self.pin_code_hash):
                self.input_pin_code.setText('ДОСТУП РАЗРЕШЕН!')
                self.input_pin_code.move(40, 220)
                self.input_pin_code.resize(230, 40)
                self.input_pin_code.setStyleSheet("font-size: 14pt; color: #90ee90;")
                self.hide_pin_code()
                self.hide_keyword()
                self.close()
                Menu_Pin_Code().hide()
                MainMenu().show()
            else:
                self.return_to_default()
                self.attempt_input_pin_code += 1
                print(self.attempt_input_pin_code)
                self.input_pin_code.setText('НЕВЕРНЫЙ ПАРОЛЬ!')
                self.input_pin_code.move(40, 60)
                self.input_pin_code.resize(230, 40)
                self.input_pin_code.setStyleSheet("font-size: 14pt; color: #ff0000")
                if self.attempt_input_pin_code == 3:
                    self.many_attempts_pin_code()
                    for buttons in self.buttons_of_keyboard:
                        buttons.setEnabled(False)
                    self.attempt_input_pin_code = 0
    
        def hide_pin_code(self):
            if self.pin_code_to_print == self.pin_code:
                self.pin_code_0.hide()
                self.pin_code_1.hide()
                self.pin_code_2.hide()
                self.pin_code_3.hide()
            else:
                self.pin_code_to_print = ''
                self.return_to_default()
    
        def hide_keyword(self):
            for button in self.buttons_of_keyboard:
                button.hide()
