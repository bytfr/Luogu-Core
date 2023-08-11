import threading

from luogu import Luogu, Log

Luogu = Luogu()
help_str = """------- 指令列表 -------

{}
------- 指令列表 -------
"""


def init():
    return Luogu


def command_help(msg, command):
    sum_str = ""
    try:
        for i in command_list:
            sum_str += " -      {}  {}\n".format(i, command_list[i]["introduce"])
        Luogu.send_message(help_str.format(sum_str), msg["sender"]["uid"])
    except:
        Luogu.send_message("表达式错误", msg["sender"]["uid"])


def jsq(msg, command):
    math_str = ""
    for i in range(1, len(command)):
        math_str += command[i]
    Luogu.send_message(str(eval(math_str)), msg["sender"]["uid"])


@Luogu.get_message
def get_msg(message):
    Log.attention(message['sender']['name'] + ':', message['content'])
    if message['content'][0] == ".":
        command = message['content'].replace("\n", " ").split(" ")
        if command[0] in command_list:
            threading.Thread(target=command_list[command[0]]["function"], args=(message, command)).start()
        else:
            Luogu.send_message("未知指令，输入 .help 获取指令帮助", message["sender"]["uid"])


command_list = {
    ".help": {"introduce": "获取指令列表", "function": command_help},
    ".计算器": {"introduce": "简单数学计算，用法: .计算器 <数学表达式>", "function": jsq}
}
