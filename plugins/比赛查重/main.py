import difflib
import re
import time
import logging

from flask import Flask, render_template
from threading import Thread
from module.luogu import Luogu, Log


# 处理获取到的源代码
def handle_src(src: str):
    src = re.sub("cin(.*?);", "", src)
    src = re.sub("scanf(.*?);", "", src)
    src = re.sub("cout(.*?);", "", src)
    src = re.sub("printf(.*?);", "", src)
    src = re.sub("#include(.*?)\n", "", src)
    src = re.sub("//(.*?)\n", "", src)
    src = src.replace("\n", "")
    src = re.sub("/\*(.*?)\*/", "", src)
    src = src.replace(" ", "")
    src = src.replace("\t", "")
    return src


class LAC:
    def __init__(self, contest_id):
        self.contest_id = contest_id
        self.real_name = {}
        self.record_list = []
        self.solution = {}

    def get_record(self):
        while 1:
            if not len(self.record_list):
                time.sleep(2)
                continue
            id = self.record_list[0]['id']
            pid = self.record_list[0]['pid']
            try:
                src = Luogu.get_record_information(id)
            except:
                src = {'currentData': {'record': {'detail': {'compileResult': {'success': False}}}}}
            frequency = 1
            # 如果没有获取成功就重试，只重试 5 次
            while (not src['currentData']['record']['detail']['compileResult']['success']) and 'code' in src and src['code'] == 200 and frequency <= 5:
                time.sleep(1)
                try:
                    src = Luogu.get_record_information(id)
                except:
                    src = {'currentData': {'record': {'detail': {'compileResult': {'success': False}}}}}
            # 获取记录源代码
            try:
                source = handle_src(src['currentData']['record']['sourceCode'])
            except:
                Log.warning("记录 {} 无法获取源代码".format(id))
                self.record_list.pop(0)
                time.sleep(0.2)
                continue
            # 去除无用内容，减少内存占用
            src = dict(src['currentData']['record'])
            src['detail'].pop('judgeResult')
            src['detail'].pop('__CLASS_NAME')
            src['detail']['compileResult'].pop('__CLASS_NAME')
            # 初始化查重率
            src["checkingRate"] = 0.0
            # 逐一跟每个题解比较
            for j in self.solution[pid]:
                # 获取最大查重率
                src["checkingRate"] = max(difflib.SequenceMatcher(None, source, j).ratio(), src["checkingRate"])
            src["checkingRate"] = float('%.2f' % (src["checkingRate"]*100))
            # 判断用户是否已记录
            if src['user']['name'] not in result:
                result[src['user']['name']] = {
                    'real_name': "" if not config["get_team_username"] else self.real_name[
                        src['user']['name']], "problem_dict": {pid: src}}
            # 如果有当前用户的其他题目的记录，但本题目没有
            elif pid not in result[src['user']['name']]["problem_dict"]:
                result[src['user']['name']]["problem_dict"][pid] = src
            # 如果有本题以前的记录，但查重率没这个高
            elif result[src['user']['name']]["problem_dict"][pid]["checkingRate"] < src["checkingRate"]:
                result[src['user']['name']]["problem_dict"][pid] = src
            self.record_list.pop(0)
            time.sleep(0.2)

    def _start(self, problem):
        # 保存题解
        solution = []
        # 题解页面
        k = 1

        while 1:
            try:
                # 获取题解
                sum_ = Luogu.get_problem_solution(problem["pid"], k)['currentData']['solutions']['result']
            except:
                Log.error("比赛查重 | 题目 {} 无法获取题解，可能是503了".format(problem["pid"]))
                time.sleep(1)
                continue
            # 判断当前题解页面是否为空
            if not len(sum_):
                break
            # 从题解里获取源代码
            for i in sum_:
                for j in re.findall("```cpp(.*?)```", i['content'], re.S):
                    # 添加题解
                    solution.append(handle_src(j))
            k += 1
            time.sleep(1)
        self.solution[problem["pid"]] = solution

        # 完成的记录的最大ID
        end_record_id = 0
        sum_max_record_id = 0
        while 1:
            # 记录页面
            k = 1
            while k:
                # 获取记录
                try:
                    sum_ = Luogu.get_record_list(problem["pid"], k, contest_id=self.contest_id)['currentData']['records'][
                    'result']
                except:
                    f = 1
                    while f:
                        try:
                            time.sleep(1)
                            sum_ = Luogu.get_record_list(problem["pid"], k, contest_id=self.contest_id)['currentData'][
                                'records'][
                                'result']
                            f=0
                            continue
                        except:
                            pass

                # 判断当前记录页面是否为空
                if not len(sum_):
                    k = 0
                    continue
                k += 1
                # 遍历每个记录
                for i in sum_:
                    try:
                        # 获取记录ID
                        id = i['id']
                        # 判断当前记录ID是否小于以前记录
                        if id <= end_record_id:
                            # 小于就gui
                            k=0
                            continue
                        # 获取记录信息
                        self.record_list.append({"id": id, "pid": problem["pid"]})
                    except:
                        pass
                # 修改已完成最大记录ID

                sum_max_record_id = max(sum_max_record_id, sum_[0]['id'])
                time.sleep(1)
            end_record_id = max(end_record_id, sum_max_record_id)
            time.sleep(2)

    def start(self):
        # 获取团队内昵称
        if config["get_team_username"]:
            Log.info("比赛查重 | 开始获取团队内昵称")
            k = 1
            while 1:
                real_name = Luogu.get_team_real_name(
                    Luogu.get_contest_information(self.contest_id)['currentData']['contest']['host']['id'], k)
                if not len(real_name):
                    break
                self.real_name.update(real_name)
                k += 1
        # 获取比赛题目列表
        Log.info("比赛查重 | 开始获取比赛题目")
        for i in Luogu.get_contest_information(self.contest_id)['currentData']['contestProblems']:
            # 判断题目是否为团队或个人题目
            if i['problem']['type'] in ['T', 'U']:
                Log.warning("比赛查重 | 题目 {} 为 {}题目，无法获取题解，所以无法查重".format(i['problem']["pid"],
                                                                                            "团队" if i['problem'][
                                                                                                          'type'] == 'T' else "个人"))
                continue
            problem_list.append(i)
            # 开始查重
            Thread(target=self._start, args=(i['problem'],)).start()
            Log.info("比赛查重 | 题目 {} 开始查重".format(i['problem']['pid']))
            # 慢点搞，避免503
            time.sleep(2)
        Thread(target=self.get_record).start()


class Web:
    def __init__(self, template_folder):
        self.app = Flask(__name__, template_folder=template_folder)
        log = logging.getLogger('werkzeug')
        log.disabled = True
        @self.app.route('/')
        def main_page():
            return render_template("index.html", result=result, problem_list=problem_list)

    def run(self, host, port):
        self.app.run(host=host, port=port)


config = {}
Luogu = Luogu()
result = {}
problem_list = []
lac = LAC(-1)


# 基础库加载
def init():
    return Luogu


# 插件初始化
def init2():
    global config, app
    # 读取配置文件
    config = Luogu.read_config()
    # 开始网页
    web = Web("{}/templates".format(Luogu.plugin_path))
    Log.info("比赛查重 | 初始化Web服务")
    # 开始查重
    lac.contest_id = config["contest_id"]
    lac.start()
    Log.attention(
        "比赛查重 | 比赛查重已启动，点击链接查看：http://{host}:{port}/".format(host=config["host"], port=config["port"]))
    web.run(config["host"], config["port"])
