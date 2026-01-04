from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt6.QtGui import QTransform, QPainter, QPen
from PyQt6.QtCore import Qt
from ChildrenGraph import ChildGraph


class Scene(QGraphicsScene):
    """
    Класс сцены для визуализации детей (ChildGraph) с возможностью смещения
    и рисования рамки вокруг всей сцены.

    Attributes
    ----------
    offset_x : int
        Горизонтальное смещение всех объектов и рамки относительно координат сцены.
    offset_y : int
        Вертикальное смещение всех объектов и рамки относительно координат сцены.
    """

    def __init__(self, width: int = 500, height: int = 300, offset_x: int = -20, offset_y: int = -100):
        """
        Инициализация сцены.

        Parameters
        ----------
        width : int
            Ширина сцены (sceneRect)
        height : int
            Высота сцены (sceneRect)
        offset_x : int
            Смещение объектов и рамки по горизонтали
        offset_y : int
            Смещение объектов и рамки по вертикали
        """
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.logic_group: set[Child] = set()
        self.child_to_item: dict[Child, ChildGraph] = {}

        self.count_click = 10

    def get_children(self, children_list: list):
        """
        Добавляет объекты ChildGraph на сцену с заданным смещением.

        Parameters
        ----------
        children_list : list
            Список объектов Child, на основе которых создаются ChildGraph
        """
        y_start = 10  # начальная координата по Y
        x_start = 10  # начальная координата по X
        x, y = x_start, y_start

        for i, child in enumerate(children_list):
            # Создаём объект ChildGraph с учётом смещения
            child_item = ChildGraph(child=child, x=x + self.offset_x, y=y + self.offset_y)
            x += 25  # шаг по X между объектами
            child_item.clicked.connect(self.on_child_selected)
            self.addItem(child_item)
            self.child_to_item[child] = child_item

            # Переход на новую строку каждые 20 объектов
            if (i + 1) % 20 == 0:
                y += 30  # шаг по Y
                x = x_start

    def on_child_selected(self, child_item: ChildGraph):
        # получаем объект модели
        child = child_item.child

        # добавляем самого ребёнка
        self.logic_group.add(child)

        # добавляем всех родственников
        for relative in child.relative_list:
            self.logic_group.add(relative)

    def get_selected_children(self):
        try:
            return tuple(self.child_to_item[child] for child in self.logic_group)
        except Exception as e:
            print(self.logic_group)

    def mousePressEvent(self, event):
        """
        Обрабатывает нажатие мыши на сцене.

        Если клик был по пустому месту (не на объекте), снимает выделение
        со всех объектов.

        Parameters
        ----------
        event : QGraphicsSceneMouseEvent
            Событие нажатия мыши
        """

        # проверяем клик по пустому месту без Ctrl/Shift
        if not self.itemAt(event.scenePos(), QTransform()):
            if not (event.modifiers() & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier)):
                self.clearSelection()
                self.logic_group.clear()


        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # теперь selection уже обновлен Qt
        self.count_click = 10 - len(self.selectedItems())
        print(self.count_click)

    def drawForeground(self, painter: QPainter, rect):
        """
        Рисует рамку вокруг всей сцены с заданным смещением.

        Parameters
        ----------
        painter : QPainter
            Объект для рисования
        rect : QRectF
            Прямоугольник видимой области, переданный QGraphicsScene
        """
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.DotLine)
        pen.setCosmetic(True)  # толщина линии фиксирована на экране
        painter.setPen(pen)

        # Сдвигаем рамку с учётом offset_x и offset_y
        frame_rect = self.sceneRect().translated(self.offset_x, self.offset_y)
        painter.drawRect(frame_rect)


class SelectedScene(Scene):
    def __init__(self, width: int = 20, height: int = 300, offset_x: int = -110, offset_y: int = -100):
        super().__init__()

        self.setSceneRect(0, 0, width, height)
        self.offset_x = offset_x
        self.offset_y = offset_y

    def get_children(self, selected_child_list: tuple[ChildGraph]):
        y_start = 10  # начальная координата по Y
        x_start = 10  # начальная координата по X
        x, y = x_start, y_start
        for child in selected_child_list:
            child.setPos(x + self.offset_x, y + self.offset_y)
            self.addItem(child)
            y += 25
