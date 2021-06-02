from tkinter import Tk, PhotoImage
from sys import platform

from app import App
from on_system_start import start_on_boot_enabled
from MainWindow import MainWindow
import settings
import os


def main():
	root = Tk()
	root.title(settings.APP_NAME)
	root.geometry(str(settings.ROOT_WIDTH) + "x" + str(settings.ROOT_HEIGHT))
	root.configure(bg="white")

	# https://stackoverflow.com/questions/11176638/tkinter-tclerror-error-reading-bitmap-file
	# give correct path for live use
	# ICO_FILE = os.path.join(ROOT_DIR, "./snapshare.png")
	# XPM_FILE = os.path.join(ROOT_DIR, "./@snapshare.xpm")
	ICO_FILE = os.path.join("images/snapshare.png")
	XPM_FILE = os.path.join("images/@snapshare.xpm")
	print(ICO_FILE)
	print(XPM_FILE)

	# https://stackoverflow.com/questions/11176638/tkinter-tclerror-error-reading-bitmap-file
	if platform == "linux":
		BITMAP_IMG = PhotoImage(file=XPM_FILE)
	else:
		BITMAP_IMG = PhotoImage(file=ICO_FILE)
	root.tk.call('wm', 'iconphoto', root._w, BITMAP_IMG)

	App(root, settings.FONT_SIZE)
	AUTO_START = start_on_boot_enabled()
	print("AUTO_START", AUTO_START)

	ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
	MainWindow(root, AUTO_START, ROOT_DIR)



	root.mainloop()


if __name__ == '__main__':
	print("Jai Swaminarayan")
	# Rename this file.
	main()