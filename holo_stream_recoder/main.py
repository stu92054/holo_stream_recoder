# coding=utf-8
import time
import searchlive
import download
import configparser
from uuid import UUID
from datetime import datetime
from threading import Thread

def check_uuid4(test_uuid,version=4):
    try:
        return UUID(test_uuid).version == version
    except ValueError:
        return False

def init_set():
    print("請登入Holodex網站(https://holodex.net/)，")
    print("點選右上角帳號圖標，並在彈出選單中選擇帳號設定")
    print("拉到該頁面的最下方，取得API金鑰後將他貼在下方\n")
    print("您也可以直接按enter鍵跳過這個步驟，")
    print("但是未設定金鑰將有機率被Holdex拒絕服務而導致程式錯誤\n")
    while True:
        apikey=input("請輸入您的Holodex API金鑰：")
        if apikey == "":
            print("未設定金鑰，返回主選單\n")
            time.sleep(1)
            return
        elif check_uuid4(apikey):
            config = configparser.ConfigParser()
            config.read('config.ini')
            config['holodex']['x-apikey']=apikey
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            print("設定成功，返回主選單\n")
            time.sleep(1)
            return
        else:
            print("金鑰格式不符，請重新設定\n")

def set_mode():
    while True:
        print("使用模式列表:")
        print("(1).下載單支影片或直播")
        print("(2).紀錄特定頻道未來所有直播與影片")
        print("(3).紀錄特定頻道特定標題直播與影片")
        print("(s)et.設定Holodex API金鑰")
        print("(e)xit.離開本服務\n")
        mode = input("請選擇使用模式(1/2/3/s/e)：")
        if mode == "1":
            print("使用模式1：下載單支影片或直播")
            return mode
        elif mode == "2":
            print("使用模式2：紀錄特定頻道未來所有直播與影片")
            return mode
        elif mode == "3":
            print("使用模式3：紀錄特定頻道特定標題直播與影片")
            return mode
        elif mode == "set" or mode == "s":
            print("設定Holodex API金鑰")
            return "set"
        elif mode == "exit" or mode == "e":
            print("感謝您使用本服務")
            return "exit"
        else:
            print("請輸入數字1或2或3或字母s或e\n")
            time.sleep(1)

def set_live_id():
    while True:
        print("\n\n請輸入影片或直播網址或ID\n例如：\nhttps://www.youtube.com/watch?v=9yBLZKFKXyg 或是")
        print("https://youtu.be/9yBLZKFKXyg 或是")
        print("9yBLZKFKXyg\n")
        id = input("請輸入影片或直播網址或ID：")
        if 'youtu.be' in id:
            id = id.split('/')[-1]
        elif 'youtube' in id:
            id = id.split('v=')[-1]
        elif id == "":
            print("\n請輸入影片或直播網址或ID：\n")
            continue
        try:
            live = searchlive.get_live_detail(id)
        except:
            print("\n無法找到影片或直播，可能是網址格式錯誤或不支援的影片或直播\n")
            time.sleep(1)
        else:
            if live.get('title', 0) != 0:
                print("您要記錄的影片或直播為"+live.get('title', 0))
                return id
            else:
                print("\n無法找到影片或直播，可能是網址格式錯誤或不支援的影片或直播\n")
                time.sleep(1)

def set_channel_id():
    while True:
        print("\n\n請輸入頻道網址或ID\n例如：\nhttps://www.youtube.com/channel/UC-hM6YJuNYVAmUWxeIr9FeA 或是")
        print("UC-hM6YJuNYVAmUWxeIr9FeA\n")
        id = input("請輸入頻道網址或ID：")
        if  'youtube' in id:
            id = id.split('/')[-1]
        elif id == "":
            print("\n請輸入頻道id\n")
            continue
        channel = searchlive.get_channel_detail(id)
        if channel.get('name', 0) != 0:
            print("您要記錄的頻道為"+channel.get('name', 0))
            return id
        else:
            print("\n無法找到頻道，可能是網址格式錯誤或不支援的頻道\n")
            time.sleep(1)

def set_keyword():
    while True:
        keyword = input("請輸入要記錄的影片或直播關鍵字(不分大小寫)：").lower()
        if keyword == "":
            return None
        return keyword


def listen_channel(channel_id,keyword = None):
    search = 0
    archived_live_id = []
    print("檢查頻道是否有新直播中...")
    search = 1
    live = searchlive.get_live(channel_id,"1")
    if live != 0:
        live_id = live["id"]
        live_title = live["title"].lower()
        archived = 0
        if keyword == None or keyword in live_title:
            if live_id in archived_live_id:
                archived = 1
            if archived == 0:
                archived_live_id.append(live_id)
                t = str(int(time.time()))
                print("download"+live_title)
                locals()['dlthread'+live_id] = Thread(target = download.download,args=(live_id,))
                locals()['dlthread'+live_id].start()
    time.sleep(1)
    while True:
        now_time = datetime.now().strftime('%M%S')
        if now_time == '5500' or now_time == '1000' or now_time == '2500' or now_time == '4000' and search == 0:
            search = 1
            live = searchlive.get_live(channel_id,"1")
            if live != 0:
                live_id = live["id"]
                live_title = live["title"].lower()
                archived = 0
                if keyword == None or keyword in live_title:
                    if live_id in archived_live_id:
                        archived = 1
                    if archived == 0:
                        archived_live_id.append(live_id)
                        t = str(int(time.time()))
                        print("download"+live_title)
                        locals()['dlthread'+live_id] = Thread(target = download.download,args=(live_id,))
                        locals()['dlthread'+live_id].start()
            time.sleep(1)
        else:
            search = 0
            time.sleep(1)


def main():
    print("vtuber紀錄小幫手 0.1.1-alpha3")
    print("該服務基於Holodex API與yt-dlp所開發，目前僅支援Holodex所收錄的vtuber與剪輯\n\n")
    config = configparser.ConfigParser()
    config.read('config.ini')
    APIKEY = config.get("holodex","x-apikey")
    if APIKEY == 'None':
        print("\n您尚未設定您的Holodex API金鑰，系統將協助您進行設定\n")
        time.sleep(1)
        init_set()
    while True:
        mode = set_mode()
        if mode == "1":
            live_id = set_live_id()
            download.download(live_id)
            print("下載完成，即將回到主選單...\n")
        elif mode == "2":
            channel_id = set_channel_id()
            listen_channel(channel_id)
        elif mode == "3":
            channel_id = set_channel_id()
            keyword = set_keyword()
            listen_channel(channel_id,keyword)
        elif mode == "set":
            init_set()
        elif mode == "exit":
            break


if __name__ == '__main__':
    main()
