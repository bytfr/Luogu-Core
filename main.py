import os
import threading
import time
import colorama
import json
import requests


headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                         "CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/115.0.0.0"}
config = {}


class Log:
    @staticmethod
    def info(*args):
        msg = ""
        for i in args:
            msg += i + " "
        print(colorama.Fore.WHITE+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"|  INFO   |", msg)
        colorama.init()

    @staticmethod
    def attention(*args):
        msg = ""
        for i in args:
            msg += i + " "
        print(colorama.Fore.CYAN + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"|ATTENTION|", msg)
        colorama.init()

    def warning(*args):
        msg = ""
        for i in args:
            msg += str(i) + " "
        print(colorama.Fore.YELLOW+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"| WARNING |", msg)
        colorama.init()

    def error(*args):
        msg = ""
        for i in args:
            msg += str(i) + " "
        print(colorama.Fore.RED + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "|  ERROR  |", msg)
        colorama.init()

class Plugins:
    def __init__(self, path: str = "./plugins"):
        self.path = path
        self.plugin_list = []
        self.event_list = {"get_message": []}

    def load(self):
        for i in os.listdir(self.path):
            try:
                plugin_sum = __import__("plugins."+i+".main", fromlist=["main"])
                information = plugin_sum.init()
                information.plugin_path = self.path+"/"+i
                information.cookie = config["cookie"]
                for j in information.event_list:
                    for k in information.event_list[j]:
                        self.event_list[j].append(k)
                try:
                    threading.Thread(target=plugin_sum.init2).start()
                except:
                    pass
                Log.info("插件", information.plugin_information["Plugin Name"], "加载成功")
            except Exception as e:
                Log.error("插件", i, "加载失败，原因:", e)
        Log.info("插件加载完成")

    def get_message(self):
        while 1:
            try:
                unread_message_count = requests.get("https://www.luogu.com.cn/chat?_contentOnly=1", headers=headers, cookies=config["cookie"]).json()["currentData"]["unreadMessageCount"]
                if len(list(unread_message_count)):
                    for i in unread_message_count:
                        sum_message = requests.get("https://www.luogu.com.cn/api/chat/record?user={}".format(i), headers=headers, cookies=config["cookie"]).json()["messages"]["result"]
                        for j in range(1, unread_message_count[i]+1):
                            for k in self.event_list["get_message"]:
                                threading.Thread(target=k, args=(sum_message[-(unread_message_count[i]+1-j)], )).start()
            except Exception as e:
                Log.warning("获取信息失败，稍后重试，失败原因:", e)
            time.sleep(1)



def get_config():
    global config
    with open("./config.json", "r") as f:
        config = json.loads(f.read())
        f.close()


plugin = Plugins()

if __name__ == '__main__':
    get_config()
    plugin.load()
    threading.Thread(target=plugin.get_message).start()
