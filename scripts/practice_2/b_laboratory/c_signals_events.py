"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущий основной монитор
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtGui
from c_signals_events_form import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.w_screen, self.h_screen = QtWidgets.QApplication.primaryScreen().size().toTuple()  # Для размера экрана
        self.screen_width, self.screen_height = QtWidgets.QApplication.primaryScreen().availableGeometry().size().toTuple()
        # Для размера экрана с учетом панели задач внизу
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """

        self.ui.pushButtonLT.clicked.connect(self.onPushButtonLTClicked)
        self.ui.pushButtonRT.clicked.connect(self.onPushButtonRTClicked)
        self.ui.pushButtonCenter.clicked.connect(self.onPushButtonCenterClicked)
        self.ui.pushButtonLB.clicked.connect(self.onPushButtonLBClicked)
        self.ui.pushButtonRB.clicked.connect(self.onPushButtonRBClicked)
        self.ui.pushButtonMoveCoords.clicked.connect(self.onPushButtonMoveCoordsClicked)
        self.ui.pushButtonGetData.clicked.connect(self.onPushButtonGetDataClicked)

    # slots --------------------------------------------------------------
    def onPushButtonLTClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLT

        :return: None
        """

        self.move(0, 0)

    def onPushButtonRTClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonRT

        :return: None
        """

        self.move(self.screen_width - self.width(), 0)

    def onPushButtonLBClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLB

        :return: None
        """

        self.move(0, self.screen_height - self.height())

    def onPushButtonRBClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonRB

        :return: None
        """

        self.move(self.screen_width - self.width(), self.screen_height - self.height())

    def onPushButtonCenterClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonCenter

        :return: None
        """
        # w_cen, h_cen = self.rect().center().toTuple()
        self.move((self.screen_width // 2 - self.width() // 2), (self.screen_height // 2 - self.height() // 2))

    def onPushButtonMoveCoordsClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonMoveCoords

        :return: None
        """

        self.move(self.ui.spinBoxX.value(), self.ui.spinBoxY.value())

    def onPushButtonGetDataClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonGetData

        :return: None
        """

        plain_text = f"""
        * Кол-во экранов: {len(QtWidgets.QApplication.screens())}
        * Текущий основной монитор: {QtWidgets.QApplication.primaryScreen().name()}
        * Разрешение экрана: {self.screen_width}x{self.screen_height}
        * На каком экране окно находится: {self.screen().name()}
        * Размеры окна: {self.geometry().width()}x{self.geometry().height()}
        * Минимальные размеры окна: {self.minimumSize().width()}x{self.minimumSize().height()}
        * Текущее положение (координаты) окна: X:{self.geometry().x()}, Y:{self.geometry().y()}
        * Координаты центра приложения: X:{self.geometry().x() + self.width() // 2}, Y:{self.geometry().y() + self.height() // 2}
        * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено): {self.check_window_state()}
        """
        # Размеры окна: {self.size().width()x{self.size().height()}
        # Текущее положение (координаты) окна: {self.x()}, {self.y()}
        # Текущее положение (координаты) окна: {self.pos().toTuple()}
        # Координаты центра приложения: {self.rect().center().toTuple()}

        self.ui.plainTextEdit.setPlainText(plain_text)

    def check_window_state(self) -> str:
        """
        Функция для определения состояния окна

        :return: статус окна
        """

        state = []
        if self.isMinimized():
            state.append('свернуто')
        if self.isMaximized():
            state.append('развернуто')
        if self.isActiveWindow():
            state.append('активно')
        if self.isVisible():
            state.append('отображено')
        return ', '.join(state)

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        """
        Событие изменения положения окна

        :param event: QtGui.QMoveEvent
        :return: None
        """

        print(f'Старое положение окна: X:{event.oldPos().x()}, Y:{event.oldPos().y()}')
        print(f'Новое положение окна: X:{event.pos().x()}, Y:{event.pos().y()}')
        print()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Событие изменения размера окна

        :param event: QtGui.QResizeEvent
        :return: None
        """

        print(f'Текущий размер окна: {event.size().width()}x{event.size().height()}')
        print()

    # def resizeEvent(self, event, /):
    # """
    # Событие изменения размера окна
    #
    # :param event: QtGui.QResizeEvent
    # :return: None
    # """

    #     print(self.size())
    #     return super().resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
