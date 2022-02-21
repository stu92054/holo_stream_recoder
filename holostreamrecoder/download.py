# coding=utf-8
import os
import time
import threading
import searchlive
import yt_dlp

def start(id,status):
    live_status = searchlive.get_live_status(id)
    if status == 0:#past or new
        ydl_opts = {
        'outtmpl': './downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])

    elif status == 1:#upcoming
        while True:
            if searchlive.get_live_status_by_holotools(id) == "live":
                break
            if searchlive.get_live_status(id) == "live":
                break
            print("waiting live...")
            time.sleep(60)
        ydl_opts = {
        'outtmpl': './downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True,
        'wait_for_video' :(1,30),
        'socket_timeout': '300'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])

    elif status == 2:#live
        ydl_opts = {
        'outtmpl': './downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True,
        'socket_timeout': '300'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])


def download(id):
    live_status = searchlive.get_live_status_by_holotools(id)
    if live_status == 0:
        live_status = searchlive.get_live_statu(id)
    if live_status == "new" or live_status == "past":
        start(id,0)
    elif live_status == "upcoming":
        start(id,1)
    elif live_status == "live":
        start(id,2)
    else:
        pass

def main():
    download("9yBLZKFKXyg")

if __name__ == '__main__':
    main()
