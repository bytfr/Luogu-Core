import re
import json
import time
import requests
import colorama

headers = {"User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                         "CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/115.0.0.0"}


class Luogu:
    def __init__(self):
        self.plugin_information = {}
        self.cookie = {}
        self.event_list = {"get_message": []}
        self.plugin_path = ""

    def get_csrf_token(self, url):
        return re.findall('<meta name="csrf-token" content="(.*?)">',
                          requests.get(url, headers=headers, cookies=self.cookie).text)[0]

    def get_my_information(self):
        return requests.get("https://www.luogu.com.cn/user/{}?_contentOnly=1".format(self.cookie["_uid"]),
                            headers=headers, cookies=self.cookie).json()

    def get_my_passed_problems(self):
        return self.get_my_information()["currentData"]["passedProblems"]

    def get_my_teams(self):
        return self.get_my_information()["currentData"]["teams"]

    def get_message(self, function):
        self.event_list["get_message"].append(function)

    def send_message(self, message, user: int):
        sum_headers = headers
        sum_cookie = self.cookie
        sum_headers["X-Csrf-Token"] = self.get_csrf_token("https://www.luogu.com.cn/chat?uid={}".format(user))
        sum_headers["referer"] = "https://www.luogu.com.cn/chat?uid={}".format(user)
        sum_cookie["login_referer"] = "https://www.luogu.com.cn/chat?uid={}".format(user)
        u = requests.post("https://www.luogu.com.cn/api/chat/new", json={"user": int(user), "content": message},
                          headers=sum_headers, cookies=sum_cookie)
        return u

    def get_team_contest(self, team_id):
        contest_list = []
        k = 1
        while k:
            try:
                sum_contest_list = \
                requests.get("https://www.luogu.com.cn/api/team/contests/{}?page={}".format(team_id, k),
                             headers=headers, cookies=self.cookie).json()["contests"]["result"]
                if len(sum_contest_list):
                    for i in sum_contest_list:
                        contest_list.append(i)
                else:
                    break
                k += 1
            except:
                break
            time.sleep(0.1)
        return contest_list

    def read_config(self):
        with open(self.plugin_path + "/config.json", "r") as f:
            config = json.loads(f.read())
            f.close()
        return config

    def save_config(self, config: dict):
        with open(self.plugin_path + "/config.json", "w") as f:
            f.write(json.dumps(config))
            f.close()

    def get_record_list(self, problem_id: str, page: int = 1, user_id=None, contest_id: int = None):
        url = "https://www.luogu.com.cn/record/list?pid={}&page={}&_contentOnly=1".format(problem_id, page)
        if user_id is not None:
            url += "&user={}".format(user_id)
        if contest_id is not None:
            url += "&contestId={}".format(contest_id)
        r=requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_record_information(self, record_id):
        url = "https://www.luogu.com.cn/record/{}?_contentOnly=1".format(record_id)
        r=requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_team_information(self, team_id):
        r = requests.get("https://www.luogu.com.cn/team/{}?_contentOnly=1".format(team_id), headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_team_real_name(self, team_id, page=1, limit=100):
        url = "https://www.luogu.com.cn/api/team/members/{}?limit={}&orderBy=group.no&page={}".format(team_id, limit, page)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        real_name = {}
        try:
            for i in r.json()["members"]["result"]:
                real_name[i["user"]["name"]] = i["realName"]
        except:
            pass
        return real_name

    def get_problem_list(self, page=1, type=None, tag=None, difficulty=None, keyword=None):
        url = "https://www.luogu.com.cn/problem/list?_contentOnly=1&page={}".format(page)
        if tag is not None:
            tag_str = "&tag="
            for i in tag:
                tag_str += str(i)+","
            tag_str = tag_str[:-1]
            url += tag_str
        if difficulty is not None:
            url += "&difficulty={}".format(difficulty)
        if type is not None:
            url += "&type={}".format(type)
        if keyword is not None:
            url += "&keyword={}".format(keyword)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text()

    def get_user_created_problems(self, page=1):
        url = "https://www.luogu.com.cn/api/user/createdProblems?page={}".format(page)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_problem(self, pid, contest_id=None):
        url = "https://www.luogu.com/problem/{}?_contentOnly=1".format(pid)
        if contest_id is not None:
            url += "&contestId={}".format(contest_id)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_problem_solution(self, pid, page=1):
        url = "https://www.luogu.com.cn/problem/solution/{}?_contentOnly=1&page={}".format(pid, page)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_content_list(self, page=1):
        url = "https://www.luogu.com.cn/contest/list?_contentOnly=1&page={}".format(page)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_contest_information(self, contest_id):
        url = "https://www.luogu.com.cn/contest/{}?_contentOnly=1".format(contest_id)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

    def get_contest_scoreboard(self, contest_id, page=1):
        url = "https://www.luogu.com.cn/fe/api/contest/scoreboard/{}?page={}".format(contest_id, page)
        r = requests.get(url, headers=headers, cookies=self.cookie)
        try:
            return r.json()
        except:
            return r.text

class Log:
    @staticmethod
    def info(*args):
        msg = ""
        for i in args:
            msg += str(i) + " "
        print(colorama.Fore.WHITE + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "|  INFO   |", msg)
        colorama.init()

    @staticmethod
    def attention(*args):
        msg = ""
        for i in args:
            msg += str(i) + " "
        print(colorama.Fore.CYAN + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "|ATTENTION|", msg)
        colorama.init()

    def warning(*args):
        msg = ""
        for i in args:
            msg += str(i) + " "
        print(colorama.Fore.YELLOW + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "| WARNING |", msg)
        colorama.init()

    def error(*args):
        msg = ""
        for i in args:
            msg += str(i) + " "
        print(colorama.Fore.RED + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "|  ERROR  |", msg)
        colorama.init()
