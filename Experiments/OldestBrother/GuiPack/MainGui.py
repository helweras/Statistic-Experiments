import sys

from MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())