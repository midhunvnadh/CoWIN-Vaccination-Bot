import requests as rq
from functions import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui, QtCore
import sys
from PyQt5 import QtTest
from get_icon_loc import get_icon_loc
import os
from datetime import datetime

class Bot(QMainWindow):
    def __init__(self):
        super().__init__()
        cls()
        self.setWindowTitle("Co-WIN vaccination bot")
        self.hw = {"height":500, "width":400}
        self.setFixedSize(self.hw["width"], self.hw["height"])
        self.setWindowIcon(QIcon(get_icon_loc(f"{get_temp_dir()}/bot_icon.svg")))
        self.showWelcome()
        width = self.hw["width"]
        height = self.hw["height"]
        self.reconfigure_settings = False

        self.botSearchDate = QLabel(f"", self)
        self.botSearchDate.move(0,100)
        self.botSearchDate.resize(width, 80)

        self.centersAvailable = QLabel(f"", self)
        self.centersAvailable.move(0,150)
        self.centersAvailable.resize(width, 80)

        self.responseWait = QLabel(f"", self)
        self.responseWait.move(0,300)
        self.responseWait.resize(width, 20)

        self.search_loc = {"state":get_settings()["state_name"], "district":get_settings()["district_name"]}

        self.reconfigBtn = QPushButton("Reconfigure Settings", self)
        self.reconfigBtn.setIcon(QIcon.fromTheme("view-refresh", QIcon(":/refresh.png")))
        self.reconfigBtn.clicked.connect(lambda: self.reconfigureSettings())
        self.reconfigBtn.move(width-200, 70)
        self.reconfigBtn.resize(180, 40)
        self.reconfigBtn.setCheckable(True)
		
        self.statusBar = QLabel(f"<div><span>Last Updated: loading...</span> | <span>Selected Location: loading...</span></div>", self)
        self.statusBar.move(0,height-30)
        self.statusBar.resize(width, 30)
        self.statusBar.setStyleSheet(
                            "background-color:#eee;"
                            "border-style: solid;"
                            "border-width: 1px;"
                            "border-color: #f2f2f2;")

        self.show()
        self.windowClosed = False


    def botStatus(self):
        location = f"{self.search_loc['district']}, {self.search_loc['state']}"
        last_updated = datetime.now().strftime("%I:%M:%S %p")
        self.statusBar.setText(f"<div><span>Last Updated: {last_updated}</span> | <span>Location: {location}</span></div>")

    def reconfigureSettings(self):
        self.reconfigure_settings = True
        settings_file = f"{get_temp_dir()}/covid_bot_settings.json"
        os.remove(settings_file)
        self.close()
    
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
    
    def data_loop(self):
        self.botStatus()
        search_date = get_nth_day_from_today(0)
        self.botSearchDate.setText(f"<h3><center>Searching centers for 7 days from Today</center></h3>")
        self.show_response(self.getCalendar(search_date, self.district_id))
        QtTest.QTest.qWait(1000)
    
    def startBot(self, district_id):
        self.district_id = district_id
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.data_loop)
        timer.start(100)
    
    def showWelcome(self):
        width = self.hw["width"]
        self.intro = QLabel("<center><h1>Co-WIN slot alert bot</h1></center>", self)
        self.intro.move(0,0)
        self.intro.resize(width, 80)
        self.intro.setStyleSheet(f"width:{width}")

    def closeEvent(self,  event):
        self.windowClosed = True
        super().closeEvent(event)
        if(self.reconfigure_settings == False):
            sys.exit()
        QCoreApplication.quit()

def startBot(dist_id):
    BotApp = QApplication([])
    setupApp = Bot()
    setupApp.startBot(dist_id)
    BotApp.exec_()