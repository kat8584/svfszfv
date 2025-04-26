from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json


app = QApplication([])

'''Заметки для параметра'''
notes = {
    "Добро пожаловать": {
       "текст": "Добро пожаловать в приложение <<Умные заметки>>!",
       "теги": ["приветствие", "иструкция"]
    }
}

#параметры окна приложения
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)




#виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')




button_note_create = QPushButton('Создать заметку') 
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')




field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')




#расположение виджетов по лэйаутам
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)




col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)




col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)




col_2.addLayout(row_3)
col_2.addLayout(row_4)




layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)


#Функционал предложения
def show_note():
    name = list_notes.selectedItems()[0].text()
    print(name)
    field_text.setText(notes[name]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[name]["теги"])
def add_note():
    note_name, ok  = QInputDialog.getText(
        notes_win, "Добавить заметку", "Название заметки: "
    )
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        list_notes.addItem(note_name)
def delete_note():
    name = list_notes.selectedItems()[0].text()
    del notes[name]
    field_text.clear()
    list_notes.clear()
    list_tags.clear()
    list_notes.addItems(notes)
    with open ("settings.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False)
def save_note():
    name = list_notes.selectedItems()[0].text()
    if list_notes.selectedItems:
        note_text = field_text.toPlainText()
        notes[name] = {"текст" : note_text, "теги" : []}
    with open ("settings.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False)
def add_tag():
    if list_notes.selectedItems:
        name = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[name]["теги"]:
            notes[name]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open ("settings.json", "w") as file:
            json.dump(notes, file, sort_keys = True )
    else: 
        print("Заметка для добавления тега не выбрана!")
def delete_tag():
    if list_notes.selectedItems:
        name = list_notes.selectedItems()[0].text()
        selected_tag = list_tags.selectedItems()[0].text()
        notes[name]["теги"].remove(selected_tag)
        list_tags.clear()
        list_tags.addItems(notes[name]["теги"])
    with open ("settings.json", "w") as file:
            json.dump(notes, file, sort_keys = True )
def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметки по тегу" and tag:
        tagged_notes = {}
        for name in notes:
            if tag in notes[name]["теги"]:
                tagged_notes[name] = notes[name]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(tagged_notes)
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")
    else: 
        pass





#запуск приложения
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(delete_note)
button_note_save.clicked.connect(save_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(delete_tag)
button_tag_search.clicked.connect(search_tag)
notes_win.show()
with open ("settings.json", "r", encoding="utf-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)
app.exec_()
