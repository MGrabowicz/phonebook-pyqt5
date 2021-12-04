import re

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QToolTip, QFileDialog

from database import mysqlConnection

emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phoneRegex = r'\b\d{9}\b'

class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 781)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pictureFrame = QtWidgets.QLabel(self.centralwidget)
        self.pictureFrame.setGeometry(QtCore.QRect(240, 180, 251, 256))
        self.pictureFrame.setPixmap(QtGui.QPixmap("phol.jpg"))
        self.pictureFrame.setScaledContents(True)
        self.pictureFrame.setObjectName("picture")
        self.pictureFrame.hide()

        self.searchLine = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLine.setGeometry(QtCore.QRect(20,680,120,21))
        self.searchLine.setObjectName("searchLine")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(140, 680, 91, 21))
        self.searchButton.setObjectName("searchButton")
        self.contactsList = QtWidgets.QListWidget(self.centralwidget)
        self.contactsList.setGeometry(QtCore.QRect(20, 30, 211, 650))
        self.contactsList.setObjectName("contactsList")
        self.contactsLabel = QtWidgets.QLabel(self.centralwidget)
        self.contactsLabel.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.contactsLabel.setObjectName("contactsLabel")
        self.nameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.nameLine.setGeometry(QtCore.QRect(290, 29, 201, 21))
        self.nameLine.setObjectName("nameLine")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(240, 30, 47, 13))
        self.nameLabel.setObjectName("nameLabel")
        self.surnameLine = QtWidgets.QLineEdit(self.centralwidget)
        self.surnameLine.setGeometry(QtCore.QRect(290, 59, 201, 21))
        self.surnameLine.setObjectName("surnameLine")
        self.surnameLabel = QtWidgets.QLabel(self.centralwidget)
        self.surnameLabel.setGeometry(QtCore.QRect(240, 60, 47, 13))
        self.surnameLabel.setObjectName("surnameLabel")
        self.emailLabel = QtWidgets.QLabel(self.centralwidget)
        self.emailLabel.setGeometry(QtCore.QRect(240, 120, 47, 13))
        self.emailLabel.setObjectName("emailLabel")
        self.mailLine = QtWidgets.QLineEdit(self.centralwidget)
        self.mailLine.setGeometry(QtCore.QRect(290, 119, 201, 21))
        self.mailLine.setObjectName("mailLine")
        self.phoneLine = QtWidgets.QLineEdit(self.centralwidget)
        self.phoneLine.setGeometry(QtCore.QRect(290, 89, 201, 21))
        self.phoneLine.setObjectName("phoneLine")
        self.phoneLabel = QtWidgets.QLabel(self.centralwidget)
        self.phoneLabel.setGeometry(QtCore.QRect(240, 90, 47, 13))
        self.phoneLabel.setObjectName("phoneLabel")
        self.createButton = QtWidgets.QPushButton(self.centralwidget)
        self.createButton.setGeometry(QtCore.QRect(20, 710, 91, 23))
        self.createButton.setObjectName("createButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(140, 710, 91, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(390, 150, 101, 23))
        self.saveButton.setObjectName("saveButton")
        self.pictureButton = QtWidgets.QPushButton(self.centralwidget)
        self.pictureButton.setGeometry(QtCore.QRect(290, 150, 101, 23))
        self.pictureButton.setObjectName("pictureButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 510, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        self.contactsList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.nameLine.setEnabled(False)
        self.surnameLine.setEnabled(False)
        self.mailLine.setEnabled(False)
        self.phoneLine.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.pictureButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

        self.contactsList.clicked.connect(self.listElementClickedEvent)
        self.createButton.clicked.connect(self.createButtonEvent)
        self.saveButton.clicked.connect(self.saveButtonEvent)
        self.deleteButton.clicked.connect(self.deleteButtonEvent)
        self.searchButton.clicked.connect(self.searchButtonEvent)
        self.pictureButton.clicked.connect(self.pictureButtonEvent)

        self.phoneLine.setToolTip("Provide number in polish format e.g.(783423643)")

        self.pictureFrame.setStyleSheet("border: 1px solid black;")

        self.editingContact = False

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Phonebook"))
        self.contactsLabel.setText(_translate("MainWindow", "Contacts"))
        self.nameLabel.setText(_translate("MainWindow", "Name:"))
        self.surnameLabel.setText(_translate("MainWindow", "Surname:"))
        self.emailLabel.setText(_translate("MainWindow", "E-mail:"))
        self.phoneLabel.setText(_translate("MainWindow", "Phone:"))
        self.createButton.setText(_translate("MainWindow", "Create"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.pictureButton.setText(_translate("MainWindow", "Picture"))

    def setupDatabase(self):
        #This defines connection with database and set starting list for contacts list.
        self.myConnection = mysqlConnection()
        self.myConnection.selectDatabase("phonebook")
        self.databasesList = self.myConnection.getContactsList()
        self.injectListToContactsList(self.databasesList)

    def createButtonEvent(self):
        #Event for 'Create' button
        self.editingContact = False
        self.contactEditingMode()
        self.createButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.contactsList.setEnabled(False)
        self.nameLine.setText("")
        self.surnameLine.setText("")
        self.mailLine.setText("")
        self.phoneLine.setText("")
        self.pictureFrame.show()
        self.pictureFrame.setPixmap(QtGui.QPixmap("noimage.png"))

    def deleteButtonEvent(self):
        #Event for 'Delete' button
        idContact = self.getSelectedContactID()
        self.myConnection.deleteContact(idContact)
        self.reloadContactsList()
        self.noSelectedContactMode()
        self.pictureFrame.hide()
        self.phoneLine.setStyleSheet("")
        self.mailLine.setStyleSheet("")

    def searchButtonEvent(self):
        # Event for 'Search' button
        searchCriteria = self.searchLine.text()
        self.contacts = self.myConnection.getSearchContactList(searchCriteria)
        self.contactsList.clear()
        self.injectListToContactsList(self.contacts)
        self.noSelectedContactMode()

    def saveButtonEvent(self):
        # Event for 'Save' button
        if not self.nameLine.text():
            QToolTip.showText(MainWindow.mapToGlobal(self.nameLine.pos()),"Name field is mandatory!")
            self.nameLine.setStyleSheet("border: 1px solid red;")
            return
        else:
            self.nameLine.setStyleSheet("")
            firstName = "'" + self.nameLine.text() + "'"

        email = self.mailLine.text()
        if (re.fullmatch(emailRegex, email)):
            self.mailLine.setStyleSheet("")
        else:
            QToolTip.showText(MainWindow.mapToGlobal(self.mailLine.pos()),"This doesn't look like email to me!")
            self.mailLine.setStyleSheet("border: 1px solid red;")

        number = self.phoneLine.text()
        if (re.fullmatch(phoneRegex, number)):
            self.phoneLine.setStyleSheet("")
        else:
            QToolTip.showText(MainWindow.mapToGlobal(self.phoneLine.pos()),"This doesn't look like phone number to me!")
            self.phoneLine.setStyleSheet("border: 1px solid red;")

        surname = self.prepareVarForInserting(self.surnameLine.text())
        email = self.prepareVarForInserting(self.mailLine.text())
        number = self.prepareVarForInserting(self.phoneLine.text())
        picture =  self.prepareVarForInserting(self.pictureFrame.windowFilePath())

        if not self.editingContact:
            self.myConnection.createNewContact(firstName, surname, email, number, picture)
            self.noSelectedContactMode()
            self.reloadContactsList()
        else:
            idContact = self.getSelectedContactID()
            self.myConnection.updateContact(idContact, firstName, surname, email, number, picture)
            self.reloadContactsList()
            selectedContact = self.contactsList.findItems(self.nameLine.text(), Qt.MatchExactly)
            self.contactsList.setCurrentItem(selectedContact[0])

    def pictureButtonEvent(self):
        # Event for 'Picture' button
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.gif *.png)")
        self.pictureFrame.setPixmap(QtGui.QPixmap(fname[0]))
        self.pictureFrame.setWindowFilePath(fname[0])

    def listElementClickedEvent(self):
        #Event for contactsList selected item
        self.editingContact = True
        idContact = self.getSelectedContactID()
        contactInfo = self.myConnection.getContact(idContact)
        self.nameLine.setText(contactInfo["firstname"])
        self.surnameLine.setText(contactInfo["surname"])
        self.mailLine.setText(contactInfo["email"])
        self.phoneLine.setText(contactInfo["number"])
        if contactInfo["picture"]:
            self.pictureFrame.setPixmap(QtGui.QPixmap(contactInfo["picture"]))
        else:
            self.pictureFrame.setPixmap(QtGui.QPixmap("noimage.png"))
        self.contactEditingMode()

    def contactEditingMode(self):
        # Enabling all buttons that should be usable when editing contact
        self.nameLine.setEnabled(True)
        self.surnameLine.setEnabled(True)
        self.mailLine.setEnabled(True)
        self.phoneLine.setEnabled(True)
        self.saveButton.setEnabled(True)
        self.deleteButton.setEnabled(True)
        self.pictureButton.setEnabled(True)
        self.nameLine.setStyleSheet("")
        self.mailLine.setStyleSheet("")
        self.phoneLine.setStyleSheet("")
        self.pictureFrame.show()

    def noSelectedContactMode(self):
        #Disabling all buttons that shouldn't be used when there isn't any contact selected
        self.createButton.setEnabled(True)
        self.contactsList.setEnabled(True)
        self.nameLine.setEnabled(False)
        self.nameLine.setText("")
        self.surnameLine.setEnabled(False)
        self.surnameLine.setText("")
        self.mailLine.setEnabled(False)
        self.mailLine.setText("")
        self.phoneLine.setEnabled(False)
        self.phoneLine.setText("")
        self.saveButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        self.pictureButton.setEnabled(False)
        self.pictureFrame.hide()
        self.phoneLine.setStyleSheet("")
        self.mailLine.setStyleSheet("")
        self.nameLine.setStyleSheet("")

    def reloadContactsList(self):
        #This reload all contacts in contactsList
        self.contactsList.clear()
        self.contacts = self.myConnection.getContactsList()
        self.injectListToContactsList(self.contacts)

    def prepareVarForInserting(self, variable):
        #Prepare variable for sql query:
        #   - empty variable is changed to NULL
        #   - variable containing text has ' added
        if variable == "":
            variable = "NULL"
        else:
            variable = "'" + variable + "'"
        return variable

    def injectListToContactsList(self, list):
        #Inserts dict of contacts into contactsList
        for key in sorted(list, reverse = True):
            item = QtWidgets.QListWidgetItem(key)
            item.setData(Qt.UserRole, int(list[key]))
            self.contactsList.insertItem(0, item)

    def getSelectedContactID(self):
        #Returns ID of a contact that is selected on contacts list
        return self.contactsList.model().data(self.contactsList.selectedIndexes()[0], QtCore.Qt.UserRole)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.setupDatabase()
    MainWindow.show()
    sys.exit(app.exec_())
