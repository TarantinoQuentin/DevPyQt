"""
Файл для повторения темы QThread

Напомнить про работу с QThread.

Предлагается создать небольшое приложение, которое будет с помощью модуля request
получать доступность того или иного сайта (возвращать из потока status_code сайта).

Поработать с сигналами, которые возникают при запуске/остановке потока,
передать данные в поток (в данном случае url),
получить данные из потока (статус код сайта),
попробовать управлять потоком (запуск, остановка).

Опционально поработать с валидацией url
"""
import time
import traceback

import requests
from PySide6 import QtWidgets, QtCore

from scripts.practice_3.a_repeat.a_qtimer_repeat import ClockWidget


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()
        self.__initSignals()
        self.__initThreads()

    def __initUi(self):
        self.setStyleSheet("font-size: 20px")

        self.lineEditUrl = QtWidgets.QLineEdit()
        self.lineEditUrl.setPlaceholderText("Введите URL")

        self.pushButtonHandle = QtWidgets.QPushButton("Старт")
        self.pushButtonHandle.setCheckable(True)

        self.plainTextEditLog = QtWidgets.QPlainTextEdit()
        self.plainTextEditLog.setReadOnly(True)

        self.clockWidget = ClockWidget()

        l_handle = QtWidgets.QHBoxLayout()
        l_handle.addWidget(self.lineEditUrl)
        l_handle.addWidget(self.pushButtonHandle)

        l = QtWidgets.QVBoxLayout()
        l.addLayout(l_handle)
        l.addWidget(self.plainTextEditLog)
        l.addWidget(self.clockWidget)

        self.setLayout(l)

    def __initSignals(self):
        self.pushButtonHandle.clicked.connect(self.__handleMainThread)

    def __initThreads(self):
        self.thread = MainThread()
        self.thread.started.connect(lambda: self.appendLogMessage("Поток запущен"))
        self.thread.checked.connect(lambda data: self.appendLogMessage(f"Статус код: {data}"))
        self.thread.finished.connect(lambda: self.appendLogMessage("Поток остановлен"))
        self.thread.finished.connect(lambda: self.pushButtonHandle.setChecked(False))
        self.thread.finished.connect(lambda: self.pushButtonHandle.setText("Старт"))

    def __handleMainThread(self):

        if not self.thread.isRunning():
            url = self.lineEditUrl.text()
            if 'http://' in url or 'https://' in url:
                self.thread.url = url
                self.thread.start()
                self.pushButtonHandle.setText("Стоп")
            else:
                self.appendLogMessage(f"Неверный URL адрес")
        else:
            self.thread.stop()

    def appendLogMessage(self, text):
        self.plainTextEditLog.appendPlainText(f"{time.ctime()} >>> {text}")


class MainThread(QtCore.QThread):
    checked = QtCore.Signal(int)

    def __init__(self, url='', delay=1, parent=None):
        super().__init__(parent)
        self.url = url
        self.__status = None
        self.__delay = delay

    def stop(self):
        self.__status = False

    def setDelay(self, delay):
        self.__delay = delay

    def run(self):
        self.__status = True
        while self.__status:
            try:
                r = requests.get(self.url, timeout=3)
                self.checked.emit(r.status_code)
                self.sleep(self.__delay)
            except Exception:
                traceback.print_exc()
                self.stop()
                print('Ошибка, поток остановлен')


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
