# coding=utf-8
import discord
import asyncio
import os
import time
import datetime
import searchlive
import download
from threading import Thread

class SearchThread(Thread):

    def __init__(self, channel_id, max_upcoming_hours ="8"):
        Thread.__init__(self)
        self.channel_id = channel_id
        self.max_upcoming_hours = max_upcoming_hours

    def run(self):
        self.result = searchlive.get_live(self.channel_id,self.max_upcoming_hours)

    def get_result(self):
        return self.result


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.search = 0
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('目前登入身份：', self.user)
        print('------')

    async def on_message(self,message):
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.user:
            return
        #如果包含 ping，機器人回傳 pong
        if message.content == '$ping':
            await message.channel.send('pong')
        elif message.content == '$test':
            channel = self.get_channel(775684553976053780)
            await channel.send('test')
        elif message.content == '$time':
            await message.channel.send('<t:'+str(int(time.time()))+'>')
        elif message.content == '$hololive' or message.content == '$holo':
            self.search = 1
        elif '$download' in message.content or '$dl' in message.content:
            print(message.content)
            url = message.content.split(' ')[1]
            if 'youtu.be' in url:
                url = url.split('/')[-1]
            elif 'youtube' in url:
                url = url.split('v=')[-1]
            t = str(int(time.time()))
            locals()['dlthread'+t] = Thread(target = download.download,args=(url,))
            locals()['dlthread'+t].start()
            await message.channel.send('ready to download '+url+"\nfile will be save")
            #dlthread.join()

    async def my_background_task(self):
        await self.wait_until_ready()
        self.counter = 0
        self.file = "hololive_channels_id.txt"
        channel = self.get_channel(933756540178030592) # channel ID goes here
        while not self.is_closed():
            now_time = datetime.datetime.now().strftime('%H%M%S')
            if now_time == '000000' or now_time == '080000' or now_time == '160000' or self.search == 1 and self.counter == 0:
                self.search = 0
                print("search",self.search)
                f = open(self.file, 'r', encoding='utf-8')
                livelist=[]
                threads = []
                i=0
                for line in f.readlines():
                    line = line.strip('\n')
                    print (line)
                    threads.append(SearchThread(line))
                    threads[i].start()
                    i += 1
                    #live = searchlive.get_live(line)
                f.close()
                for count in range(i):
                    threads[count].join()
                for count in range(i):
                    if threads[count].get_result() != 0:
                        livelist.append(threads[count].get_result())
                    else:
                        pass

                '''live_id = live["id"]
                live_time = str(int(datetime.datetime.strptime(live["available_at"],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()))
                live_title = live["title"]
                channel_name = live["channel"]["name"]
                print(live_time)
                await channel.send('at <t:'+live_time+'>\n'+channel_name+'\n'+live_title+'\nhttps://youtu.be/'+live_id)'''

                livelist.sort(key = lambda live: int(datetime.datetime.strptime(live["available_at"],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()))
                print(livelist)
                for live in livelist:
                    live_id = live["id"]
                    live_time = str(int(datetime.datetime.strptime(live["available_at"],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()))
                    live_title = live["title"]
                    channel_name = live["channel"]["name"]
                    embed = discord.Embed(title=live_title, url='https://youtu.be/'+live_id, color=0xff0000)
                    embed.set_author(name=channel_name)
                    embed.add_field(name="排定直播時間", value='<t:'+live_time+'>(<t:'+live_time+':R>)', inline=False)
                    live_photo = 'https://img.youtube.com/vi/'+live_id+'/maxresdefault.jpg'
                    embed.set_image(url=live_photo)
                    await channel.send(embed=embed)
                    #await channel.send('<t:'+live_time+'>(<t:'+live_time+':R>)\nhttps://youtu.be/'+live_id)
                self.counter = 1
                await asyncio.sleep(1)

            elif now_time[2:] == '0000' or now_time[2:] == '1500' or now_time[2:] == '3000' or now_time[2:] == '4500' and self.counter == 0:
                live = searchlive.get_live("UC3n5uGu18FoCy23ggWWp8tA","1")
                if live != 0:
                    live_id = live["id"]
                    live_title = live["title"].lower()
                    archived = 0
                    if "sing" in live_title or "karaoke" in live_title or "unarchived" in live_title:
                        archived_id_file = "archived_id_file.txt"
                        f = open(archived_id_file, 'r+', encoding='utf-8')
                        for line in f.readlines():
                            print(line)
                            if live_id in line:
                                archived = 1
                                break
                        if archived == 0:
                            f.write(live_id+"\n")
                            t = str(int(time.time()))
                            print("download"+live_title)
                            locals()['dlthread'+t] = Thread(target = download.download,args=(live_id,))
                            locals()['dlthread'+t].start()
                        f.close()
                self.counter = 1
                await asyncio.sleep(1)

            else:
                self.counter = 0
                await asyncio.sleep(1)
                pass


client = MyClient()
client.run(os.environ["DISCORD_TOKEN"])
