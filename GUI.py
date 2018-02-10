import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QMainWindow,
    QGridLayout, QLabel, QLineEdit, QTextEdit, QScrollBar, QFrame, QGroupBox, QVBoxLayout, QHBoxLayout, QMenuBar,
    QAction, QFileDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import * # QCoreApplication  #для сигналів
from validator import *
import csv
import json

class ImportList(QWidget):
    def __init__(self):
        pass


class Application(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def history_frame(self):
        """
        empty for history with title and list found email
        :return: frame with history
        """
        font_title = QFont()
        font_title.setPointSize(15)
        font_title.setFamily("Comic Sans MS")
        font_title.setBold(True)

        title_history = QLabel("History")
        title_history.setStyleSheet("background-color: rgb(125, 125, 125)")
        title_history.setFixedHeight(25)
        title_history.setFont(font_title)
        title_history.setAlignment(Qt.AlignCenter)

        font_history = QFont()
        font_history.setPointSize(10)
        font_history.setFamily('Souvenir Lt BT')

        field_history = QLabel("Some Text")
        field_history.setFont(font_history)
        field_history.setAlignment(Qt.AlignTop)

        box_history = QVBoxLayout()
        box_history.addWidget(title_history)
        box_history.addWidget(field_history)

        frame_history = QFrame()
        frame_history.setLayout(box_history)
        frame_history.setStyleSheet("background-color: rgb(148, 148, 148)")
        return frame_history


    def item_frame(self):
        """

        :return:
        """

        frame_item = QFrame()
        frame_item.setStyleSheet("background-color: rgb(200, 255, 255)")
        frame_item.setVisible(True)  #Visible frame
        return frame_item

    def central_widget(self):
        """
        create central widget

        :return:
        """
        label_email = QLabel("Enter Email:")
        line_email = QLineEdit()
        btn_validator = QPushButton('Valid')
        status_email = QLabel("Status Email:")
        self.is_valid =  QLabel("Empty status")

        frame_item = self.item_frame()
        frame_history = self.history_frame()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(label_email, 0, 0)
        grid.addWidget(line_email, 1, 0, 1, 3)
        grid.addWidget(btn_validator, 1, 3)
        grid.addWidget(status_email, 2, 0)
        grid.addWidget(frame_item, 3, 0, 7, 6)
        grid.addWidget(self.is_valid, 2, 1)
        grid.addWidget(frame_history,0, 6, 10, 10)

        window = QWidget(self)
        window.setLayout(grid)
        self.setCentralWidget(window)


    def center_window(self):
        """
        centering window
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() #Centrring Windows
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def import_list(self):
        """
        Call class ImportList and return list with emails
        :return:
        """
        self.listData = QTextEdit()
        fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
        print(fname)
        fileformat = Formater.findFormat(fname)
        if fileformat:
            if fname:
                try:
                    if fileformat == 'txt':
                        self.listData = []
                        f = open(fname, 'r')
                        with f:
                            self.listData = f.read().split("\n")
                        self.setStatusTip('The list has been uploaded')
                    if fileformat == 'csv':
                        with open(fname, 'r', encoding='utf-8') as fcsv:
                            reader = csv.reader(fcsv, delimiter=',')
                            self.listData = []
                            for row in reader:
                                self.listData.append(row)
                        self.setStatusTip('The list has been uploaded')
                    if fileformat == 'json':
                        with open(fname, 'r', encoding='utf-8') as f_json:
                            self.listData = json.load(f_json)
                except:
                    self.setStatusTip('Error in data')
                    self.listData = None
            else:
                self.setStatusTip("The list hasn't been uploaded")
        else:
            self.setStatusTip("Invalid data format")


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def menu_bar(self):

        importList = QAction(QIcon(''), '&Import', self)
        importList.setShortcut('Ctrl+I')
        importList.setStatusTip("Import list with emails")
        importList.triggered.connect(self.import_list)

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(app.quit)

        info_program = QAction(QIcon(''), '&Information', self)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(importList)
        fileMenu.addAction(exitAction)
        info = menubar.addMenu("&Info")
        info.addAction(info_program)

    def initUI(self):

        self.menu_bar()
        self.central_widget()
        self.center_window()
        self.setWindowTitle('Email Validator')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(600, 440)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())