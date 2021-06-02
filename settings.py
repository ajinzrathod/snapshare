import os


def print_settings_data():
	print("DEBUG", DEBUG)
	# print("ROOT_DIR", ROOT_DIR)
	print("APP_NAME", APP_NAME)
	print("APP_AUTHOR", APP_AUTHOR)
	# print("ICO_FILE", ICO_FILE)
	# print("XPM_FILE", XPM_FILE)
	print("platform", platform)
	print("BITMAP_IMG", BITMAP_IMG)
	print("ROOT_WIDTH", ROOT_WIDTH)
	print("ROOT_HEIGHT", ROOT_HEIGHT)
	print("FONT_SIZE", FONT_SIZE)
	print()


# everywhere name must be "snapshare", no space and all small
# will change if any probelm occurs, till then do not
APP_NAME = "SnapShare"
APP_AUTHOR = "Ghanshyam Maharaj"
DEBUG = False
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

ROOT_WIDTH = 525
ROOT_HEIGHT = 500
FONT_SIZE = 12