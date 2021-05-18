#! /bin/python3
import requests
from requests.models import Response
from functions import *
from time import sleep
import datetime


def get_response(date):
	date = str(date.strftime("%d-%m-%Y"))
	sessions = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict",
        params={'district_id': 298, 'date': date},
        headers={
			'User-Agent': getRandUserAgent(),
			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
		}
    )
	try:
		response = sessions.json()
		JSON_r = response["sessions"]
	except:
		JSON_r = [403]
	return JSON_r

def startBot():
	print("Starting bot at {} \n\n\n".format(str(datetime.datetime.now())))
	dates_to_search = []
	for days in range(-3, 45):
		dates_to_search.append(get_nth_day_from_today(days))
	for date in dates_to_search:
		print_response(date, get_response(date))
		sleep(1)
	cls()

while(True):
	cls()
	startBot()