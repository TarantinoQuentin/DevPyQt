"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

import time
from datetime import datetime
from PySide6 import QtWidgets
from a_threads import WeatherHandler


class ExtendedWeatherHandler(WeatherHandler):

    def __init__(self, lat=59.57, lon=30.19):
        super().__init__(lat, lon)

    def set_longitude_and_latitude(self, lat: float, lon: float) -> None:
        """
        Метод для ручной установки высоты и долготы

        :return: None
        """

        self.set_api_url(lat, lon)

    def stop(self) -> None:
        """
        Метод для остановки цикла приложения

        :return: None
        """

        self.set_status(False)


class WeatherWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()
        self.initThreads()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        labelLatitude = QtWidgets.QLabel('Высота')
        labelLongitude = QtWidgets.QLabel('Долгота')
        self.spinBoxLatitude = QtWidgets.QDoubleSpinBox()
        self.spinBoxLatitude.setValue(59.57)
        self.spinBoxLatitude.setSingleStep(0.01)
        self.spinBoxLongitude = QtWidgets.QDoubleSpinBox()
        self.spinBoxLongitude.setValue(30.19)
        self.spinBoxLongitude.setSingleStep(0.01)

        layoutLatitude = QtWidgets.QHBoxLayout()
        layoutLatitude.addWidget(labelLatitude)
        layoutLatitude.addWidget(self.spinBoxLatitude)

        layoutLongitude = QtWidgets.QHBoxLayout()
        layoutLongitude.addWidget(labelLongitude)
        layoutLongitude.addWidget(self.spinBoxLongitude)

        layoutCoordinates = QtWidgets.QVBoxLayout()
        layoutCoordinates.addLayout(layoutLatitude)
        layoutCoordinates.addLayout(layoutLongitude)

        self.groupBoxCoordinates = QtWidgets.QGroupBox()
        self.groupBoxCoordinates.setTitle('Координаты')
        self.groupBoxCoordinates.setLayout(layoutCoordinates)

        labelDelay = QtWidgets.QLabel('Время задержки')
        self.lineEditDelay = QtWidgets.QLineEdit()
        self.lineEditDelay.setPlaceholderText('Введите время')

        layoutDelay = QtWidgets.QHBoxLayout()
        layoutDelay.addWidget(labelDelay)
        layoutDelay.addWidget(self.lineEditDelay)

        self.groupBoxDelay = QtWidgets.QGroupBox()
        self.groupBoxDelay.setTitle('Задержка обновления данных')
        self.groupBoxDelay.setLayout(layoutDelay)

        self.pushButtonSetData = QtWidgets.QPushButton('Установить значения и\nзапустить программу')
        self.pushButtonSetData.setCheckable(True)

        layoutSetData = QtWidgets.QVBoxLayout()
        layoutSetData.addWidget(self.groupBoxCoordinates)
        layoutSetData.addWidget(self.groupBoxDelay)
        layoutSetData.addWidget(self.pushButtonSetData)

        self.plainTextEditLog = QtWidgets.QPlainTextEdit()

        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addLayout(layoutSetData)
        layoutMain.addWidget(self.plainTextEditLog)

        self.setLayout(layoutMain)
        self.setWindowTitle('Weather App')
        self.resize(650, 200)

    def initThreads(self) -> None:
        """
        Инициализация потоков

        :return: None
        """

        self.weather_api_app = ExtendedWeatherHandler()
        self.weather_api_app.received_weather_data.connect(lambda data: self.weather_api_updated(data))
        self.weather_api_app.finished.connect(lambda: self.pushButtonSetData.setChecked(False))
        self.weather_api_app.finished.connect(lambda: self.pushButtonSetData.setText('Установить значения и\nзапустить программу'))
        self.weather_api_app.finished.connect(lambda: self.spinBoxLongitude.setEnabled(True))
        self.weather_api_app.finished.connect(lambda: self.spinBoxLatitude.setEnabled(True))
        self.weather_api_app.finished.connect(lambda: self.lineEditDelay.setEnabled(True))

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.pushButtonSetData.clicked.connect(self.onPushButtonSetData)

    def onPushButtonSetData(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonSetData

        :return: None
        """

        if not self.weather_api_app.isRunning():
            self.weather_api_app.set_longitude_and_latitude(lat=self.spinBoxLatitude.value(),
                                                            lon=self.spinBoxLongitude.value())
            self.weather_api_app.setDelay(int(self.lineEditDelay.text()))
            self.pushButtonSetData.setText("Стоп")
            self.weather_api_app.start()
            self.spinBoxLongitude.setEnabled(False)
            self.spinBoxLatitude.setEnabled(False)
            self.lineEditDelay.setEnabled(False)
        else:
            self.weather_api_app.stop()

    def weather_api_updated(self, data: dict) -> None:
        """
        Метод для вывода полученных значений в лог

        :return: None
        """

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

        result = (f"Время последнего обновления: {datetime.fromisoformat(data['current_weather']['time'])}\n"
                  f"Температура: {data['current_weather']['temperature']} °C\n"
                  f"Скорость ветра: {round((data['current_weather']['windspeed'] / 3.6), 1)} м/с\n"
                  f'Направление ветра: {get_wind_direction()}')

        self.plainTextEditLog.setPlainText(f"Обновлено: {time.ctime()}\n\n"
                                           f"Координаты:\nВысота — {self.spinBoxLatitude.value()}\nДолгота — {self.spinBoxLongitude.value()}\n\n"
                                           f"{result}\n")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = WeatherWidget()
    window.show()

    app.exec()
