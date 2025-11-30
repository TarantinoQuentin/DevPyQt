"""
Модуль в котором содержаться потоки Qt
"""

import time
from datetime import datetime
import requests
import psutil
from PySide6 import QtWidgets, QtCore
from a_threads_form import Ui_MainWindow


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # создайте атрибут класса self.delay = None, для управления задержкой получения данных

    def run(self) -> None:  # переопределить метод run
        if self.delay is None:  # Если задержка не передана в поток перед его запуском
            self.delay = 1  # то устанавливайте значение 1

        while True:  # Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent   # с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    received_weather_data = QtCore.Signal(dict)  # Пропишите сигналы, которые считаете нужными

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = None

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay

    def run(self) -> None:
        self.__status = True  # настройте метод для корректной работы

        while self.__status:
            #  Примерный код ниже
            response = requests.get(self.__api_url)
            data = response.json()
            self.received_weather_data.emit(data)
            self.sleep(self.__delay)


class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initThreads()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initSignals()


    def initThreads(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.system_info_app = SystemInfo()
        self.weather_api_app = WeatherHandler(59.57, 30.19)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        # self.ui.pushButton.clicked.connect(self.runLongProcess)


        self.ui.pushButton.clicked.connect(self.weather_api_app.start)
        self.weather_api_app.received_weather_data.connect(self.weather_api_updated)

        self.ui.pushButton_2.clicked.connect(self.system_info_app.start)
        self.system_info_app.systemInfoReceived.connect(self.system_info_updated)

    def weather_api_updated(self, data: dict) -> None:

        def get_wind_direction():
            degrees = data['current_weather']['winddirection']
            if 337.5 <= degrees <= 360 or 0 <= degrees < 22.5:
                return "Север (С)"
            elif 22.5 <= degrees < 67.5:
                return "Северо-восток (СВ)"
            elif 67.5 <= degrees < 112.5:
                return "Восток (В)"
            elif 112.5 <= degrees < 157.5:
                return "Юго-восток (ЮВ)"
            elif 157.5 <= degrees < 202.5:
                return "Юг (Ю)"
            elif 202.5 <= degrees < 247.5:
                return "Юго-запад (ЮЗ)"
            elif 247.5 <= degrees < 292.5:
                return "Запад (З)"
            elif 292.5 <= degrees < 337.5:
                return "Северо-запад (СЗ)"
            else:
                return "Неизвестное направление"

        result = (f'Время последнего обновления: {datetime.fromisoformat(data['current_weather']['time'])}\n'
                  f'Температура: {data['current_weather']['temperature']} °C\n'
                  f'Скорость ветра: {round((data['current_weather']['windspeed'] / 3.6), 1)} м/с\n'
                  f'Направление ветра: {get_wind_direction()}')

        self.ui.plainTextEdit.setPlainText(f"Обновлено: {time.ctime()}\n{result}")

    def system_info_updated(self, data: dict) -> None:

        result = (f'Загрузка системы в реальном времени:\n\n'
                  f'{time.ctime()}\n\n'
                  f'CPU: {data[0]}\n'
                  f'RAM: {data[1]}')
        self.ui.plainTextEdit_2.setPlainText(result)






if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
