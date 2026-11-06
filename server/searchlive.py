# coding=utf-8
import os
import requests
import json

API_KEY = os.environ.get("HOLODEX_API_KEY", "")

def get_live(channel,max_upcoming_hours="8"):
    url = "https://holodex.net/api/v2/live"

    querystring = {"limit":"1"}
    querystring['channel_id'] = channel
    querystring['max_upcoming_hours'] = max_upcoming_hours

    headers = {'Content-Type': 'application/json',"X-APIKEY" : API_KEY}

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

    headers = {'Content-Type': 'application/json',"X-APIKEY" : API_KEY}

    response = requests.request("GET", url, headers=headers)
    live_dict = json.loads(response.text)
    if len(live_dict) > 0:
        return live_dict["status"]
    else:
        return 0

def get_live_status_by_holotools(id): #broken
    url = "https://api.holotools.app/v1/videos/youtube/"+id

    headers = {'Content-Type': 'application/json'}

    response = requests.request("GET", url, headers=headers)
    live_dict = json.loads(response.text)
    if len(live_dict) > 0:
        return live_dict["status"]
    else:
        return 0

def get_live_detail(id):
    url = "https://holodex.net/api/v2/videos/"+id

    headers = {'Content-Type': 'application/json',"X-APIKEY" : API_KEY}

    response = requests.request("GET", url, headers=headers)
    live_dict = json.loads(response.text)
    if len(live_dict) > 0:
        return live_dict
    else:
        return 0

def main():
    print(get_live("UCFTLzh12_nrtzqBPsTCqenA"))

if __name__ == '__main__':
    main()



'''
[
{"id":"uhyqNbP9Ia8",
    "title":"【ARK Lost Island】わわわわワイバーン!?【不知火フレア/ホロライブ】",
    "type":"stream",
    "topic_id":"ark",
    "published_at":"2022-01-18T16:06:06.000Z",
    "available_at":"2022-01-18T16:30:57.000Z",
    "duration":0,
    "status":"live",
    "start_scheduled":"2022-01-18T16:30:00.000Z",
    "start_actual":"2022-01-18T16:30:57.000Z",
    "live_viewers":8347,
    "channel":{"id":"UCvInZx9h3jC2JzsIzoOebWg","name":"Flare Ch. 不知火フレア","org":"Hololive","type":"vtuber","photo":"https://yt3.ggpht.com/d9aIrGtZR0eI4k1Wnev5f_R4llIBsWnQOjkdsqkMycoAxA3g_zz-jyeBl8tEHfbm1iTg0SJj=s800-c-k-c0x00ffffff-no-rj","english_name":"Shiranui Flare"}
    }
    ]
'''
