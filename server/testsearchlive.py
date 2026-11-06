import time
import datetime
import searchlive

while True:
    now_time = datetime.datetime.now().strftime('%H%M%S')
    if now_time[2:] == '5500':
        break
    time.sleep(0.3)

while True:
    now_time = datetime.datetime.now().strftime('%H%M%S')
    print(now_time)
    print(searchlive.get_live_status('HB9hQu0LJP4'))
    if searchlive.get_live_status('HB9hQu0LJP4') == "live":
        break
    time.sleep(60)
