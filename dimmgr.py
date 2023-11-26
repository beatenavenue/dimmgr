import os
import subprocess

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QSystemTrayIcon

import icons_binary

home = os.environ['HOME']

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

pixmap = QPixmap()
pixmap.loadFromData(icons_binary.icon_1f4a1)
v_icon = QIcon(pixmap)
pixmap.loadFromData(icons_binary.icon_1f31e)
sun_icon = QIcon(pixmap)
pixmap.loadFromData(icons_binary.icon_1f31b)
moon_icon = QIcon(pixmap)

day_value = 3600
night_value = 300

tray = QSystemTrayIcon()
tray.setIcon(v_icon)
tray.setVisible(True)


def get_current_value():
  cmd_str = (f'/usr/bin/kreadconfig5 --file {home}/.config/powermanagementprofilesrc '
             '--group AC --group DPMSControl --key idleTime')
  result = subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, text=True)
  return result.stdout.strip()


def update_status():
  current = get_current_value()

  if current == str(day_value):
    tray.setIcon(sun_icon)
  elif current == str(night_value):
    tray.setIcon(moon_icon)
  else:
    tray.setIcon(v_icon)


def set_day():
  set_value(day_value)


def set_night():
  set_value(night_value)


def set_value(value):
  cmd_str1 = (f'/usr/bin/kwriteconfig5 --file {home}/.config/powermanagementprofilesrc '
              f'--group AC --group DPMSControl --key idleTime --type int {value}')
  cmd_str2 = ('/usr/bin/qdbus org.kde.Solid.PowerManagement '
              '/org/kde/Solid/PowerManagement org.kde.Solid.PowerManagement.refreshStatus')
  subprocess.run(cmd_str1, shell=True)
  subprocess.run(cmd_str2, shell=True)


menu = QMenu()
option_day = QAction('SET DAY')
option_day.triggered.connect(set_day)
option_night = QAction('SET NIGHT')
option_night.triggered.connect(set_night)
menu.addAction(option_day)
menu.addAction(option_night)

quit = QAction('Quit')
quit.triggered.connect(app.quit)
menu.addAction(quit)

tray.setContextMenu(menu)

timer = QTimer()
timer.timeout.connect(update_status)
timer.start(5000)

app.exec_()
