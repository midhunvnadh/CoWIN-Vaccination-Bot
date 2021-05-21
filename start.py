import json
from pathlib import Path


from setup import setup
from vaccine_bot import initBot
from functions import cls

def startProgram():
    cls()
    settings_file_name = "./settings.json"
    settings_file_exists = Path(settings_file_name).is_file()
    if (settings_file_exists):
        try:
            settings_file = open(settings_file_name, "r")
            settings_params = json.load(settings_file)
            district_id = settings_params["district_id"]
        except:
            setup(settings_file_name)
            startProgram()
        initBot(district_id)
    else:
        setup(settings_file_name)
        startProgram()
startProgram()