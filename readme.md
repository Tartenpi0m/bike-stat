# Stat bike

## Install

- Install Python3 
- Create virtual environnement : ```python3 -m venv .venv```
- Activate .venv : ```source .venv/bin/activate```
- Install requirements : ```pip install -r requirements```
- Run app : ```python3 cli.py```

## Create executable

Creating an executable avoid to have python and dependencies install on your machine. Consequently you can share the executable with other person using the same OS and 64/32bit architecture than you.

- Follow the "Install" part
- Install PyInstaller (.venv need to be activated) : ```pip install pyinstaller==5.6.2 pyinstaller-hooks-contrib==2022.13```
- Execute PyInstaller : ```python -m eel cli.py static_web --hidden-import='PIL._tkinter_finder'```
- Create an empty directory "cache" in "/dist/cli" folder : [from "bike-stat" folder] ```mkdir ./dist/cli/cache```
- You can know share the "cli" folder as mentionned and uninstall python (optionnal)

Warning : The option --onefile of PyInstaller doesn't work for now