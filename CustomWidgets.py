from tkinter import (Button, Canvas)


# HoverButton:
# https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        pass

    def on_leave(self, e):
        pass


class Seperator:
    def draw_seperator(root_width, master, transparent=False):
        winx = root_width
        # winx = root_width - (root_width * 10 / 100)
        winy = 10

        w = Canvas(
            master,
            width=winx, height=winy,
            bg="white",
            highlightthickness=0)

        if transparent:
            w.create_rectangle(
                0, 0, root_width, 2,
                fill="white", outline="")
        else:
            w.create_rectangle(
                0, 0, root_width, 2,
                fill="#ddd", outline="")
        return w
