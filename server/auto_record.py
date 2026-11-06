# coding=utf-8
import os
import time
import threading
import signal
import searchlive
import yt_dlp
from subprocess import Popen,PIPE

def get_live_id(channel_id):
    #live_dict = searchlive.get_live(id)
    #return searchlive.get_live(id)
    live = searchlive.get_live(channel_id)
    if live != 0:
        live_title = live["title"]
        print(live_title)
        return live["id"]
        '''live_title = live_title.lower()
        if "unarchived" in live_title:
            return live["id"]'''

def download(id):
    live_status = searchlive.get_live_status(id)
    print(live_status)
    if live_status == "past" or live_status == "new":
        print("1")
        ydl_opts = {
        'outtmpl': '~/downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
           ydl.download(['https://youtu.be/'+id])
    elif live_status == "upcoming":
        print("2")
        '''while True:
            if searchlive.get_live_status_by_holotools(id) == "live":
                break
            print("waiting live...")
            time.sleep(60)'''
        ydl_opts = {
        'outtmpl': '~/downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True,
        'wait_for_video' :(1,30),
        'socket_timeout': '300'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])
    elif live_status == "live":
        print("3")
        ydl_opts = {
        'outtmpl': '~/downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True,
        'live_from_start' : True,
        'socket_timeout': '300'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])

def main():
    while True:
        #live_id = get_live_id('UC3n5uGu18FoCy23ggWWp8tA')
        live_id = get_live_id('UCp-5t9SrOQwXMU7iIjQfARg')
        if live_id != 0:
            download(live_id)
            print('download '+live_id)
        else:
            time.sleep(60*5)
    #download("N9ONwqivAN0")

if __name__ == '__main__':
    main()
