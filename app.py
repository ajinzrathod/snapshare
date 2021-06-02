from tkinter import Tk, font


class App:
    def __init__(self, master: Tk, font_size) -> None:
        self.master = master

        # Creating a Font object of "TkDefaultFont"
        self.defaultFont = font.nametofont("TkDefaultFont")

        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family="Verdana",
                                   size=font_size,
                                   # weight=font.BOLD
                                   )