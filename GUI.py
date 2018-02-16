import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QMessageBox, QDesktopWidget, QMainWindow,
    QGridLayout, QLabel, QLineEdit, QTextEdit, QScrollBar, QFrame, QGroupBox, QVBoxLayout, QHBoxLayout, QMenuBar,
    QAction, QFileDialog, QScrollArea, QFormLayout, QProgressBar)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import * # QCoreApplication  #для сигналів
from validator import *
import csv
import json
import datetime
import time

class ImportList(QWidget):

    def __init__(self, listData):
        super().__init__()
        self.data = listData
        self.setWindowTitle('Import List')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(800, 440)
        self.show()


class HistoryWidget(QWidget):

    def __init__(self, email, result, parent=None):
        super(HistoryWidget, self).__init__(parent)

        self.labelEmail = QLabel(email+result)
        self.searchTime = QLabel(str(datetime.datetime.now().time())[:-7])
        layout = QVBoxLayout()
        layout.addWidget(self.labelEmail)
        layout.addWidget(self.searchTime)
        self.setLayout(layout)


class Application(QMainWindow):

    def __init__(self):
        super().__init__()
        self.listData = []
        self.current_count = 0
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
        font_history = QFont()
        font_history.setPointSize(10)
        font_history.setFamily('Souvenir Lt BT')

        title_history = QLabel("History")
        title_history.setStyleSheet("background-color: rgb(125, 125, 125)")
        title_history.setFixedHeight(25)
        title_history.setFont(font_title)
        title_history.setAlignment(Qt.AlignCenter)

        self.scrollLayout = QFormLayout()

        # scroll area widget contents
        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)

        # scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)

        box_history = QVBoxLayout()
        box_history.addWidget(title_history)
        box_history.addWidget(self.scrollArea)

        self.frame_history = QFrame()
        self.frame_history.setLayout(box_history)
        self.frame_history.setStyleSheet("background-color: rgb(148, 148, 148)")


    def addEmail(self, email, result):
        self.scrollLayout.addRow(HistoryWidget(email, result))



    def update_item_img(self, erorr_list):
        """
        :return:
        """
        self.email_syntax_img.setPixmap(self.true_img)
        self.disposable_domain_img.setPixmap(self.true_img)
        self.isp_syntax_img.setPixmap(self.true_img)
        self.domain_validity_img.setPixmap(self.true_img)
        self.mail_exchanger_img.setPixmap(self.true_img)
        self.smpt_connection_img.setPixmap(self.true_img)
        self.mailbox_existence_img.setPixmap(self.true_img)
        if erorr_list is not None:
            for error in erorr_list:
                if error == "Email Syntax":
                    self.email_syntax_img.setPixmap(self.false_img)
                if error == "Known Disposable Email Domain":
                    self.disposable_domain_img.setPixmap(self.false_img)
                if error == "ISP-Specific Syntax":
                    self.isp_syntax_img.setPixmap(self.false_img)
                if error == "Domain Validity":
                    self.domain_validity_img.setPixmap(self.false_img)
                if error == "Mail Exchanger (MX) records":
                    self.mail_exchanger_img.setPixmap(self.false_img)
                if error == "SMTP Connection":
                    self.smpt_connection_img.setPixmap(self.false_img)
                if error == "Mailbox Existence":
                    self.mailbox_existence_img.setPixmap(self.false_img)


    def updateProgressBar(self):
        """
        update Progress Bar
        :return:
        """
        self.import_frame.setVisible(True)
        self.progress_bar.setValue(self.persent_data)
        self.current_file.setText(str(self.current_count).strip())
        self.all_files.setText("with " + str(self.listData.__len__()))


    def ImportdLayout(self):
        """
        Layout for import data:
        :return:
        """
        self.progress_bar = QProgressBar(self)
        self.label_download = QLabel("Download:")
        self.current_file = QLabel(str(self.current_count).strip())
        self.all_files = QLabel("with " + str(self.listData.__len__()))

        self.donwload_layout = QHBoxLayout()
        self.donwload_layout.addWidget(self.label_download)
        self.donwload_layout.addWidget(self.current_file)
        self.donwload_layout.addWidget(self.all_files)

        self.import_layout = QVBoxLayout()
        self.import_layout.addWidget(self.progress_bar)
        self.import_layout.addLayout(self.donwload_layout)

        self.import_frame = QFrame()
        self.import_frame.setLayout(self.import_layout)
        self.import_frame.setVisible(False)


    def loadingData(self):
        if self.listData != []:
            self.current_count = 1
            self.frame_item.setVisible(False)
            self.is_valid.setText("Download...")
            data_len = self.listData.__len__()
            self.persent_data = 0
            self.updateProgressBar()
            for data in self.listData:
                self.persent_data =  self.current_count / data_len * 100
                self.updateProgressBar()
                self.emailValidatorForData(data)
                self.current_count += 1


    def saveEmail(self, new_data, name_file):
        """
        Save email in file
        :return:
        """
        try:
            with open(name_file, 'r',  encoding='utf-8') as old_file:
                data = json.load(old_file)
        except:
            data = []
            with open(name_file, 'w', encoding='utf-8') as old_file:
                json.dump(data,old_file, indent=4)
        finally:
            data.append(new_data)
            with open(name_file, 'w', encoding='utf-8') as new_file:
                json.dump(data, new_file, indent=4)


    def emailValidatorForData(self, email):
        """

        :param email:
        :return:
        """
        self.validator.setEmail(email)
        self.validator.find_email_at_site()
        result = self.validator.get_result()
        if result == "The Email is valid":
            self.addEmail(email, "is valid")
            data = {
                'email': email
            }
            self.saveEmail(data, "true_emails.json")
        elif result == "The email is not valid":
            errors = self.validator.get_error_email()
            self.addEmail(email, "is not valid")
            data = {
                'email': email,
                'error': errors
            }
            self.saveEmail(data,"wrond_emails.json")
        else:
            pass


    def item_frame(self):
        """
        Creating item_frame
        :return:
        """
        self.true_img = QPixmap("true.png")
        self.true_img = self.true_img.scaled(64, 50)
        self.false_img = QPixmap("false.png")
        self.false_img = self.false_img.scaled(64, 50)

        self.test_img = QPixmap("logo.png")
        self.test_img = self.test_img.scaled(64, 50)

        email_syntax = QLabel("Email Syntax:")
        self.email_syntax_img = QLabel()
        self.email_syntax_img.setPixmap(self.true_img)
        email_syntax_loyout = QHBoxLayout()
        email_syntax_loyout.addWidget(email_syntax)
        email_syntax_loyout.addWidget(self.email_syntax_img)

        disposable_domain = QLabel("Known Disposable Email Domain:")
        self.disposable_domain_img = QLabel()
        self.disposable_domain_img.setPixmap(self.false_img)
        disposable_domain_layout = QHBoxLayout()
        disposable_domain_layout.addWidget(disposable_domain)
        disposable_domain_layout.addWidget(self.disposable_domain_img)

        isp_syntax = QLabel("ISP-Specific Syntax:")
        self.isp_syntax_img = QLabel()
        self.isp_syntax_img.setPixmap(self.test_img)
        isp_syntax_layout = QHBoxLayout()
        isp_syntax_layout.addWidget(isp_syntax)
        isp_syntax_layout.addWidget(self.isp_syntax_img)

        domain_validity = QLabel("Domain Validity:")
        self.domain_validity_img = QLabel()
        self.domain_validity_img.setPixmap(self.test_img)
        domain_validity_layout = QHBoxLayout()
        domain_validity_layout.addWidget(domain_validity)
        domain_validity_layout.addWidget(self.domain_validity_img)

        mail_exchanger = QLabel("Mail Exchanger (MX) records:")
        self.mail_exchanger_img = QLabel()
        self.mail_exchanger_img.setPixmap(self.test_img)
        mail_exchanger_layout = QHBoxLayout()
        mail_exchanger_layout.addWidget(mail_exchanger)
        mail_exchanger_layout.addWidget(self.mail_exchanger_img)

        smpt_connection = QLabel("SMTP Connection:")
        self.smpt_connection_img = QLabel()
        self.smpt_connection_img.setPixmap(self.test_img)
        smpt_connection_layout = QHBoxLayout()
        smpt_connection_layout.addWidget(smpt_connection)
        smpt_connection_layout.addWidget(self.smpt_connection_img)

        mailbox_existence = QLabel("Mailbox Existence:")
        self.mailbox_existence_img = QLabel()
        self.mailbox_existence_img.setPixmap(self.test_img)
        mailbox_existence_layout = QHBoxLayout()
        mailbox_existence_layout.addWidget(mailbox_existence)
        mailbox_existence_layout.addWidget(self.mailbox_existence_img)

        frame_layout = QVBoxLayout()
        frame_layout.addLayout(email_syntax_loyout)
        frame_layout.addLayout(disposable_domain_layout)
        frame_layout.addLayout(isp_syntax_layout)
        frame_layout.addLayout(domain_validity_layout)
        frame_layout.addLayout(mail_exchanger_layout)
        frame_layout.addLayout(smpt_connection_layout)
        frame_layout.addLayout(mailbox_existence_layout)

        #Create Main Frame for email item
        self.frame_item = QFrame()
        self.frame_item.setLayout(frame_layout)
        self.frame_item.setVisible(False)
        self.frame_item.setStyleSheet("background-color: rgb(200, 255, 255)")

          #Visible frame

    def central_widget(self):
        """
        create central widget

        :return:
        """
        self.label_email = QLabel("Enter Email:")
        self.line_email = QLineEdit()
        self.btn_validator = QPushButton('Valid')
        self.status_email = QLabel("Status Email:")
        self.is_valid =  QLabel("Empty status")

        self.item_frame()
        self.history_frame()
        self.ImportdLayout()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label_email, 0, 0)
        self.grid.addWidget(self.line_email, 1, 0, 1, 3)
        self.grid.addWidget(self.btn_validator, 1, 3)
        self.grid.addWidget(self.status_email, 2, 0)
        self.grid.addWidget(self.frame_item, 3, 0, 6, 3)
        self.grid.addWidget(self.is_valid, 2, 1)
        self.grid.addWidget(self.frame_history,0, 4, 10, 10)
        self.grid.addWidget(self.import_frame, 3, 0, 4, 2)

        window = QWidget(self)
        window.setLayout(self.grid)

        self.setCentralWidget(window)
        self.btn_validator.clicked.connect(self.buttonClickedValid)


    def buttonClickedValid(self):
        """
        :return:
        """
        if self.line_email.text().strip() is not None and self.line_email.text().strip() != "":
            self.emailValidator(self.line_email.text().strip())


    def emailValidator(self, email):
        """
        :param email:
        :return:
        """
        self.validator.setEmail(email)
        self.validator.find_email_at_site()
        result = self.validator.get_result()
        print(result)
        if result == "The Email is valid":
            self.is_valid.setText(email + " " + "is a valid Email address")
            self.is_valid.setStyleSheet("color: green")
            self.frame_item.setVisible(False)
            self.addEmail(email, "is valid")

        elif result == "The email is not valid":
            self.is_valid.setText(email + " " + "does not appear to be a valid Email address")
            self.is_valid.setStyleSheet("color: red")
            errors = self.validator.get_error_email()
            #print(errors)
            self.update_item_img(errors)
            self.frame_item.setVisible(True)
            self.addEmail(email, "is not valid")
        else:
            self.is_valid.setText("Error, Try again")
            self.is_valid.setStyleSheet("color: yellow")
            self.frame_item.setVisible(False)




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
                if fileformat == 'txt':
                    self.listData = []
                    f = open(fname, 'r')
                    with f:
                        self.listData = f.read().split("\n")
                    self.setStatusTip('The list has been uploaded')
                    self.loadingData()
                elif fileformat == 'csv':
                    with open(fname, 'r', encoding='utf-8') as fcsv:
                        reader = csv.reader(fcsv, delimiter=',')
                        self.listData = []
                        for row in reader:
                            self.listData.append(row)
                    self.setStatusTip('The list has been uploaded')
                    self.loadingData()
                elif fileformat == 'json':
                    with open(fname, 'r', encoding='utf-8') as f_json:
                        self.listData = json.load(f_json)
                    self.loadingData()
                else:
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
            self.validator.close()
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
        exitAction.triggered.connect(self.validator.close)
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

        self.validator = Validator()
        self.menu_bar()
        self.central_widget()
        self.center_window()
        self.setWindowTitle('Email Validator')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(800, 440)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())