import os
import time
from dotenv import load_dotenv
import numpy as np
import requests
from http.client import HTTPException
import base64
from IPython.core import display

load_dotenv()
_USERNAME = os.getenv("SPLUNK_USERNAME")
_PASSWORD = os.getenv("SPLUNK_PASSWORD")
_SEARCH_URL = os.getenv("SPLUNK_SEARCH_URL")
_MAX_COUNT = 100
_STATUS_BUCKETS = 300
_SPLUNK_SLEEP_SECONDS = 2
id = 0

if _SEARCH_URL == None:
    raise Exception("Splunk search url not found")
if _USERNAME == None:
    raise Exception("Splunk username not found")
if _PASSWORD == None:
    raise Exception("Splunk password not found")


def bearer_header(token):
    return { "Authorization": "Bearer " + token }

def basic_auth(username, password):
    return { "Authorization": "Basic " + base64.b64encode((username + ":" + password).encode('utf-8')).decode('utf-8') }

def send_request(query):
    global id
    searchId = "splunk_query_" + str(id)
    id += 1
    payload = {
        "id": searchId,
        "search": "search " + query,
        "max_count": _MAX_COUNT,
        "status_buckets": _STATUS_BUCKETS,
        "earliest_time": "-24h"
    }

    r = requests.post(_SEARCH_URL, headers = basic_auth(_USERNAME, _PASSWORD), data = payload, verify = False)

    if r.status_code == 200 or r.status_code == 201:
        return searchId
    else:
        print(r.reason)
        raise HTTPException("Splunk service returned status code: " + str(r.status_code) + " while sending request")


def get_status(search_id):
    r = requests.get(_SEARCH_URL + "/{}".format(search_id), headers = basic_auth(_USERNAME, _PASSWORD), params = { 'output_mode': 'json' }, verify = False)
    
    if r.status_code == 200:
        json_response = r.json()
        return (json_response['entry'][0]['content']['doneProgress'], json_response['entry'][0]['content']['dispatchState'])
    else:
        raise HTTPException("Splunk service returned status code: " + str(r.status_code) + " while getting status")

def fetch_result(search_id):
    r = requests.get(_SEARCH_URL + "/{}/results".format(search_id), headers = basic_auth(_USERNAME, _PASSWORD), verify = False, params = { 
        'output_mode': 'json_rows',
         })

    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException("Splunk service returned status code: " + str(r.status_code) + " while fetching result")

def execute(query):
    search_id = send_request(query)

    done_progress = 0
    while done_progress != 1:
        (done_progress, dispatch_state) = get_status(search_id)

        if done_progress != 1:
            time.sleep(_SPLUNK_SLEEP_SECONDS)
    
    json_response = fetch_result(search_id)
    return format_splunk_response(json_response)



def format_splunk_response(response):
    formatted_response = {}
    formatted_response['columns'] = np.array(response['fields'])
    formatted_response['rows'] = np.array(response['rows'])
    formatted_response['column_types'] = None
    return formatted_response