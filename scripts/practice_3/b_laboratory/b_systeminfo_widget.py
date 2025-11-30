"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

import time
import psutil
from PySide6 import QtWidgets, QtCore
from a_threads import SystemInfo


class ExtendedSystemInfo(SystemInfo):

    def set_delay(self, delay: int) -> None:
        """
        Метод для ручной установки задержки
        получения данных

        :return: None
        """

        self.delay = delay


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initThreads()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        lableDelay = QtWidgets.QLabel('Время задержки')

        self.pushButtonDelay = QtWidgets.QPushButton('Установить\nвремя задержки')
        self.pushButtonDelay.setFixedSize(110, 60)
        self.lineEditDelay = QtWidgets.QLineEdit()
        self.lineEditDelay.setPlaceholderText('Введите время')

        layoutDelayline = QtWidgets.QHBoxLayout()
        layoutDelayline.addWidget(lableDelay)
        layoutDelayline.addWidget(self.lineEditDelay)

        layoutDelayBlock = QtWidgets.QVBoxLayout()
        layoutDelayBlock.addLayout(layoutDelayline)
        layoutDelayBlock.addWidget(self.pushButtonDelay)


        self.groupBoxSystemData = QtWidgets.QGroupBox()
        self.groupBoxSystemData.setTitle('Данные загрузки системы')
        lableRAM = QtWidgets.QLabel('Загрузка RAM')
        lableCPU = QtWidgets.QLabel('Загрузка CPU')
        self.lcdNumberRAM = QtWidgets.QLCDNumber()
        self.lcdNumberRAM.setMinimumSize(100, 100)
        self.lcdNumberCPU = QtWidgets.QLCDNumber()
        self.lcdNumberCPU.setMinimumSize(100, 100)

        layoutRAM = QtWidgets.QVBoxLayout()
        layoutRAM.addWidget(lableRAM)
        layoutRAM.addWidget(self.lcdNumberRAM)

        layoutCPU = QtWidgets.QVBoxLayout()
        layoutCPU.addWidget(lableCPU)
        layoutCPU.addWidget(self.lcdNumberCPU)

        layoutSystemData = QtWidgets.QVBoxLayout()
        layoutSystemData.addLayout(layoutRAM)
        layoutSystemData.addLayout(layoutCPU)
        self.groupBoxSystemData.setLayout(layoutSystemData)

        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutDelayBlock)

        self.horizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layoutMain.addSpacerItem(self.horizontalSpacer)
        layoutMain.addWidget(self.groupBoxSystemData)

        self.setLayout(layoutMain)

        self.setWindowTitle('System Info')


    def initThreads(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.system_info_app = ExtendedSystemInfo()
        self.system_info_app.start()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.pushButtonDelay.clicked.connect(self.onPushButtonDelayClicked)
        self.system_info_app.systemInfoReceived.connect(self.system_info_updated)

    def onPushButtonDelayClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonDelay

        :return: None
        """

        self.system_info_app.set_delay(int(self.lineEditDelay.text()))

    def system_info_updated(self, data: list) -> None:
        """
        Вывод значений полученной информации о работе
        системы на соответствующие виджеты

        :return: None
        """

        self.lcdNumberCPU.display(data[0])
        self.lcdNumberRAM.display(data[1])


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
