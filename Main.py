import sys
from PyQt5 import QtWidgets
from View.ViewQt import View


class App(QtWidgets.QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.view = View()
        self.view.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
