# coding=utf-8
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
APIKEY = config.get("holodex","x-apikey")
if APIKEY == 'None':
    X_APIKEY = None
else:
    X_APIKEY = APIKEY

def get_live(channel,max_upcoming_hours="8"):
    url = "https://holodex.net/api/v2/live"

    querystring = {"limit":"1"}
    querystring['channel_id'] = channel
    querystring['max_upcoming_hours'] = max_upcoming_hours

    headers = {'Content-Type': 'application/json'}
    headers['x-apikey'] = X_APIKEY
    #file = "hololive_channels.txt"

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_0 = json.loads(response.text)
    if len(response_0) > 0:
        live_dict = response_0[0]
        return live_dict
    else:
        return 0

def get_live_status(id):
    url = "https://holodex.net/api/v2/videos/"+id

    headers = {'Content-Type': 'application/json'}
    headers['x-apikey'] = X_APIKEY

    response = requests.request("GET", url, headers=headers)
    live_dict = json.loads(response.text)
    if len(live_dict) > 0:
        return live_dict.get("status",0)
    else:
        return 0

def get_live_status_by_holotools(id):
    url = "https://api.holotools.app/v1/videos/youtube/"+id

    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers)
    live_dict = json.loads(response.text)
    if len(live_dict) > 0:
        return live_dict.get("status",0)
    else:
        return 0

def get_live_detail(id):
    url = "https://holodex.net/api/v2/videos/"+id

    headers = {'Content-Type': 'application/json'}
    headers['x-apikey'] = X_APIKEY

    response = requests.request("GET", url, headers=headers)
    live_dict = json.loads(response.text)
    if len(live_dict) > 0:
        return live_dict
    else:
        return 0

def get_channel_detail(id):
    url = "https://holodex.net/api/v2/channels/"+id

    headers = {'Content-Type': 'application/json'}
    headers['x-apikey'] = X_APIKEY

    response = requests.request("GET", url, headers=headers)
    channel_dict = json.loads(response.text)
    if len(channel_dict) > 0:
        return channel_dict
    else:
        return 0

def main():
    print(get_channel_detail("UCvInZx9h3jC2JzsIzoOebWg"))


if __name__ == '__main__':
    main()
