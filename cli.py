# python -m eel cli.py static_web --hidden-import='PIL._tkinter_finder'

import eel
import pylib.exposed

if __name__ == '__main__':
    eel.init(".")
    eel.start("./static_web/main.html", mode="default")

