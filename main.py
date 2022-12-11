import sys
import PyQt5
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QTime, QRect
from PyQt5.QtGui import QPainter, QColor
from random import choice, randint
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlRelationalDelegate
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox, \
    QGraphicsOpacityEffect, QDialog, QMessageBox, QTableView, QDateEdit, QDateTimeEdit, QListWidgetItem, QListWidget
from PyQt5.QtGui import QPixmap
import sqlite3

conn = sqlite3.connect('planirovshik.sqlite')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS Plan(
Id varchar(30),
Data varchar(30),
Time_start varchar(30),
Time_end varchar(30),
Job varchar(30),
Status_Job varchar(30))
""")
conn.commit()

#Главное окно
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):

        self.setGeometry(700, 100, 700, 700)
        self.setWindowTitle('Планировщик на день')
        self.spisokt = QLabel('Список дел', self)
        #self.spisokt.setStyleSheet("font:12pt;")
        self.spisokt.move(300, 30)

        self.jobs = QListWidget(self)
        self.jobs.setGeometry(QRect(80, 70, 530, 300))
        self.jobs.setStyleSheet("font:12pt;")
        self.jobs.setObjectName("jobs")


        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("planirovshik.sqlite")
        self.db.open()
        self.view = QTableView(self)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('Plan')
        self.model.select()
        self.view.setModel(self.model)
        self.view.move(50, 60)
        self.view.resize(0, 0)

        rows = self.model.rowCount()
        if not rows:
            return

        self.jobs.clear()

        for row in range(rows):
            id = self.model.record(row).value("Id")
            data = self.model.record(row).value("Data")
            ts = self.model.record(row).value("Time_start")
            te = self.model.record(row).value("Time_end")
            j = self.model.record(row).value("Job")
            sj = self.model.record(row).value("Status_Job")


            self.jobs.addItem(f" {data}  {ts}-{te}  -  {j}  -  {sj}")


        self.button_0 = QPushButton(self)
        self.button_0.move(245, 500)
        self.button_0.resize(170, 30)
        self.button_0.setText("Таблица")
        self.button_0.clicked.connect(self.run0)

        self.button_1 = QPushButton(self)
        self.button_1.move(245, 550)
        self.button_1.resize(170, 30)
        self.button_1.setText("Добавить дело")
        self.button_1.clicked.connect(self.run1)

        self.button_2 = QPushButton(self)
        self.button_2.move(245, 600)
        self.button_2.resize(170, 30)
        self.button_2.setText("Удалить дело")
        self.button_2.clicked.connect(self.run2)

    def run0(self):
        self.w = Window0()
        self.w.show()
        self.hide()

    def run1(self):
        self.w = Window1()
        self.w.show()
        self.hide()

    def run2(self):
        self.w = Window2()
        self.w.show()

class Window0(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таблица")
        self.setGeometry(700, 100, 700, 700)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("planirovshik.sqlite")
        self.db.open()
        self.view = QTableView(self)
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('Plan')
        self.model.select()
        self.view.setModel(self.model)
        self.view.move(50, 60)
        self.view.resize(600, 300)

        self.button_1 = QPushButton(self)
        self.button_1.move(245, 550)
        self.button_1.resize(170, 30)
        self.button_1.setText("Назад")
        self.button_1.clicked.connect(self.run1)

    def run1(self):
        self.w = Example()
        self.w.show()
        self.hide()


class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление дела")
        self.setGeometry(600, 100, 800, 700)

        self.idt = QLabel('Номер', self)
        self.idt.move(300, 30)
        self.id = QLineEdit(self)
        self.id.setObjectName("Номер")
        self.id.move(300, 60)
        self.id.resize(170, 30)


        self.data = QDateEdit(self)
        self.data.setCalendarPopup(True)
        self.data.setDate(QtCore.QDate.currentDate())
        self.data.setObjectName("Дата")
        self.data.move(300, 120)
        self.data.resize(170, 30)

        self.time_startt = QLabel('Время начала', self)
        self.time_startt.move(300, 150)
        self.time_start=QDateTimeEdit(QTime.currentTime(), self)
        self.time_start.setObjectName("Время начала")
        self.time_start.move(300, 180)
        self.time_start.resize(170, 30)

        self.time_endt = QLabel('Время конца', self)
        self.time_endt.move(300, 210)
        self.time_end =QDateTimeEdit(QTime.currentTime(), self)
        self.time_end.setObjectName("Время конца")
        self.time_end.move(300, 240)
        self.time_end.resize(170, 30)

        self.jobt = QLabel('Дело', self)
        self.jobt.move(300, 270)
        self.job = QLineEdit(self)
        self.job.setObjectName("Дело")
        self.job.move(300, 300)
        self.job.resize(170, 30)

        self.status_jobt = QLabel('Выполнено/Невыполнено', self)
        self.status_jobt.move(300, 330)
        self.status_job = QLineEdit(self)
        self.status_job.setObjectName("Выполнено/Невыполнено")
        self.status_job.move(300, 360)
        self.status_job.resize(170, 30)

        self.button_1 = QPushButton(self)
        self.button_1.move(300, 590)
        self.button_1.resize(170, 30)
        self.button_1.setText("Добавить дело")
        self.button_1.clicked.connect(self.run1)

        self.button_2 = QPushButton(self)
        self.button_2.move(300, 640)
        self.button_2.resize(170, 30)
        self.button_2.setText("Назад")
        self.button_2.clicked.connect(self.run2)

    def run1(self):
        i = str(self.id.text())
        d = str(self.data.text())
        ts = str(self.time_start.text())
        te = str(self.time_end.text())
        j = str(self.job.text())
        s = str(self.status_job.text())


        lineEdits = self.findChildren(QLineEdit)
        text = ''
        for lineEdit in lineEdits:
            if not lineEdit.text():
                print(f'Заполните {lineEdit.objectName()}')
                text = f'{text}Заполните {lineEdit.objectName()}\n'
        if text:
            msg = QtWidgets.QMessageBox.information(
                self, 'Внимание', text)
        else:
            msg = QtWidgets.QMessageBox.information(
                self, 'Информация', 'Все поля заполнены.')
            cur.execute(
                '''INSERT INTO Plan(Id, Data, Time_start, Time_end,Job, Status_Job) VALUES (?, ?, ?,?,?,?)''',
                (i, d,ts,te,j,s))
            conn.commit()

    def run2(self):
        self.w = Example()
        self.w.show()
        self.hide()

class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Удаление данных")
        self.setGeometry(750, 300, 500, 400)

        self.idt = QLabel('Выбери ID строки, которую нужно удалить', self)
        self.idt.move(120, 30)
        self.idt.resize(260, 30)
        self.id = QLineEdit(self)
        self.id.move(170, 60)
        self.id.resize(170, 30)

        self.button_1 = QPushButton(self)
        self.button_1.move(170, 240)
        self.button_1.resize(170, 30)
        self.button_1.setText("Удалить")
        self.button_1.clicked.connect(self.run1)

    def run1(self):
        i = str(self.id.text())

        cur.execute('''DELETE from Plan where Id = ?''', (i))
        conn.commit()
        print("Успешно удалено")
        msg = QMessageBox()
        msg.setWindowTitle("Успешно")
        msg.setText("Успешно удалено")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

        self.w = Example()
        self.w.show()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())