# coding=utf-8
import os
import time
import threading
import signal
import searchlive
import yt_dlp
from subprocess import Popen,PIPE

def start(id,status):
    live_status = searchlive.get_live_status(id)
    if status == 0:#past or new
        ydl_opts = {
        'outtmpl': '~/downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])
        #command = "yt-dlp -o ~/downloads/%\(title\)s-%\(id\)s-%\(release_date\)s.%\(ext\)s https://youtu.be/"+id
        #proc = Popen(command,shell=True)
    elif status == 1:#upcoming
        while True:
            if searchlive.get_live_status(id) == "live":
                break
            print("waiting live...")
            time.sleep(60)
        ydl_opts = {
        'outtmpl': '~/downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True,
        'wait_for_video' :(1,30),
        'socket_timeout': '300'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])
        #command = "yt-dlp -o ~/downloads/%\(title\)s-%\(id\)s-%\(release_date\)s.%\(ext\)s https://youtu.be/"+id
        #proc = Popen(command,shell=True)
    elif status == 2:#live
        ydl_opts = {
        'outtmpl': '~/downloads/%(title)s-%(id)s-%(release_date)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist' : True,
        'socket_timeout': '300'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://youtu.be/'+id])
        #command = "yt-dlp -o ~/downloads/%\(title\)s-%\(id\)s-%\(release_date\)s.%\(ext\)s https://youtu.be/"+id
        #proc = Popen(command,shell=True)
    '''command = "yt-dlp -o ~/downloads/%\(title\)s-%\(id\)s-%\(release_date\)s.%\(ext\)s https://youtu.be/"+id
    print(command)
    global proc
    proc = Popen(command,shell=True)
    #os.system(command)
    print("dl")'''

def stop(id):
    time.sleep(7)
    while True:
        if searchlive.get_live_status(id) != "upcoming":
            break
        time.sleep(60)
    getpid = Popen("pgrep -n yt-dlp",stdout=PIPE,shell=True)
    pid_bit = getpid.communicate()[0]
    pid = pid_bit.decode("utf-8")
    while True:
        if searchlive.get_live_status(id) == "past":
            break
        time.sleep(60)
    #for test=====
    '''time.sleep(30)
    while True:
        if searchlive.get_live_status(id) == "live":
            break
        time.sleep(60)'''
    #=====
    Popen("sudo kill -SIGINT "+pid,shell=True)
    #time.sleep(10)
    '''print("============================================================================\n"+str(proc.pid)+"\n=============================================================================")
    Popen("sudo kill -SIGINT $(pgrep yt-dlp)",shell=True)
    #os.kill(proc.pid, signal.SIGINT)
    #os.system("sudo kill -SIGINT $\(pgrep yt-dlp\)")
    print("------------------------------------------------------------------------------------------------------------------------------------------------------stop")'''

#try:
def download(id):
    live_status = searchlive.get_live_status(id)
    if live_status == "new" or live_status == "past":
        start(id,0)
    elif live_status == "upcoming":
        start(id,1)
        '''thread1 = threading.Thread(target = start,args=(id,1,))
        thread2 = threading.Thread(target = stop,args=(id,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()'''
    elif live_status == "live":
        start(id,2)
        '''thread1 = threading.Thread(target = start,args=(id,2,))
        thread2 = threading.Thread(target = stop,args=(id,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()'''
    else:
        pass

def main():
    download("Y_L8TusmUsU")

if __name__ == '__main__':
    main()

'''thread1 = threading.Thread(target = download,args=('USNZDIAN1yU',))
thread2 = threading.Thread(target = stop)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("complete")'''

#--abort-on-unavailable-fragment
#--hls-use-mpegts
#except:
#   print ("Error: 无法启动线程")
