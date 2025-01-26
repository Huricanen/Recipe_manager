import sys

from PyQt6.QtCore import QTime
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPolygonF, QIcon
from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QInputDialog, QLineEdit, QPlainTextEdit,
                             QTimeEdit, QListWidget, QMessageBox, QFileDialog)

from datetime import datetime
import sqlite3


class Manager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(760, 680)
        self.setWindowTitle('Менеджер рецептов')
        self.setWindowIcon(QIcon('_internal\Manager_window_icon.jpg'))

        # Управление категориями рецептов

        self.label_categories = QLabel('Команды для управления категориями', self)
        self.label_categories.adjustSize()
        self.label_categories.move(50, 600)

        self.btn_add_new_category = QPushButton('Добавить новую категорию', self)
        self.btn_add_new_category.setStyleSheet('QPushButton { background-color: #228B22}')
        self.btn_add_new_category.adjustSize()
        self.btn_add_new_category.move(20, 625)
        self.btn_add_new_category.clicked.connect(self.add_new_category)

        self.btn_del_category = QPushButton('Удалить категорию', self)
        self.btn_del_category.setStyleSheet('QPushButton { background-color: #B22222}')
        self.btn_del_category.adjustSize()
        self.btn_del_category.move(190, 625)
        self.btn_del_category.clicked.connect(self.del_existing_category)

        # Управление рецептами

        self.label_recipies = QLabel('Команды для управления рецептами', self)
        self.label_recipies.adjustSize()
        self.label_recipies.move(460, 10)

        self.btn_add_recipe = QPushButton('Сохранить рецепт в категорию', self)
        self.btn_add_recipe.adjustSize()
        self.btn_add_recipe.move(390, 30)
        self.btn_add_recipe.clicked.connect(self.add_new_recipe)

        self.btn_clear = QPushButton('Создать новый рецепт', self)
        self.btn_clear.adjustSize()
        self.btn_clear.move(483, 115)
        self.btn_clear.clicked.connect(self.create_new_recipe)

        self.btn_del_recipe = QPushButton('Удалить рецепт', self)
        self.btn_del_recipe.adjustSize()
        self.btn_del_recipe.move(570, 30)
        self.btn_del_recipe.clicked.connect(self.del_existing_recipe)

        self.btn_import_recipe = QPushButton('Импортировать рецепт', self)
        self.btn_import_recipe.adjustSize()
        self.btn_import_recipe.move(390, 55)
        self.btn_import_recipe.clicked.connect(self.import_recipe)

        self.btn_edit_recipe = QPushButton('Редактировать рецепт', self)
        self.btn_edit_recipe.adjustSize()
        self.btn_edit_recipe.move(570, 55)
        self.btn_edit_recipe.clicked.connect(self.edit_recipe)

        # Управление фильтрацией

        self.label_filter = QLabel('Команды для фильтрации рецептов', self)
        self.label_filter.adjustSize()
        self.label_filter.move(60, 10)

        self.btn_filter = QPushButton('Отфильтровать рецепты', self)
        self.btn_filter.adjustSize()
        self.btn_filter.move(25, 30)
        self.btn_filter.clicked.connect(self.filter_recipes)

        self.btn_cancel_filter = QPushButton('Отмена фильтрации', self)
        self.btn_cancel_filter.adjustSize()
        self.btn_cancel_filter.move(180, 30)
        self.btn_cancel_filter.clicked.connect(self.cancel_filter)

        # фильтры

        self.label_filter_in = QLabel('Фильтры для рецептов', self)
        self.label_filter_in.adjustSize()
        self.label_filter_in.move(90, 90)

        self.filter_name = QLineEdit(self)
        self.filter_name.move(150, 140)

        self.name_label = QLabel('Название', self)
        self.name_label.adjustSize()
        self.name_label.move(20, 145)

        self.filter_time = QTimeEdit(self)
        self.filter_time.move(150, 110)

        self.time_label = QLabel('Время приготовления', self)
        self.time_label.adjustSize()
        self.time_label.move(20, 115)

        self.filter_products = QLineEdit(self)
        self.filter_products.move(150, 170)

        self.products_label = QLabel('Продукты', self)
        self.products_label.adjustSize()
        self.products_label.move(20, 175)

        # Поле для вывода рецепта

        self.recipe_text = QPlainTextEdit(self)
        self.recipe_text.setGeometry(100, 100, 400, 400)
        self.recipe_text.move(350, 140)

        self.label_recipe_text = QLabel('Поле для вывода и редактирования рецепта', self)
        self.label_recipe_text.adjustSize()
        self.label_recipe_text.move(430, 100)

        self.products_edit = QLineEdit(self)
        self.products_edit_label = QLabel('Продукты:', self)
        self.products_edit_label.adjustSize()
        self.products_edit.setFixedSize(300, 30)
        self.products_edit.move(430, 550)
        self.products_edit_label.move(360, 555)

        self.time_edit = QTimeEdit(self)
        self.time_edit_label = QLabel('Время приготовления: ', self)
        self.time_edit_label.adjustSize()
        self.time_edit.move(570, 620)
        self.time_edit_label.move(440, 625)

        self.name_edit = QLineEdit(self)
        self.name_edit_label = QLabel('Название рецепта:', self)
        self.name_edit.setFixedSize(160, 30)
        self.name_edit_label.adjustSize()
        self.name_edit.move(570, 585)
        self.name_edit_label.move(440, 590)

        self.products_edit.setReadOnly(True)
        self.time_edit.setReadOnly(True)
        self.name_edit.setReadOnly(True)

        self.categ_name_category = {}

        self.recipes = {}

        self.recipes_parameters = {}

        # кнопки для принятия или отмены изменений

        self.btn_save_changes = QPushButton('Сохранить изменения', self)
        self.btn_save_changes.adjustSize()
        self.btn_save_changes.move(620, 115)
        self.btn_save_changes.clicked.connect(self.save_changes_recipe_redaction)
        self.btn_save_changes.hide()

        self.btn_cancel_changes = QPushButton('Отменить изменения', self)
        self.btn_cancel_changes.adjustSize()
        self.btn_cancel_changes.move(350, 115)
        self.btn_cancel_changes.clicked.connect(self.cancel_changes_recipe_redaction)
        self.btn_cancel_changes.hide()

        self.recipe_which_is_redacted = ''
        self.category_of_recipe_which_is_redacted = ''
        self.curr_shown = ''
        self.products = ''

        self.recipe_text.setReadOnly(True)

        self.can_save_recipe = False

        self.id_of_curr_user = None

    def add_new_category(self, is_being_uploaded=False, curr_step=0):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        if is_being_uploaded:
            name_from_user = list(self.recipes.keys())[curr_step]
            ok_pressed = True
        else:
            name_from_user = ''
            error = 'Как назовём?'
            ok_pressed = False
            while len(name_from_user) > 100 or not name_from_user or not ok_pressed:
                name_from_user, ok_pressed = QInputDialog.getText(self, "Введите название категории",
                                                                  error)
                if not ok_pressed:
                    return
                elif len(name_from_user) > 100:
                    error = 'Название категории не должно превышать 100 символов!'
                elif not name_from_user:
                    error = 'Название категории не может быть пустым!'
        if ok_pressed:
            if self.categ_name_category.get(name_from_user) is None:
                curr_n = len(self.categ_name_category.items())
                if curr_n >= 9:
                    self.statusBar().showMessage('⚠️ Достигнуто максимально количество категорий! ⚠️')
                    self.statusBar().setStyleSheet('color: black; background: yellow')
                else:
                    new_name = QLineEdit(name_from_user, self)
                    new_name.show()
                    new_name.setReadOnly(True)
                    new = QListWidget(self)
                    new.setFixedSize(100, 100)
                    new.show()
                    new.itemClicked.connect(self.print_recipe)
                    self.categ_name_category[name_from_user] = [new, new_name]
                    if not is_being_uploaded:
                        self.recipes[name_from_user] = {}
                        self.recipes_parameters[name_from_user] = {}
                    new_name.move(20 + 110 * (curr_n % 3), 205 + 133 * (curr_n // 3))
                    new.move(20 + 110 * (curr_n % 3), 235 + 133 * (curr_n // 3))
                    self.save_user_data()
            else:
                self.statusBar().showMessage('⚠️ Категория с таким названием уже существует! ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
                pass

    def del_existing_category(self):
        try:
            self.statusBar().clearMessage()
            self.statusBar().setStyleSheet('')
            if self.categ_name_category.keys():
                category, ok_pressed = QInputDialog.getItem(
                    self, "Выберите категорию для удаления", "Какую категорию удаляем?",
                    (self.categ_name_category.keys()), 0, False)
                if ok_pressed:
                    btn_reply = QMessageBox.question(self, 'Уточнение', 'Все рецепты, хранящиеся в категории, будут '
                                                                        'безвозвратно удалены! Вы точно хотите удалить '
                                                                        f'категорию: "{category}"?')
                    if btn_reply.value != 65536:
                        self.categ_name_category[category][0].hide()
                        self.categ_name_category[category][1].hide()
                        self.categ_name_category.pop(category)
                        if self.curr_shown in self.recipes[category].keys():
                            self.clear()
                            self.name_edit.clear()
                            self.time_edit.setTime(QTime(0, 0))
                            self.products_edit.clear()
                        self.recipes.pop(category)
                        for el in self.categ_name_category.values():
                            new_name = el[1]
                            new = el[0]
                            curr_n = list(self.categ_name_category.values()).index(el)
                            new_name.move(20 + 110 * (curr_n % 3), 205 + 133 * (curr_n // 3))
                            new.move(20 + 110 * (curr_n % 3), 235 + 133 * (curr_n // 3))
            else:
                self.statusBar().showMessage('⚠️ Отсуствуют категории для удаления! ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
            self.save_user_data()
        except Exception as e:
            print(repr(e))

    def clear(self):
        self.curr_shown = None
        self.recipe_text.clear()

    def create_new_recipe(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        self.can_save_recipe = True
        if self.categ_name_category:
            self.set_all_enabled_or_disabled(False)
            self.btn_add_recipe.setEnabled(True)
            self.name_edit.clear()
            self.products_edit.clear()
            self.time_edit.setTime(QTime(0, 0))
            self.curr_shown = None
            self.recipe_text.setReadOnly(False)
            self.recipe_text.clear()
            products = '!'
            ok_pressed3 = True
            text_in = ''
            error = 'Продукты с маленькой буквы и через запятую'
            while not self.check_products(products) or not ok_pressed3:
                products, ok_pressed3 = QInputDialog.getText(self, "Введите продукты для рецепта",
                                                             error, text=text_in)
                text_in = products
                if not self.check_products(products):
                    error = 'Введенные продукты не соответствуют формату!'
                if not ok_pressed3:
                    self.can_save_recipe = False
                    self.recipe_text.setReadOnly(True)
                    self.set_all_enabled_or_disabled(True)
                    return
            self.products = products
            self.products_edit.setText(products)
        else:
            self.statusBar().showMessage('⚠️ Нет категорий, куда можно будет сохранить рецепт! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')

    def add_new_recipe(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        if self.can_save_recipe:
            if self.categ_name_category.keys():
                category, ok_pressed = QInputDialog.getItem(
                    self, "Выберите категорию для хранения", "В какую категорию добавляем?",
                    (self.categ_name_category.keys()), 0, False)
                if ok_pressed:
                    curr_recepies = self.recipes[category].values()
                    add = None
                    if any(list(map(lambda x: self.check_identity(text1=self.recipe_text.toPlainText(), text2=x),
                                    curr_recepies))):
                        fuck = ' '.join(list(map(lambda y: list(filter(lambda z: z[1] == y,
                                                                       self.recipes[category].items()))[0][0],
                                                 list(filter(lambda x: self.check_identity(text1=x,
                                                                                           text2=self.recipe_text.
                                                                                           toPlainText()),
                                                             self.recipes[category].values())))))
                        buttonReply = QMessageBox.question(self, 'Уточнение', "Такой рецепт уже существует в данной"
                                                                              f"категории под названием(-ями) "
                                                                              f"'{fuck}'"
                                                                              ", всё равно добавить?")

                        if buttonReply.value != 65536:
                            add = True
                        else:
                            add = False
                    if add is None or add:
                        time = ''
                        ok_pressed4 = False
                        while not ok_pressed4:
                            time, ok_pressed4 = QInputDialog.getInt(self, "Введите время", "Время в минутах", 15, 0,
                                                                    1439)
                            if not ok_pressed4:
                                return
                        if ok_pressed4:
                            self.time_edit.setTime(QTime(int(time) // 60, int(time) % 60))
                            name_for_recipe_from_user = ''
                            ok_pressed2 = True
                            show_str = 'Как назовём?'
                            demand_1 = ' '.join([' '.join(y) for y in [i.keys() for i in self.recipes.values()]])
                            while (not name_for_recipe_from_user or not ok_pressed2
                                   or name_for_recipe_from_user in self.recipes[category].keys() or
                                   len(name_for_recipe_from_user) > 100):
                                name_for_recipe_from_user, ok_pressed2 = QInputDialog.getText(self,
                                                                                              "Введите название "
                                                                                              "рецепта", show_str)
                                if not ok_pressed2:
                                    return
                                if name_for_recipe_from_user in demand_1 and name_for_recipe_from_user:
                                    show_str = 'Рецепт с таким именем уже существует!'
                                elif len(name_for_recipe_from_user) > 100:
                                    show_str = 'Назвение рецепта должно не превышать 100 символов!'
                                elif not name_for_recipe_from_user:
                                    show_str = 'Название не может быть пустой строкой!'

                            if ok_pressed2:
                                self.name_edit.setText(name_for_recipe_from_user)
                                self.categ_name_category[category][0].addItem(name_for_recipe_from_user)
                                self.recipes[category][name_for_recipe_from_user] = self.recipe_text.toPlainText()
                                self.recipes_parameters[category][name_for_recipe_from_user] = \
                                    [self.products.split(', '), int(time)]
                                self.recipe_text.setReadOnly(True)
                                self.curr_shown = name_for_recipe_from_user
                                self.set_all_enabled_or_disabled(True)
                                self.can_save_recipe = False
        else:
            self.statusBar().showMessage('⚠️ Для того, чтобы добавить рецепт нужно сначала его создать! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')
        self.save_user_data()

    def print_recipe(self, item):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        self.recipe_text.clear()
        self.recipe_text.setReadOnly(True)
        categ = dict((filter(lambda x: item.text() in x[1].keys(), list(self.recipes.items())))).keys()
        categ = (list(categ)[0])
        self.recipe_text.setPlainText(self.recipes[categ][item.text()])
        self.hide_or_show_edits(is_show=True)
        self.btn_save_changes.hide()
        self.btn_cancel_changes.hide()
        self.products_edit.setReadOnly(True)
        self.time_edit.setReadOnly(True)
        self.name_edit.setReadOnly(True)
        self.time_edit.setTime(QTime(self.recipes_parameters[categ][item.text()][1] // 60,
                                     self.recipes_parameters[categ][item.text()][1] % 60))
        self.products_edit.setText(', '.join(self.recipes_parameters[categ][item.text()][0]))
        self.products_edit.setCursorPosition(0)
        self.name_edit.setText(item.text())
        self.name_edit.setCursorPosition(0)
        self.curr_shown = item.text()

    def del_existing_recipe(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        if self.categ_name_category.keys():
            if self.recipe_text.toPlainText() and self.recipe_text.isReadOnly():
                btn_reply = QMessageBox.question(self, 'Уточнение', 'Удалить рецепт, который выбран или другой?')
                if btn_reply.value != 65536:
                    right_one = list(filter(lambda x: self.curr_shown in x[1].keys(), list(self.recipes.items())))
                    category = right_one[0][0]
                    self.categ_name_category[category][0].takeItem(
                        list(self.recipes[category].keys()).index(self.curr_shown))
                    self.recipes[category].pop(self.curr_shown)
                    self.products_edit.clear()
                    self.name_edit.clear()
                    self.time_edit.setTime(QTime(0, 0))
                    self.clear()
                    return
            category, ok_pressed = QInputDialog.getItem(
                self, "Выберите категорию откуда удаляем", "Из какой категории удаляем?",
                (self.categ_name_category.keys()), 0, False)
            if ok_pressed:
                if self.recipes[category].keys():
                    recipe, ok_pressed2 = QInputDialog.getItem(
                        self, "Выберите рецепт для удаления", "Какой рецепт удаляем?",
                        (self.recipes[category].keys()), 0, False)
                    if ok_pressed2:
                        self.categ_name_category[category][0].takeItem(
                            list(self.recipes[category].keys()).index(recipe))
                        self.recipes[category].pop(recipe)
                        self.products_edit.clear()
                        self.name_edit.clear()
                        self.time_edit.setTime(QTime(0, 0))
                        self.clear()

                else:
                    self.statusBar().showMessage('⚠️ В данной категории нет рецептов для удаления! ⚠️')
                    self.statusBar().setStyleSheet('color: black; background: yellow')
        else:
            self.statusBar().showMessage('⚠️ Нет категорий, откуда удалить рецепт! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')
        self.save_user_data()

    def import_recipe(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        a = self.create_new_recipe()
        if a is None:
            return
        self.can_save_recipe = True
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '',
            'Текстовик (*.txt)')[0]
        if fname:
            encode, ok_pressed2 = QInputDialog.getItem(
                self, "Выберите кодировку для файла", "Какая кодировка?",
                ('utf-8', 'Windows_1251'), 0, False)
            if ok_pressed2:
                with open(fname, 'r', encoding=encode) as file:
                    data = file.readlines()
                    s = ''.join(data)
                    self.recipe_text.setPlainText(s)

    def edit_recipe(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        is_curr = False
        if self.recipes:
            if self.recipe_text.toPlainText() and self.recipe_text.isReadOnly():
                btn_reply = QMessageBox.question(self, 'Уточнение',
                                                 'Редактируем рецепт, который выбран или другой?')
                if btn_reply.value != 65536:
                    right_one = list(filter(lambda x: self.curr_shown in x[1].keys(), list(self.recipes.items())))
                    category = right_one[0][0]
                    recipe = self.curr_shown
                    ok_pressed = True
                    ok_pressed2 = True
                    is_curr = True
            if not (self.recipe_text.toPlainText() and self.recipe_text.isReadOnly()) or not is_curr:
                category, ok_pressed = QInputDialog.getItem(
                    self, "Выберите категорию где лежит нужный вам рецепт", "Какая категория?",
                    (self.recipes.keys()), 0, False)
            self.category_of_recipe_which_is_redacted = category
            if self.recipes[category].keys():
                if ok_pressed:
                    if not is_curr:
                        recipe, ok_pressed2 = QInputDialog.getItem(
                            self, "Выберите нужный рецепт", "Какой рецепт будем редактировать?",
                            (self.recipes[category].keys()), 0, False)
                    self.recipe_which_is_redacted = recipe
                    if ok_pressed2:
                        self.set_all_enabled_or_disabled(False)
                        self.recipe_text.setPlainText(self.recipes[category][recipe])
                        self.hide_or_show_edits(is_show=True)
                        self.products_edit.setText(', '.join(self.recipes_parameters[category][recipe][0]))
                        self.time_edit.setTime(QTime(self.recipes_parameters[category][recipe][1] // 60,
                                                     self.recipes_parameters[category][recipe][1] % 60))
                        self.name_edit.setText(recipe)
                        self.products_edit.setReadOnly(False)
                        self.time_edit.setReadOnly(False)
                        self.name_edit.setReadOnly(False)
            else:
                self.statusBar().showMessage('⚠️ Нет рецептов в данной категории! ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')

        else:
            self.statusBar().showMessage('⚠️ Нет категорий для выбора редактирования рецепта! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')

    def save_changes_recipe_redaction(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        if self.check_products(self.products_edit.text()):
            new_text = self.recipe_text.toPlainText()
            new_name = self.name_edit.text()
            new_products = self.products_edit.text()
            new_time = int(self.time_edit.text().split(':')[0]) * 60 + int(self.time_edit.text().split(':')[1])
            demand_1 = ' '.join([' '.join(y) for y in [i.keys() for i in self.recipes.values()]])
            if len(new_name) > 100 or new_name in demand_1:
                self.statusBar().showMessage('⚠️ Название уже существует или название длиной более 100 символов!'
                                             ' ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
            else:
                self.recipes[self.category_of_recipe_which_is_redacted][self.recipe_which_is_redacted] = new_text
                self.recipes_parameters[self.category_of_recipe_which_is_redacted][self.recipe_which_is_redacted] = [
                    new_products.split(', '), int(new_time)]
                if new_name.strip() != self.recipe_which_is_redacted:
                    self.recipes[self.category_of_recipe_which_is_redacted][new_name] = \
                        self.recipes[self.category_of_recipe_which_is_redacted][
                            self.recipe_which_is_redacted]
                    self.recipes_parameters[self.category_of_recipe_which_is_redacted][new_name] = (
                        self.recipes_parameters)[
                        self.category_of_recipe_which_is_redacted][self.recipe_which_is_redacted]
                    del self.recipes[self.category_of_recipe_which_is_redacted][self.recipe_which_is_redacted]
                    del self.recipes_parameters[self.category_of_recipe_which_is_redacted][
                        self.recipe_which_is_redacted]
                self.update_list(category=self.category_of_recipe_which_is_redacted)
                self.set_all_enabled_or_disabled(True)
                self.btn_cancel_changes.hide()
                self.btn_save_changes.hide()
                self.name_edit.setCursorPosition(0)
                self.products_edit.setCursorPosition(0)
                self.products_edit.setReadOnly(True)
                self.time_edit.setReadOnly(True)
                self.name_edit.setReadOnly(True)
                self.curr_shown = new_name
                self.save_user_data()
        else:
            self.statusBar().showMessage('⚠️ Неправильный формат продуктов! Должен быть формат вида: "продукт1, '
                                         'продукт2, продукт3" ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')

    def cancel_changes_recipe_redaction(self):
        self.curr_shown = self.recipe_which_is_redacted
        self.set_all_enabled_or_disabled(True)
        self.btn_cancel_changes.hide()
        self.btn_save_changes.hide()
        self.recipe_text.setPlainText(self.recipes[self.category_of_recipe_which_is_redacted][self.
                                      recipe_which_is_redacted])
        self.name_edit.setText(self.recipe_which_is_redacted)
        time = self.recipes_parameters[self.category_of_recipe_which_is_redacted][self.recipe_which_is_redacted][1]
        self.time_edit.setTime(QTime(time // 60, time % 60))
        self.products_edit.setText(', '.join(
            self.recipes_parameters[self.category_of_recipe_which_is_redacted][self.recipe_which_is_redacted][0]))
        self.name_edit.setCursorPosition(0)
        self.products_edit.setCursorPosition(0)
        self.products_edit.setReadOnly(True)
        self.time_edit.setReadOnly(True)
        self.name_edit.setReadOnly(True)

    def hide_or_show_edits(self, is_show=False):
        self.products_edit.setVisible(is_show)
        self.products_edit_label.setVisible(is_show)
        self.time_edit.setVisible(is_show)
        self.time_edit_label.setVisible(is_show)
        self.name_edit.setVisible(is_show)
        self.name_edit_label.setVisible(is_show)
        self.btn_save_changes.setVisible(is_show)
        self.btn_cancel_changes.setVisible(is_show)

    def update_list(self, category):
        self.categ_name_category[category][0].clear()
        for recipe_n, recipe in self.recipes[category].items():
            self.categ_name_category[category][0].addItem(recipe_n)

    def filter_recipes(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        time = int(self.filter_time.text().split(':')[0]) * 60 + int(self.filter_time.text().split(':')[1])
        name = self.filter_name.text()
        products = self.filter_products.text()
        for k, v in self.categ_name_category.items():
            curr_category = v[0]
            curr_category: QListWidget
            items = list(self.recipes[v[1].text()].keys())
            if self.filter_time.text() != '0:00':
                items = list(filter(lambda y: time >= self.recipes_parameters[v[1].text()][y][1], items))
            if name:
                items = list(filter(lambda z: name.lower() in z.lower(), items))
            if self.check_products(products):
                items = list(
                    filter(lambda h: all(i.lower() in products for i in self.recipes_parameters[v[1].text()][h][0]),
                           items))
            elif not products:
                pass
            elif not self.check_products(products):
                self.statusBar().showMessage('⚠️ Сортировки по продуктам не произошло, потому что неправильный формат!'
                                             ' ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
            curr_category.clear()
            for recipe in items:
                curr_category.addItem(recipe)

    def cancel_filter(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        if self.categ_name_category:
            self.filter_name.clear()
            self.filter_products.clear()
            self.filter_time.setTime(QTime(0, 0))
            self.filter_recipes()

    def check_identity(self, text1, text2):
        i = -1
        n = 0
        all_of = len(text1.split('\n')) + len(text2.split('\n'))
        if len(text1.split('\n')) <= len(text2.split('\n')):
            for string in text1.split('\n'):
                i += 1
                if sorted(set(string.lower().split())) == sorted(set(text2.split('\n')[i].lower().split())):
                    n += 2
        elif len(text1.split('\n')) > len(text2.split('\n')):
            for string in text2.split('\n'):
                i += 1
                if sorted(set(string.lower().split())) == sorted(set(text1.split('\n')[i].lower().split())):
                    n += 2
        return (n / all_of) * 100 > 95

    def check_products(self, products):
        restricted = '1234567890=+!@#$%^&*()!"№;%:?<>/|\\[]{}\'.'
        if ', ' not in products and not products.isalpha():
            return False
        else:
            if any([i in restricted for i in products]) or not all(
                    [True if y else False for y in products.split(', ')]):
                return False
            else:
                return True

    def set_all_enabled_or_disabled(self, turn):
        self.btn_clear.setEnabled(turn)
        self.recipe_text.setReadOnly(turn)
        self.btn_add_recipe.setEnabled(turn)
        self.btn_del_recipe.setEnabled(turn)
        self.btn_edit_recipe.setEnabled(turn)
        self.btn_import_recipe.setEnabled(turn)
        self.btn_add_new_category.setEnabled(turn)
        self.btn_del_category.setEnabled(turn)
        self.btn_filter.setEnabled(turn)
        self.btn_cancel_filter.setEnabled(turn)
        self.filter_name.setEnabled(turn)
        self.filter_products.setEnabled(turn)
        self.filter_time.setEnabled(turn)
        for k, v in self.categ_name_category.items():
            v[0].setEnabled(turn)

        # Сохранение данных в БД

    def save_user_data(self):
        self.con = sqlite3.connect('RM_data.sqlite')
        self.cur = self.con.cursor()
        self.cur.execute(f"""UPDATE userData
                                    SET recipes = "{self.recipes}"
                                    WHERE id = {self.id_of_curr_user}
                                    """)
        self.con.commit()
        self.cur.execute(f"""UPDATE userData
                                    SET recipes_parameters = "{self.recipes_parameters}"                                
                                    WHERE id = {self.id_of_curr_user}
                                    """)
        self.con.commit()
        self.con.close()

    # Подгрузка данных при входе в систему
    def load_user_data(self, recipes, recipes_params, id_of_user):
        self.id_of_curr_user = id_of_user
        self.recipes = recipes
        self.recipes_parameters = recipes_params
        for cr_step in range(len(self.recipes.keys())):
            self.add_new_category(True, cr_step)
            self.update_list(list(self.recipes.keys())[cr_step])


# Класс для реализации Авторизации пользователя через БД
class Authorisation(QMainWindow):
    def __init__(self, w2):
        super().__init__()
        self.initUI()
        self.mainbro = w2

    def initUI(self):
        self.setFixedSize(200, 210)
        self.setWindowTitle('Авторизация')

        self.welcome_sign = QPixmap('_internal\welcome_sign.png')
        self.image = QLabel(self)
        self.image.adjustSize()
        self.image.resize(200, 132)
        self.image.move(0, 100)
        self.image.setPixmap(self.welcome_sign)

        self.login_btn = QPushButton('Войти', self)
        self.login_btn.move(50, 50)
        self.login_btn.clicked.connect(self.login)

        self.registrate_btn = QPushButton('Зарегестрироваться', self)
        self.registrate_btn.adjustSize()
        self.registrate_btn.move(40, 100)
        self.registrate_btn.clicked.connect(self.registrate)

        self.pswd_edit = QLineEdit(self)
        self.pswd_edit.move(50, 100)
        self.pswd_edit.hide()

        self.pswd_label = QLabel('Введите пароль', self)
        self.pswd_label.move(55, 75)
        self.pswd_label.adjustSize()
        self.pswd_label.hide()

        self.id_edit = QLineEdit(self)
        self.id_edit.move(50, 40)
        self.id_edit.hide()

        self.id_label = QLabel('Введите свой id', self)
        self.id_label.move(55, 15)
        self.id_label.adjustSize()
        self.id_label.hide()

        self.btn_create_acc = QPushButton('Создать аккаунт', self)
        self.btn_create_acc.move(50, 150)
        self.btn_create_acc.clicked.connect(self.create_new_acc)
        self.btn_create_acc.hide()

        self.btn_login = QPushButton('Войти в аккаунт', self)
        self.btn_login.move(50, 150)
        self.btn_login.clicked.connect(self.enter_existing_acc)
        self.btn_login.hide()

        self.error_label = QLabel(self)
        self.error_label.move(0, 175)

        self.can_exec_Manager = False

        self.recipes = {}
        self.recipes_parameters = {}

        self.con = sqlite3.connect('RM_data.sqlite')
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS "userData" ("id"	INTEGER NOT NULL UNIQUE,  "recipes"	TEXT NOT 
        NULL, "recipes_parameters" TEXT NOT NULL, "pswd" TEXT NOT NULL, PRIMARY KEY("id"))""")

    def registrate(self):
        self.image.hide()
        self.registrate_btn.hide()
        self.login_btn.hide()
        self.pswd_edit.show()
        self.pswd_label.show()
        self.id_edit.show()
        self.id_label.show()
        self.btn_create_acc.show()

    def login(self):
        self.image.hide()
        self.registrate_btn.hide()
        self.login_btn.hide()
        self.pswd_edit.show()
        self.pswd_label.show()
        self.id_edit.show()
        self.id_label.show()
        self.btn_login.show()

    def create_new_acc(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        password = self.pswd_edit.text()
        if self.pswd_edit.text():
            id = self.id_edit.text()
            if not id.isdigit():
                self.statusBar().showMessage('⚠️ id должен быть целым числом! ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
            elif not self.cur.execute(f"""SELECT id FROM userData WHERE id = {id}""").fetchall():
                self.cur.execute(
                    f"""INSERT INTO userData(id, recipes, recipes_parameters, pswd) VALUES({id}, "{dict()}",
                     "{dict()}", "{password}")""")
                self.con.commit()
                self.con.close()
                self.can_exec_Manager = True
                self.start_session(False)
                self.con.close()
            else:
                self.statusBar().showMessage('⚠️ Этот id занят! ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
        else:
            self.statusBar().showMessage('⚠️ Пароль не введен! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')

    def enter_existing_acc(self):
        self.statusBar().clearMessage()
        self.statusBar().setStyleSheet('')
        password = self.pswd_edit.text()
        id = self.id_edit.text()
        if not password or not id:
            self.statusBar().showMessage('⚠️ Пароль или id не заполнены! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')
        elif not id.isdigit():
            self.statusBar().showMessage('⚠️ id должен быть целым числом! ⚠️')
            self.statusBar().setStyleSheet('color: black; background: yellow')
        else:
            usr_dt = self.cur.execute(f"""SELECT id, recipes, recipes_parameters, pswd FROM userData WHERE id = {id}
                 and pswd = '{password}'""").fetchall()
            if not usr_dt:
                self.statusBar().showMessage('⚠️ Пароль или id неверные! ⚠️')
                self.statusBar().setStyleSheet('color: black; background: yellow')
            else:
                self.recipes = eval(usr_dt[0][1])
                recipes_params_raw = eval(usr_dt[0][2])
                for k, v in recipes_params_raw.items():
                    for k1, v1 in v.items():
                        recipes_params_raw[k][k1] = [v1[0], v1[1]]
                self.recipes_parameters = recipes_params_raw
                self.can_exec_Manager = True
                self.start_session(True)
                self.con.close()

    def start_session(self, logined):
        if self.can_exec_Manager:
            self.write_log(user_id=self.id_edit.text())
            self.setVisible(False)
            self.mainbro.show()
            if logined:
                self.mainbro.load_user_data(self.recipes, self.recipes_parameters, int(self.id_edit.text()))
            elif not logined:
                self.mainbro.id_of_curr_user = int(self.id_edit.text())

    def write_log(self, user_id):
        with open('_internal\log.txt', 'r') as log:
            text = log.read()
        with open('_internal\log.txt', 'w') as log:
            status = f'Пользователь с id: {user_id}, зашёл в систему в {datetime.today()}\n'
            log.write(text + status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Manager()
    user_authorisation = Authorisation(ex)
    user_authorisation.show()
    sys.exit(app.exec())
