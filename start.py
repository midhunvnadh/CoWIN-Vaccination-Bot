#! /bin/python3
import json
from pathlib import Path
from functions import get_temp_dir
from functions import get_settings

from setup import startSetup
from bot import startBot
from functions import cls

def startProgram(file, createFile):
    settings_file_name = file
    settings_file_exists = Path(settings_file_name).is_file()
    if (settings_file_exists):
        try:
            district_id = get_settings()["district_id"]
            print(district_id)
        except:
            startSetup(settings_file_name)
            startProgram(settings_file_name, False)
        startBot(district_id)
    else:
        if(createFile):
            startSetup(settings_file_name)
        startProgram(f"{get_temp_dir()}/covid_bot_settings.json", True)

def main():
    startProgram("./settings.json", False)

if __name__ == "__main__":
    while True:
       main()