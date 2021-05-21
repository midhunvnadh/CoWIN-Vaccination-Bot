import requests as rq
from functions import *

def get_states():
    states = rq.get(
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
        sleepNow(5)
        return get_states()
def get_districts(state_id):
    districts = rq.get(
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
        sleepNow(5)
        return get_districts(state_id)
def setup(filename):
    cls()
    states = sorted(get_states()["states"], key = lambda i: i["state_id"])
    state_id = chooseState(states)
    districts = sorted(get_districts(state_id)["districts"], key = lambda i: i["district_id"])
    district_id = chooseDistrict(districts)
    setting = {
        "state_id":state_id,
        "district_id":district_id
    }
    with open(filename, 'w') as fp:
        json_data = json.dumps(setting)
        fp.write(json_data)