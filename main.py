import sys
from PyQt5.QtWidgets import QApplication
from windowclass import Window


class AppWindow(Window):
    def __init__(self):
        super().__init__()
        self.ui = Window()
        self.ui.setup_ui(self)
        self.show()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())

