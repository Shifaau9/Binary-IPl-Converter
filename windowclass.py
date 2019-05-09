# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IPLConverter.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import os
import struct

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # binary ipl format found here https://gtamods.com/wiki/Item_Placement

        self.header_format = "4s18i"
        self.inst_format = "7f3i"
        self.cars_format = "4f8i"
        self.header_size = struct.calcsize(self.header_format)
        self.inst_size = struct.calcsize(self.inst_format)
        self.cars_size = struct.calcsize(self.cars_format)
        self.text = ""
        self.file = None
        self.file_path = ""

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("IPL Converter")
        MainWindow.resize(581, 312)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 581, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuBatch_Conversion = QtWidgets.QMenu(self.menubar)
        self.menuBatch_Conversion.setObjectName("menuBatch_Conversion")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionBinary_Text = QtWidgets.QAction(MainWindow)
        self.actionBinary_Text.setObjectName("actionBinary_Text")
        self.actionText_Binary = QtWidgets.QAction(MainWindow)
        self.actionText_Binary.setObjectName("actionText_Binary")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionClose)
        self.menuBatch_Conversion.addAction(self.actionBinary_Text)
        self.menuBatch_Conversion.addAction(self.actionText_Binary)
        self.menuAbout.addAction(self.actionHelp)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuBatch_Conversion.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IPL Conveter"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuBatch_Conversion.setTitle(_translate("MainWindow", "Batch Conversion"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionBinary_Text.setText(_translate("MainWindow", "Binary - > Text"))
        self.actionText_Binary.setText(_translate("MainWindow", "Text -> Binary"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.triggered.connect(self.save_file_as)
        self.actionClose.triggered.connect(self.close_file)
        self.actionHelp.triggered.connect(self.help_popup)
        self.actionBinary_Text.triggered.connect(self.batch_bin2text)

    def open_file(self):
        if self.plainTextEdit.toPlainText() != self.text:
            reply = QMessageBox.question(self, 'PyQt5 message', "Would you like to save your changes?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.file is None:
                    self.save_file_as()
                else:
                    self.save_file()
                return

        self.file_path, _ = QFileDialog.getOpenFileName(None, "Select Item Placement File", os.getcwd(),
                                                        "All Files (*);;Item Placement File (*.ipl)", )
        if self.file_path:
            try:
                # if file is in text form this block would run
                self.file = open(self.file_path, "r")
                self.text = self.file.read()
                self.plainTextEdit.setPlainText(self.text)
                self.file.close()
            except UnicodeDecodeError:
                # if file is non text(binary) this block would run
                self.bin2text()
                self.plainTextEdit.setPlainText(self.text)

    def save_file(self):
        if self.file_path != "":
            # usual save  block
            self.file = open(self.file_path, "w")
            if self.file:
                self.file.truncate(0)
                self.text = self.plainTextEdit.toPlainText()
                self.file.write(self.plainTextEdit.toPlainText())
                self.file.close()
        else:
            # save as block.will run if no fie found
            self.save_file_as()

    def save_file_as(self):
        self.file_path = (QFileDialog.getSaveFileName(self,
                                                      "Select save directory", "",
                                                      "Any File (*);;Item Placement File (*.ipl)"))[0]
        self.file = open(self.file_path, "w")
        if self.file:
            self.file.truncate(0)
            self.text = self.plainTextEdit.toPlainText()
            self.file.write(self.plainTextEdit.toPlainText())
            self.file.close()

    def close_file(self):
        if self.plainTextEdit.toPlainText() != self.text:
            reply = QMessageBox.question(self, 'PyQt5 message', "Would you like to save your changes?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.file is None:
                    self.save_file_as()
                else:
                    self.save_file()
        self.plainTextEdit.setPlainText("")

    def help_popup(self):
        QMessageBox.information(self, "IPL Converter",
                                "IPL Converter v1.0.\nAuthor : Grinch_\nContact: user.grinch@gmail.com")

    # Converts binary form -> text form
    def bin2text(self):

        try:
            self.file = open(self.file_path, "rb")
            data = struct.unpack(self.header_format, self.file.read()[:self.header_size])
        except:
            QMessageBox.warning(self, "IPL Converter", "The binary file format is not recognized")
            return

        # reading 'bnry' identifier
        if str(data[0])[2:-1] != "bnry":
            QMessageBox.warning(self, "IPL Converter", "Unable to find 'bnry' identifier")
            return

        inst_instances = data[1]
        car_instances = data[5]

        self.text = "# This file is converted using IPL Converter\ninst\n"

        size = self.header_size

        for x in range(inst_instances):
            self.file.seek(0, 0)
            try:
                data = struct.unpack(self.inst_format, self.file.read()[size:(size + self.inst_size)])
                size += self.inst_size
            except:
                QMessageBox.warning(self, "IPL Converter", "Error reading file")
                return
            self.text += (str(data[7]) + ' , ' + 'dummy' + ' , ' + str(data[8]) + ' , ' + str(
                data[0]) + ' , ' + str(data[1]) + ' , ' + str(data[2]) + ' , ' + str(data[3]) + ' , ' + str(
                data[4]) + ' , ' + str(data[5]) + ' , ' + str(data[6]) + ' , ' + str(data[9]) + '\n')
        self.text += "end\ncars\n"

        for x in range(car_instances):
            self.file.seek(0, 0)
            try:
                data = struct.unpack(self.cars_format, self.file.read()[size:(size + self.cars_size)])
                size += self.cars_size
            except:
                QMessageBox.warning(self, "IPL Converter", "Error reading file")
                return
            self.text += (''.join(str(data)[1:-1]) + '\n')
        self.text += "end"
        self.file.close()


    def batch_bin2text(self):
        file_list, _ = QFileDialog.getOpenFileNames(None, "Select Item Placement File", os.getcwd(),
                                                        "All Files (*);;Item Placement File (*.ipl)", )
        if file_list:
            for self.file_path in file_list:
                self.bin2text()
                self.file = open(self.file_path, "w")
                self.file.truncate(0)
                self.file.write(self.text)
                self.file.close()
            self.file_path = ""
