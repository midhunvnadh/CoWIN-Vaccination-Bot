import requests as rq
from functions import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5 import QtGui, QtCore
import sys
from get_icon_loc import get_icon_loc

class Setup(QMainWindow):
    def __init__(self):
        super().__init__()
        cls()
        self.startBot = False
        self.setWindowTitle("Co-WIN vaccination bot")
        self.hw = {"height":500, "width":400}
        self.setFixedSize(self.hw["width"], self.hw["height"])
        self.setWindowIcon(QIcon(get_icon_loc(f"{get_temp_dir()}/bot_icon.svg")))

        self.showWelcome()
        self.show()

    def showWelcome(self):
        width = self.hw["width"]
        self.intro = QLabel("<center><h1>Co-WIN bot</h1></center>", self)
        self.intro.move(0,0)
        self.intro.resize(width, 80)
        self.intro.setStyleSheet(f"width:{width}")

    def saveSettings(self, districts, filename, stateName):
        width = self.hw["width"]
        districtName = self.dist_dropdown.currentText()
        if districtName == "SELECT":
            ()
        else:
            district_id = get_id_from_list(districts, {"name":"district_name", "id":"district_id"}, districtName)
            setting = {
                "state_name":stateName,
                "district_name":districtName,
                "district_id":district_id
            }
            with open(filename, 'w') as fp:
                json_data = json.dumps(setting)
                fp.write(json_data)
                self.finished_label = QLabel("<center><h2>Settings saved.</h2></center>", self)
                self.finished_label.move(10, 210)
                self.finished_label.resize(width-25, 80)
                self.exitBtn = QPushButton("Restart", self)
                self.exitBtn.move((width/2)-50, 300)
                self.exitBtn.resize(100, 50)
                self.exitBtn.setCheckable(True)
                self.exitBtn.clicked.connect(self.startBotFunc)
            self.exitBtn.show()
            self.finished_label.show()
    def startBotFunc(self):
        self.startBot = True
        self.close()
        
    def selectDistrict(self, states, filename):
        width = self.hw["width"]
        stateName = self.dropdown.currentText()
        if(stateName == "SELECT"):
            ()
        else:
            state_id = get_id_from_list(states, {"name":"state_name", "id":"state_id"}, stateName)
            districts = sorted(get_districts(state_id)["districts"], key = lambda i: i["district_id"])
            options = ["SELECT"]
            for district in districts:
                options.append(district["district_name"])
            
            self.sel_state_label.setText("<h2>Select your district</h2>")

            self.dist_dropdown = QComboBox(self)
            self.dist_dropdown.move(10,175)
            self.dist_dropdown.resize(width-25, 40)
            self.dist_dropdown.addItems(options)
            self.dist_dropdown.currentIndexChanged.connect(lambda: self.saveSettings(districts, filename, stateName))

            self.dist_dropdown.show()
    
    def selectState(self, states, filename):
        options = ["SELECT"]
        for state in states:
            options.append(state["state_name"])
        width = self.hw["width"]
        
        self.sel_state_label = QLabel("<h2>Select your state</h2>", self)
        self.sel_state_label.move(10, 60)
        self.sel_state_label.resize(width, 80)

        self.dropdown = QComboBox(self)
        self.dropdown.move(10,130)
        self.dropdown.resize(width-25, 40)
        self.dropdown.addItems(options)
        self.dropdown.currentIndexChanged.connect(lambda: self.selectDistrict(states, filename))

        self.dropdown.show()
        self.sel_state_label.show()

    def setup(self, filename):
        states = sorted(get_states()["states"], key = lambda i: i["state_id"])
        self.selectState(states, filename)
    def closeEvent(self, event):
        self.windowClosed = True
        super().closeEvent(event)
        if(self.startBot == False):
            sys.exit()


def startSetup(filename):
    App = QApplication([])
    setupApp = Setup()
    setupApp.setup(filename)
    App.exec_()