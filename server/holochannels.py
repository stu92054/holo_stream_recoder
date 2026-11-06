# coding=utf-8
import requests
import json
import time

def get_channels_id():
    url = "https://api.holotools.app/v1/channels/"

    querystring0 = {"limit":"50"}
    querystring1 = {"limit":"50","offset":"50"}

    headers = {'Content-Type': 'application/json'}

    file = "hololive_channels_id.txt"

    response0 = requests.request("GET", url, headers=headers, params=querystring0)
    response1 = requests.request("GET", url, headers=headers, params=querystring1)
    response_0 = json.loads(response0.text)
    response_1 = json.loads(response1.text)
    channel_list0 = response_0['channels']
    channel_list1 = response_1['channels']
    channel_list = channel_list0 + channel_list1

    #print(channel_list)
    hololive_channels=[]

    f = open(file, 'w', encoding='utf-8')
    f.write("update_time:"+str(time.time())+"\n")
    for channel in channel_list:
        name = channel['name']
        id = channel['id']
        yt_id = channel['yt_channel_id']
        twitter_link = channel['twitter_link']
        #print(str(id)+' '+name)
        f.write(yt_id+'\n')
        channel_detail = {"holotools_id":id,"name":name,"yt_id":yt_id,"twitter_link":twitter_link}
        hololive_channels.append(channel_detail)
    #print(hololive_channels)
    f.close()
    return hololive_channels

def get_channels():
    url = "https://api.holotools.app/v1/channels/"

    querystring0 = {"limit":"50"}
    querystring1 = {"limit":"50","offset":"50"}

    headers = {'Content-Type': 'application/json'}

    file = "hololive_channels.txt"

    response0 = requests.request("GET", url, headers=headers, params=querystring0)
    response1 = requests.request("GET", url, headers=headers, params=querystring1)
    response_0 = json.loads(response0.text)
    response_1 = json.loads(response1.text)
    channel_list0 = response_0['channels']
    channel_list1 = response_1['channels']
    channel_list = channel_list0 + channel_list1

    #print(channel_list)
    hololive_channels=[]

    f = open(file, 'w', encoding='utf-8')
    f.write("update_time:"+str(time.time())+"\n")
    for channel in channel_list:
        name = channel['name']
        id = channel['id']
        yt_id = channel['yt_channel_id']
        twitter_link = channel['twitter_link']
        #print(str(id)+' '+name)
        f.write("holotools_id,"+str(id)+','+"name,"+name+','+"yt_id,"+yt_id+','+"twitter_link,"+twitter_link+'\n')
        channel_detail = {"holotools_id":id,"name":name,"yt_id":yt_id,"twitter_link":twitter_link}
        hololive_channels.append(channel_detail)
    #print(hololive_channels)
    f.close()
    return hololive_channels


def main():
    print(get_channels_id())

if __name__ == '__main__':
    main()
