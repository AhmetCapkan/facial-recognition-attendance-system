# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kayit_formu.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 443)
        MainWindow.setStyleSheet("background-color: #f5f5f5;\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 0, 521, 41))
        font = QtGui.QFont()
        font.setFamily("Lucida Handwriting")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setStyleSheet("QLineEdit {\n"
"    color: red; /* Metin rengi */\n"
"    background-color: white; /* Arkaplan rengi */\n"
"    border: 1px solid gray; /* Kenarlık */\n"
"}\n"
"")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 50, 411, 248))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(5, 10, 11, 7)
        self.formLayout.setHorizontalSpacing(15)
        self.formLayout.setVerticalSpacing(28)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineAdSoyad = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lineAdSoyad.setFont(font)
        self.lineAdSoyad.setStyleSheet("border: 2px solid #ccc;\n"
"border-radius: 10px;\n"
"padding: 5px;\n"
"font-size: 14px;")
        self.lineAdSoyad.setText("")
        self.lineAdSoyad.setObjectName("lineAdSoyad")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineAdSoyad)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineNumara = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lineNumara.setFont(font)
        self.lineNumara.setStyleSheet("border: 2px solid #ccc;\n"
"border-radius: 10px;\n"
"padding: 5px;\n"
"font-size: 14px;")
        self.lineNumara.setText("")
        self.lineNumara.setObjectName("lineNumara")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineNumara)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineBolum = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.lineBolum.setFont(font)
        self.lineBolum.setStyleSheet("border: 2px solid #ccc;\n"
"border-radius: 10px;\n"
"padding: 5px;\n"
"font-size: 14px;")
        self.lineBolum.setText("")
        self.lineBolum.setObjectName("lineBolum")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineBolum)
        self.btnLoadPhoto = QtWidgets.QPushButton(self.formLayoutWidget)
        self.btnLoadPhoto.setMinimumSize(QtCore.QSize(0, 43))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.btnLoadPhoto.setFont(font)
        self.btnLoadPhoto.setStyleSheet("QPushButton{\n"
"border: 2px solid #ccc;\n"
"border-radius: 10px;\n"
"padding: 5px;\n"
"font-size: 20px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #E5E1DA;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/90537/Desktop/foto.icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLoadPhoto.setIcon(icon)
        self.btnLoadPhoto.setIconSize(QtCore.QSize(40, 30))
        self.btnLoadPhoto.setObjectName("btnLoadPhoto")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.btnLoadPhoto)
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(30, 310, 361, 71))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.btn.setFont(font)
        self.btn.setStyleSheet("QPushButton{\n"
"border: 2px solid #ccc;\n"
"border-radius: 10px;\n"
"padding: 5px;\n"
"font-size: 25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #E5E1DA;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/90537/Desktop/add.icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn.setIcon(icon1)
        self.btn.setIconSize(QtCore.QSize(40, 40))
        self.btn.setObjectName("btn")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(454, 65, 301, 301))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "📝 Öğremci Kayıt Formu"))
        self.label_2.setText(_translate("MainWindow", "Ad Soyad"))
        self.label_3.setText(_translate("MainWindow", "Numara"))
        self.label_4.setText(_translate("MainWindow", "Bölüm"))
        self.btnLoadPhoto.setText(_translate("MainWindow", "Fotoğraf Ekle"))
        self.btn.setText(_translate("MainWindow", "Kayıt Ekle"))
        self.label_5.setText(_translate("MainWindow", "Yüklenecek Fotoğraf"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
