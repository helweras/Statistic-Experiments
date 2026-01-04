import sys

from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QHBoxLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from GraphicScene import Scene, SelectedScene
from ClassView import View
from ChildrenGraph import ChildGraph
from Experiments.OldestBrother.Logic import ret_children


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 старт")
        self.resize(1200, 600)

        self.scene_all = Scene()
        self.selected_scene = SelectedScene()
        self.add_child_in_scene()

        self.view_all = View(self.scene_all)
        self.view_selected = View(self.selected_scene)

        self.btn_rebase = QPushButton("Переместить выбранных")
        self.btn_rebase.clicked.connect(
            lambda: self.rebase_selected_children(self.scene_all, self.selected_scene)
        )

        central = QWidget()
        layout = QHBoxLayout(central)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.view_selected)
        right_layout.addWidget(self.btn_rebase)

        layout.addWidget(self.view_all, stretch=3)
        layout.addLayout(right_layout, stretch=1)

        self.setCentralWidget(central)

    def add_child_in_scene(self):
        self.scene_all.get_children(ret_children())

    def rebase_selected_children(self, scene_1: Scene, scene_2:Scene):
        print(len(scene_1.selectedItems()))
        selected_children = scene_1.get_selected_children()
        if selected_children:
            for child in selected_children:
                scene_1.removeItem(child)
            scene_2.get_children(selected_children)
        scene_2.clearSelection()
        scene_1.clearSelection()


    def view_show(self):
        self.show()

