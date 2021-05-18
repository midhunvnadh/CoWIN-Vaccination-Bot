import os
import json
from datetime import date
from datetime import timedelta
from time import sleep
import random
import requests

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
    
def print_response(search_date, response):
    response_len = len(response)
    print("Searched on date: {}, {}".format(search_date.strftime("%d-%m-%Y"), response if (response == [403]) else "Found {} vaccination centers.".format(str(response_len))))
    if(response_len > 0 and response != [403]):
        if(search_date > get_today()):
            print(search_date)
            print(get_today())
            print("Found a vaccination center")
            print(format_json(response))
            siren()
            sleep(2)
            exit()
    elif(response == [403]):
        print("Sleeping for 30s")
        for x in range(30, 0, -1):
            print ("\033[A                             \033[A")
            print("Sleeping for {}s".format(x))
            sleep(1)

def siren():
    os.system('play -nq -t alsa synth {} sine {}'.format(5, 440))

def getRandUserAgent():
    userAgents = requests.get("https://gist.github.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt")
    userAgents = userAgents.content
    lines = userAgents.splitlines()
    line = random.choice(lines)
    return line