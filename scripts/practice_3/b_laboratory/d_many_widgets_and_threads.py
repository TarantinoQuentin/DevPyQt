"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""

from PySide6 import QtWidgets, QtCore
from c_weatherapi_widget import WeatherWidget
from b_systeminfo_widget import SystemInfoWidget


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Weather & System Info App')
        self.resize(1100, 400)
        self.initUi()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        self.weather_widget = WeatherWidget(self)
        self.system_info_widget = SystemInfoWidget(self)

        self.groupBoxWeatherApp = QtWidgets.QGroupBox('Приложение погоды')
        self.groupBoxWeatherApp.setLayout(QtWidgets.QVBoxLayout())
        self.groupBoxWeatherApp.layout().addWidget(self.weather_widget)
        self.groupBoxWeatherApp.setMinimumSize(650, 100)

        self.groupBoxSystemInfoApp = QtWidgets.QGroupBox('Приложение контроля загрузки системы')
        self.groupBoxSystemInfoApp.setLayout(QtWidgets.QVBoxLayout())
        self.groupBoxSystemInfoApp.layout().addWidget(self.system_info_widget)

        layoutMain = QtWidgets.QHBoxLayout()
        layoutMain.addWidget(self.groupBoxWeatherApp)
        layoutMain.addWidget(self.groupBoxSystemInfoApp)

        self.setLayout(layoutMain)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
