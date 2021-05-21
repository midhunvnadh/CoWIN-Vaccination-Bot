#! /bin/python3
import requests
from requests.models import Response
from functions import *
from time import sleep
import datetime


def get_response(date, district_id):
	date = str(date.strftime("%d-%m-%Y"))
	sessions = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
        params={'district_id': district_id, 'date': date},
        headers={
			'User-Agent': getRandUserAgent(),
			'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"'
		}
    )
	try:
		response = sessions.json()
		print(response)
		JSON_r = response["centers"]
	except:
		JSON_r = [403]
	return JSON_r

def startBot(district_id):
	print(f"Starting bot at {str(datetime.datetime.now())} \nAimed at district_id: {district_id} \n\n\n")
	dates_to_search = []
	for days in range(0, 10):
		dates_to_search.append(get_nth_day_from_today(days*7))
	for date in dates_to_search:
		print_response(date, get_response(date, district_id))
		sleep(1)
	cls()

def initBot(district_id):
	while(True):
		startBot(district_id)
