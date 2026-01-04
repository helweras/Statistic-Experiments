from PyQt6.QtWidgets import QGraphicsObject, QGraphicsItem
from PyQt6.QtCore import pyqtSignal, QRectF, Qt
from PyQt6.QtGui import QBrush, QPen, QPainter


class ChildGraph(QGraphicsObject):
    """
    Графическое представление ребенка на сцене в виде круга с возможностью выбора и сигналами.

    Каждый объект представляет одного ребенка и умеет:
    - отображать себя в виде круга,
    — менять цвет в зависимости от пола ребенка,
    — реагировать на клики с передачей себя через сигнал `clicked`.

    Attributes
    ----------
    child : Child
        Экземпляр класса Child, содержащий данные ребенка (имя, пол и др.).
    radius : float
        Радиус круга, отображающего ребенка.
    clicked : pyqtSignal
        Сигнал, который эмитится при клике по объекту. Передает сам объект ChildGraph.
    """

    # Сигнал, который передает сам объект при клике
    clicked = pyqtSignal(object)

    def __init__(self, child, x: float, y: float, diameter: float = 20):
        """
        Инициализация графического объекта ребенка.

        Parameters
        ----------
        child : Child
            Объект Child с данными ребенка.
        x : float
            Координата X на сцене.
        y : float
            Координата Y на сцене.
        diameter : float, optional
            Диаметр круга, по умолчанию 20.
        """
        super().__init__()
        self.child = child
        self.radius = diameter / 2

        # Разрешаем выделение объекта на сцене
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        # Устанавливаем позицию на сцене
        self.setPos(x, y)

    # -------------------------
    # Методы доступа к данным
    # -------------------------
    def get_name(self) -> str:
        """Возвращает имя ребенка."""
        return self.child.name

    def get_sex(self) -> str:
        """Возвращает пол ребенка ('Men' или 'Women')."""
        return self.child.sex

    def get_color(self) -> Qt.GlobalColor:
        """
        Определяет цвет круга в зависимости от пола ребенка.

        Returns
        -------
        Qt.GlobalColor
            Синий для мужчин, красный для женщин.
        """
        return Qt.GlobalColor.blue if self.get_sex() == "Men" else Qt.GlobalColor.red

    # -------------------------
    # Вспомогательные методы
    # -------------------------
    def paint_color(self):
        """
        Обновляет цвет объекта на сцене.

        Цвет задается в методе paint().
        """
        self.update()  # инициируем перерисовку

    # -------------------------
    # Переопределенные методы QGraphicsObject
    # -------------------------
    def boundingRect(self) -> QRectF:
        """
        Возвращает ограничивающий прямоугольник объекта.
        Используется системой для отрисовки и обработки событий.

        Returns
        -------
        QRectF
            Прямоугольник, охватывающий круг.
        """
        return QRectF(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

    def paint(self, painter: QPainter, option, widget=None):
        """
        Отрисовка графического объекта.

        Рисует круг с цветом по полу ребенка.
        Если объект выделен, рисуется желтая рамка вокруг круга.

        Parameters
        ----------
        painter : QPainter
            Инструмент для рисования.
        option : QStyleOptionGraphicsItem
            Опции стиля объекта.
        widget : QWidget, optional
            Виджет, на котором производится рисование.
        """
        # Рисуем основной круг с цветом по полу
        color = self.get_color()
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(Qt.GlobalColor.black, 1))
        painter.drawEllipse(self.boundingRect())

        # Если объект выделен — рисуем желтую рамку
        if self.isSelected():
            pen = QPen(Qt.GlobalColor.yellow, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(self.boundingRect())

    # -------------------------
    # Переопределение событий мыши
    # -------------------------
    def mousePressEvent(self, event):
        """
        Обрабатывает событие клика мышью.

        Эмитит сигнал `clicked` с передачей себя и вызывает стандартную обработку.
        """
        self.clicked.emit(self)
        super().mousePressEvent(event)
