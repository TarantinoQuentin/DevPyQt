# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QFormLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(542, 284)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.Label = QLabel(self.centralwidget)
        self.Label.setObjectName(u"Label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.Label)

        self.LineEdit = QLineEdit(self.centralwidget)
        self.LineEdit.setObjectName(u"LineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.LineEdit)

        self.Label_2 = QLabel(self.centralwidget)
        self.Label_2.setObjectName(u"Label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.Label_2)

        self.SpinBox = QSpinBox(self.centralwidget)
        self.SpinBox.setObjectName(u"SpinBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.SpinBox)

        self.Label_3 = QLabel(self.centralwidget)
        self.Label_3.setObjectName(u"Label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.Label_3)

        self.DateEdit = QDateEdit(self.centralwidget)
        self.DateEdit.setObjectName(u"DateEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.DateEdit)


        self.verticalLayout.addLayout(self.formLayout)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 542, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043c\u044f", None))
        self.Label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u043e\u0437\u0440\u0430\u0441\u0442", None))
        self.Label_3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0430\u0442\u0430", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

