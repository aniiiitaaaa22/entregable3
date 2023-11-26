# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menuMYpiHf.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QSlider, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
from res import *
from icon import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from messagebox import msg_error

import menu_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(756, 469)
        MainWindow.setMinimumSize(QSize(400, 0))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName(u"frame_superior")
        self.frame_superior.setMinimumSize(QSize(0, 35))
        self.frame_superior.setMaximumSize(QSize(16777215, 50))
        self.frame_superior.setStyleSheet(u"\n"
"QFrame{\n"
"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 20px;\n"
"\n"
"background-color: rgba(212, 154, 220,250);\n"
"\n"
"}\n"
"")
        self.frame_superior.setFrameShape(QFrame.StyledPanel)
        self.frame_superior.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_superior)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(2, 0, 2, 0)
        self.bt_menu = QPushButton(self.frame_superior)
        self.bt_menu.setObjectName(u"bt_menu")
        self.bt_menu.setMinimumSize(QSize(200, 0))
        self.bt_menu.setMaximumSize(QSize(200, 16777215))
        self.bt_menu.setStyleSheet(u"QPushButton{\n"
"background-color: #8D3291;\n"
"font: 87 12pt \"Arial Black\";\n"
"border-radius:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"font: 87 12pt \"Arial Black\";\n"
"\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u"barra-de-menus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_menu.setIcon(icon)
        self.bt_menu.setIconSize(QSize(32, 32))
        self.bt_menu.setAutoDefault(False)
        self.bt_menu.setFlat(False)

        self.horizontalLayout_8.addWidget(self.bt_menu, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(265, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.bt_minimizar = QPushButton(self.frame_superior)
        self.bt_minimizar.setObjectName(u"bt_minimizar")
        self.bt_minimizar.setMinimumSize(QSize(35, 35))
        self.bt_minimizar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#B6D3F1;\n"
"\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u"minimizar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_minimizar.setIcon(icon1)
        self.bt_minimizar.setIconSize(QSize(32, 32))
        self.bt_minimizar.setFlat(False)

        self.horizontalLayout_8.addWidget(self.bt_minimizar, 0, Qt.AlignRight)

        self.bt_restaurar = QPushButton(self.frame_superior)
        self.bt_restaurar.setObjectName(u"bt_restaurar")
        self.bt_restaurar.setMaximumSize(QSize(35, 35))
        self.bt_restaurar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#D1EBAC;\n"
"\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u"restaurar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_restaurar.setIcon(icon2)
        self.bt_restaurar.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.bt_restaurar, 0, Qt.AlignRight)

        self.bt_maximizar = QPushButton(self.frame_superior)
        self.bt_maximizar.setObjectName(u"bt_maximizar")
        self.bt_maximizar.setMaximumSize(QSize(35, 35))
        self.bt_maximizar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#FBF3B3;\n"
"\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u"maximizar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_maximizar.setIcon(icon3)
        self.bt_maximizar.setIconSize(QSize(32, 32))

        self.horizontalLayout_8.addWidget(self.bt_maximizar, 0, Qt.AlignRight)

        self.bt_cerrar = QPushButton(self.frame_superior)
        self.bt_cerrar.setObjectName(u"bt_cerrar")
        self.bt_cerrar.setMaximumSize(QSize(35, 16777215))
        self.bt_cerrar.setStyleSheet(u"QPushButton{\n"
"border:0px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:5px solid #aa00ff;\n"
"background-color:#F39897;\n"
"\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u"cerrar.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_cerrar.setIcon(icon4)
        self.bt_cerrar.setIconSize(QSize(32, 32))

        self.horizontalLayout_8.addWidget(self.bt_cerrar, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.frame_superior)

        self.frame_inferior = QFrame(self.centralwidget)
        self.frame_inferior.setObjectName(u"frame_inferior")
        self.frame_inferior.setStyleSheet(u"")
        self.frame_inferior.setFrameShape(QFrame.StyledPanel)
        self.frame_inferior.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_inferior)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_lateral = QFrame(self.frame_inferior)
        self.frame_lateral.setObjectName(u"frame_lateral")
        self.frame_lateral.setMinimumSize(QSize(200, 0))
        self.frame_lateral.setMaximumSize(QSize(0, 16777215))
        self.frame_lateral.setLayoutDirection(Qt.LeftToRight)
        self.frame_lateral.setAutoFillBackground(False)
        self.frame_lateral.setStyleSheet(u"\n"
"QFrame{\n"
"background-color:#D49ADC;\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton{\n"
"background-color: #D49ADC;\n"
"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 20px;\n"
"\n"
"font: 75 12pt \"Arial Narrow\";\n"
"	\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background-color: white;\n"
"border-top-left-radius: 20px;\n"
"border-bottom-left-radius: 20px;\n"
"\n"
"font: 75 12pt \"Arial Narrow\";\n"
"}")
        self.frame_lateral.setFrameShape(QFrame.StyledPanel)
        self.frame_lateral.setFrameShadow(QFrame.Plain)
        self.verticalLayout_2 = QVBoxLayout(self.frame_lateral)
        self.verticalLayout_2.setSpacing(20)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, 0, 9)
        self.bt_inicio = QPushButton(self.frame_lateral)
        self.bt_inicio.setObjectName(u"bt_inicio")
        self.bt_inicio.setMinimumSize(QSize(0, 40))
        self.bt_inicio.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.bt_inicio.setLayoutDirection(Qt.LeftToRight)
        icon5 = QIcon()
        icon5.addFile(u"inteligencia-artificial.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_inicio.setIcon(icon5)
        self.bt_inicio.setIconSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.bt_inicio)

        self.bt_uno = QPushButton(self.frame_lateral)
        self.bt_uno.setObjectName(u"bt_uno")
        self.bt_uno.setMinimumSize(QSize(0, 40))
        self.bt_uno.setToolTipDuration(0)
        self.bt_uno.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u"base-de-datos.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_uno.setIcon(icon6)
        self.bt_uno.setIconSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.bt_uno)

        self.bt_dos = QPushButton(self.frame_lateral)
        self.bt_dos.setObjectName(u"bt_dos")
        self.bt_dos.setMinimumSize(QSize(0, 40))
        self.bt_dos.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u"chip.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_dos.setIcon(icon7)
        self.bt_dos.setIconSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.bt_dos)

        self.bt_tres = QPushButton(self.frame_lateral)
        self.bt_tres.setObjectName(u"bt_tres")
        self.bt_tres.setMinimumSize(QSize(0, 40))
        self.bt_tres.setStyleSheet(u"")
        icon8 = QIcon()
        icon8.addFile(u"moto.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_tres.setIcon(icon8)
        self.bt_tres.setIconSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.bt_tres)

        self.bt_cuatro = QPushButton(self.frame_lateral)
        self.bt_cuatro.setObjectName(u"bt_cuatro")
        self.bt_cuatro.setMinimumSize(QSize(0, 40))
        self.bt_cuatro.setStyleSheet(u"")
        icon9 = QIcon()
        icon9.addFile(u"encriptado.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bt_cuatro.setIcon(icon9)
        self.bt_cuatro.setIconSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.bt_cuatro)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_2 = QLabel(self.frame_lateral)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamily(u"The Serif Hand Blacki")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"font: italic 15pt \"The Serif Hand Blacki\";")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)


        self.horizontalLayout.addWidget(self.frame_lateral, 0, Qt.AlignLeft)

        self.frame_contenedor = QFrame(self.frame_inferior)
        self.frame_contenedor.setObjectName(u"frame_contenedor")
        self.frame_contenedor.setStyleSheet(u"")
        self.frame_contenedor.setFrameShape(QFrame.StyledPanel)
        self.frame_contenedor.setFrameShadow(QFrame.Raised)
        self.frame_contenedor.setLineWidth(1)
        self.verticalLayout_3 = QVBoxLayout(self.frame_contenedor)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_contenedor)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(400, 400))
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.stackedWidget.setFrameShape(QFrame.NoFrame)
        self.stackedWidget.setFrameShadow(QFrame.Plain)
        self.stackedWidget.setLineWidth(0)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_9 = QVBoxLayout(self.page)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"border-image: url(:/menu/icon/hellokitty1.png);")
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setIndent(0)

        self.verticalLayout_9.addWidget(self.label)

        self.stackedWidget.addWidget(self.page)
        self.page_uno = QWidget()
        self.page_uno.setObjectName(u"page_uno")
        self.page_uno.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_4 = QVBoxLayout(self.page_uno)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_5 = QPushButton(self.page_uno)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(400, 400))
        self.pushButton_5.setStyleSheet(u"border-image: url(:/menu/icon/Keroppi.png);")

        self.verticalLayout_4.addWidget(self.pushButton_5)

        self.stackedWidget.addWidget(self.page_uno)
        self.page_dos = QWidget()
        self.page_dos.setObjectName(u"page_dos")
        self.page_dos.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_5 = QVBoxLayout(self.page_dos)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton_4 = QPushButton(self.page_dos)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(400, 400))
        self.pushButton_4.setStyleSheet(u"border-image: url(:/menu/icon/HK3.png);")

        self.verticalLayout_5.addWidget(self.pushButton_4)

        self.stackedWidget.addWidget(self.page_dos)
        self.page_tres = QWidget()
        self.page_tres.setObjectName(u"page_tres")
        self.verticalLayout_6 = QVBoxLayout(self.page_tres)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_3 = QPushButton(self.page_tres)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(400, 400))
        self.pushButton_3.setStyleSheet(u"border-image: url(:/menu/icon/HK4.png);")

        self.verticalLayout_6.addWidget(self.pushButton_3)

        self.stackedWidget.addWidget(self.page_tres)
        self.page_cuatro = QWidget()
        self.page_cuatro.setObjectName(u"page_cuatro")
        self.page_cuatro.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_7 = QVBoxLayout(self.page_cuatro)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.pushButton_2 = QPushButton(self.page_cuatro)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(400, 400))
        self.pushButton_2.setStyleSheet(u"border-image: url(:/menu/icon/HK5.png);")

        self.verticalLayout_7.addWidget(self.pushButton_2)

        self.stackedWidget.addWidget(self.page_cuatro)
        self.page_cinco = QWidget()
        self.page_cinco.setObjectName(u"page_cinco")
        self.page_cinco.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_8 = QVBoxLayout(self.page_cinco)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.pushButton = QPushButton(self.page_cinco)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(400, 400))
        self.pushButton.setStyleSheet(u"border-image: url(:/menu/icon/KM1.png);")

        self.verticalLayout_8.addWidget(self.pushButton)

        self.stackedWidget.addWidget(self.page_cinco)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.frame_contenedor)


        self.verticalLayout.addWidget(self.frame_inferior)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.bt_menu.setDefault(False)
        self.stackedWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.bt_menu.setText(QCoreApplication.translate("MainWindow", u"    MENU ", None))
        self.bt_minimizar.setText("")
        self.bt_restaurar.setText("")
        self.bt_maximizar.setText("")
        self.bt_cerrar.setText("")
        self.bt_inicio.setText(QCoreApplication.translate("MainWindow", u"ARCHIVOS DCM", None))
        self.bt_uno.setText(QCoreApplication.translate("MainWindow", u"ARCHIVOS JPG,PNG", None))
        self.bt_dos.setText(QCoreApplication.translate("MainWindow", u"ARCHIVOS CSV", None))
        self.bt_tres.setText(QCoreApplication.translate("MainWindow", u"ARCHIVOS MAT", None))
        self.bt_cuatro.setText(QCoreApplication.translate("MainWindow", u"SALIR", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"SanrioMedical", None))
        self.label.setText("")
        self.pushButton_2.setText("")
        self.pushButton.setText("")
    # retranslateUi

