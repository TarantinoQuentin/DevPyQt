"""
Подключение формы созданной в дизайнере

Команда для конвертации формы:
PySide6-uic path_to_form.ui -o path_to_form.py
"""

from PySide6 import QtWidgets

from form import Ui_MainWindow  # Импортируем класс формы


class Window(QtWidgets.QMainWindow):  # наследуемся от того же класса, что и форма в QtDesigner
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создание "прокси" переменной для работы с формой
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.setText('Нажми')

        self.ui.pushButton.setStyleSheet(
            # "QPushButton {"
            # "    color: white;"
            # "    background-color: #4CAF50;"
            # "    border: 2px solid #2E8B57;"
            # "    border-radius: 10px;"
            # "    padding: 5px;"
            # "}"
            # "QPushButton:hover {"
            # "    background-color: #45a049;"
            # "}"
            # "QPushButton:pressed {"
            # "    background-color: #388e3c;"
            # "    border-style: inset;"
            # "}"
            # "QPushButton {"
            # "    border-radius: 15px;"
            # "    background-color: lightblue;"
            # "    padding: 10px;"
            # "}"
            # "QPushButton:hover {"
            # "    background-color: skyblue;"
            # "}"
            "QPushButton {"
            "    border-radius: 15px;"
            "    color: white;"
            "    padding: 10px;"
            "    transition: .2s linear;"
            "    background: #0B63F6;"
            "}"
            "QPushButton:hover {"
            "    box-shadow: 0 0 0 2px white, 0 0 0 4px #3C82F8;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #3C82F8;"
            "    border-style: inset;"
            "}"
        );

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
