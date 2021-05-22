import os
import json
from datetime import date
from datetime import timedelta
from time import sleep
import random
import requests
import tempfile
from pathlib import Path

def cls():
    if os.name == 'posix':
        _ = os.system('reset')
    else:
        _ = os.system('cls')


def format_json(jsonI):
    return json.dumps(jsonI, indent=4, sort_keys=True)


def get_today():
    return date.today()

def get_nth_day_from_today(n):
    return date.today() + timedelta(days=n)

def siren():
    os.system('play -nq -t alsa synth {} sine {}'.format(5, 440))

def getRandUserAgent():
    try:
        userAgents = requests.get("https://gist.github.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt")
    except:
        sleep(1000)
        return getRandUserAgent()

    if(userAgents.status_code != 200):
        sleep(1000)
        return getRandUserAgent()
    else:
        userAgents = userAgents.content
        lines = userAgents.splitlines()
        line = random.choice(lines)
        return line

def get_id_from_list(list, position, chosen):
    for that in list:
        if that[position["name"]] == chosen:
            return that[position["id"]]

def get_states():
    states = requests.get(
        "https://cdn-api.co-vin.in/api/v2/admin/location/states",
        headers={
            'User-Agent': getRandUserAgent(),
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
        }
    )
    try: 
        theStates = states.json()
        return theStates
    except: 
        sleep(5)
        return get_states()
def get_districts(state_id):
    districts = requests.get(
        "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id),
        headers={
            'User-Agent': getRandUserAgent(),
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
        }
    )
    try: 
        theDistricts = districts.json()
        return theDistricts
    except: 
        sleep(5)
        return get_districts(state_id)

def get_temp_dir():
    return tempfile.gettempdir()

def get_settings():
    settings_file = f"{get_temp_dir()}/covid_bot_settings.json"
    settings_file_exists = Path(settings_file).is_file()
    if(settings_file_exists is False):
        settings_file = "./settings.json"
    settings_file = open(settings_file, "r")
    settings_params = json.load(settings_file)
    return settings_params