import requests as rq
from functions import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui, QtCore
import sys
import datetime
import time
from PyQt5 import QtTest
from get_icon_loc import get_icon_loc

class Bot(QMainWindow):
    def __init__(self):
        super().__init__()
        cls()
        self.setWindowTitle("Co-WIN vaccination bot")
        self.hw = {"height":500, "width":400}
        self.setFixedSize(self.hw["width"], self.hw["height"])
        self.setWindowIcon(QIcon(get_icon_loc("/tmp/bot_icon.svg")))
        self.showWelcome()
        width = self.hw["width"]

        self.botSearchDate = QLabel(f"", self)
        self.botSearchDate.show()
        self.botSearchDate.move(0,100)
        self.botSearchDate.resize(width, 80)

        self.centersAvailable = QLabel(f"", self)
        self.centersAvailable.show()
        self.centersAvailable.move(0,200)
        self.centersAvailable.resize(width, 80)

        self.responseWait = QLabel(f"", self)
        self.responseWait.show()
        self.responseWait.move(0,300)
        self.responseWait.resize(width, 20)

        self.completed = 0
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, 180, width-20, 15)
		
        self.show()
        self.windowClosed = False

    def getCalendar(self, date, district_id):
        dateQ = str(date.strftime("%d-%m-%Y"))
        sessions = requests.get(
            "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
            params={'district_id': district_id, 'date': dateQ},
            headers={
                'User-Agent': getRandUserAgent(),
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
            }
        )
        try:
            response = sessions.json()
            JSON_r = response["centers"]
        except:
            self.showResponseWait(True)
            return self.getCalendar(date, district_id)
        if(sessions.status_code != 200):
            self.showResponseWait(True)
            return self.getCalendar(date, district_id)        
        self.showResponseWait(False)
        return JSON_r
    def showResponseWait(self, show):
        if(show):
            self.responseWait.show()
            for secs in range(30, 0, -1):
                self.responseWait.setText(f"<center><h3>Waiting for response from server... {secs}s</h3></center>")
                QtTest.QTest.qWait(1000)
        else:
            self.responseWait.hide()
    def show_response(self, JSON_d):
        centersAvailable = JSON_d
        centersLength = len(centersAvailable)
        self.centersAvailable.setText(f"<h3><center>{centersLength} Centers Available</center></h3>")
    def startBot(self, district_id):
        while not self.windowClosed:
            self.completed = 0
            for days in range(0, 10):
                self.completed += 10
                search_date = get_nth_day_from_today(days*7)
                self.botSearchDate.setText(f"<h3><center>Searching for 7 days from {search_date.strftime('%d-%m-%Y')}</center></h3>")
                self.show_response(self.getCalendar(search_date, district_id))
                self.progress.setValue(self.completed)
                QtTest.QTest.qWait(1000)
    def showWelcome(self):
        width = self.hw["width"]
        self.intro = QLabel("<center><h1>Co-WIN slot alert bot</h1></center>", self)
        self.intro.move(0,0)
        self.intro.resize(width, 80)
        self.intro.setStyleSheet(f"width:{width}")

    def closeEvent(self, *args, **kwargs):
        self.windowClosed = True
        super(QMainWindow, self).closeEvent(*args, **kwargs)
        exit()

def startBot(dist_id):
    App = QApplication(sys.argv)
    setupApp = Bot()
    setupApp.startBot(dist_id)
    sys.exit(App.exec())