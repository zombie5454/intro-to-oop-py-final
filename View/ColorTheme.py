from types import SimpleNamespace
from PyQt5 import QtCore


class Theme(SimpleNamespace):
    DARK = SimpleNamespace(
        button_text="深色模式", 
        button_text_EN="Dark",    # used for English version
        text_color="white",
        button_color="gainsboro",
        background_1="#17181e",
        background_2="#2d313c",
        button_hover="#535865",
        button_disabled="#1d2029",
        list_hover="#3a3e49",
        list_selected="#535865",
        success_color="#00ec00",
        error_color="#f75000",
    )
    LIGHT = SimpleNamespace(
        button_text="淺色模式",
        button_text_EN="Light",    # used for English version
        text_color="black",
        button_color="black",
        background_1="#f0f0f0",
        background_2="#fafafa",
        button_hover="#e0e0e0",
        button_disabled="#fafafa",
        list_hover="#ebebeb",
        list_selected="#e0e0e0",
        success_color="#00bb00",
        error_color="#ea0000",
    )


class ColorTheme(object):
    def __init__(self, theme=Theme.DARK):
        file = QtCore.QFile("./UI/base.qss")
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(file)
        self.qss = stream.readAll()
        self.style = ""
        self.theme = theme
        self.change_theme(theme)

    def toggle_theme(self):
        if self.theme is Theme.DARK:
            self.change_theme(Theme.LIGHT)
        else:
            self.change_theme(Theme.DARK)

    def change_theme(self, theme: Theme):
        self.style = (
            self.qss.replace("$text_color", theme.text_color)
            .replace("$button_color", theme.button_color)
            .replace("$background_1", theme.background_1)
            .replace("$background_2", theme.background_2)
            .replace("$button_hover", theme.button_hover)
            .replace("$button_disabled", theme.button_disabled)
            .replace("$list_hover", theme.list_hover)
            .replace("$list_selected", theme.list_selected)
        )
        self.theme = theme
