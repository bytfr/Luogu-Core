# Luogu Core 使用

## config.json

配置文件，以下是个样例

```json
{
  // pip 文件路径
  "pip_path": "C:\\Users\\26785\\PycharmProjects\\Luogu Core\\venv\\Scripts\\pip.exe",
  // 洛谷Cookie
  "cookie": {"__client_id": "不告诉你", "_uid": "728260"}
}
```

## 导入插件

直接把插件放到plugins文件夹就行

样例:

```file
main.py
config.json
configs/ (存放插件配置文件)
plugins/
	样例插件/
    	    main.py
            plugin_information.json
            config.json (插件配置，需要再添加)
            requirements.txt (插件需要的模块)
module/ (存放插件运行模块的地方)
	Luogu/ (Luogu接口)
		__init__.py
```



# Luogu Core 插件开发文档

## 插件模板

main.py

```python
# 导入基本模块
from module.luogu import Luogu, Log

# 初始化
Luogu = Luogu()
# 设置信息(非必要)
Luogu.plugin_information["Plugin Name"] = "Luogu Core Plugin"


# 初始化函数(class Luogu 不可用)
def init():
  # 返回class Luogu(必要)
  return Luogu


# 初始化函数2(class Luogu 可用 非必要函数)
def init2():
  Log.info(Luogu.get_contest_real_name(55775))


# 获取信息(需要时使用)
@Luogu.get_message
def get_msg(message: dict):
  Log.info(message)
```

plugin_information.json

```json
{
  "Luogu-Core Version": 1.0,
  "Program_entry": "main", // 程序入口，填入开始程序的文件名，不要有后缀名!!!
  "Plugin Name": "Luogu Core Plugin",
  "Author": "bytfr",
  "Version": "1.0.0",
  "Author URL": "https://www.grmine.cn",
  "Email": "grmine@qq.com"
}
```

requirements.txt

```text
pymongo
flask
```

config.json

```json
// 无统一格式，只要保证是json即可
```



## class Luogu 里的函数

### 关于题目

- get_problem_list()	获取题目列表

  - ```python
    参数:
    - page  # 页面，默认为1
    - type  # 题目类型 (CF为CodeForces  SP为SPOJ  AT为AtCoder  UVA为UVA) 非必须
    - tag   # 题目标签 传入一个list，每一个值代表一个标签，具体标签参数请在https://www.luogu.com.cn/problem/list自行查看 非必须
    - difficulty # 题目难度，入门为1，难度递增 非必须
    - keyword # 关键词搜索 非必须
    
    Return dict
    
    例子:
    Luogu.get_problem_list()
    Return: 因为太长，复制链接查看：https://www.luogu.com.cn/problem/list?_contentOnly=1
    ```

- get_user_created_problems()	获取用户创建的题目列表

  - ```python
    参数:
    - page # 页面，默认为1
    
    Return dict
    
    例子:
    Luogu.get_user_created_problems()
    Return:
    {
      "problems": {
        "result": [
          {
            "tags": [
              
            ],
            "wantsTranslation": false,
            "totalSubmit": 0,
            "totalAccepted": 0,
            "flag": 0,
            "pid": "U315876",
            "title": "彩虹",
            "difficulty": 0,
            "fullScore": 0,
            "type": "U"
          },
          {
            "tags": [
              10,
              314
            ],
            "wantsTranslation": false,
            "totalSubmit": 31,
            "totalAccepted": 16,
            "flag": 5,
            "pid": "U312976",
            "title": "A^B Problem",
            "difficulty": 3,
            "fullScore": 100,
            "type": "U"
          }
        ],
        "perPage": 20,
        "count": 2
      }
    }
    ```

- get_problem()	获取题目信息

  - ```python
    参数:
    - pid  # 题目ID 例:P1001
    - contest_id  # 比赛ID 非必须
    
    Return dict
    
    例子:
    Luogu.get_problem("P1001")
    Return: 因为太长，复制链接查看：https://www.luogu.com.cn/problem/P1001?_contentOnly=1
    ```

- get_problem_solution()	获取题解

  - ```python
    参数:
    - pid  # 题目ID 例:P1001
    - page # 页面，默认为1
    
    Return dict
    
    例子:
    Luogu.get_problem_solution("P1001")
    Return: 因为太长，复制链接查看：https://www.luogu.com.cn/problem/solution/P1001?_contentOnly=1
    ```

### 关于比赛

- get_content_list()	获取公开赛列表

  - ```python
    参数:
    - page # 页面，默认为1
    
    Return dict
    
    例子:
    Luogu.get_contest_list()
    Return: 因为太长，复制链接查看：https://www.luogu.com.cn/contest/list?_contentOnly=1
    ```

- get_contest_information()	获取比赛信息

  - ```python
    参数:
    - contest_id # 比赛ID
    
    Return dict
    
    例子:
    Luogu.get_contest_information(121700)
    Return:
    {
        "code": 200,
        "currentTemplate": "ContestShow",
        "currentData": {
            "contest": {
                "description": "**J 组通道：<https://www.luogu.com.cn/contest/121699>**\n\n## 简介\n\n针对 2019 年 CSP 非专业组第一轮（相当于原 NOIP 初赛）的题目改革，我们命制了一套第一轮的模拟试卷。**为了维护 CCF 的知识产权利益，本次比赛简称 SCP 第一轮。**\n\n本次模拟测试形式一致，但与洛谷以往提供的模拟赛不同的是，本次分成了 J 组和 S 组两套试卷，以进行更具针对性的检测。如果希望查缺补漏或者体验形式，千万不要错过。**本场比赛只影响比赛咕值，不影响比赛等级分。**\n\n## 比赛时间和形式\n\n**时间**：2023 年 8 月 14 日 14:30-16:30\n\n**题型**：\n\n- **单项选择**：15 题，四选一单选\n- **阅读程序**：阅读程序并理解其中细节。有 3-4 个判断题和 2-3 个单项选择。\n- **完善程序**：给定任务要求和被挖空的程序代码，每处空格需要从 4 个选项中选择正确的一项填入空缺的地方。\n\n**两个组别中会有部分试题相同。** 题目将在洛谷有题中公开，但是由于洛谷有题暂时不支持进行比赛，因此需要选手在主站报名对应的比赛，并且**使用程序输出答案**的形式提交程序，使用 OI 赛制。比赛结束后会公布结果进行排行。\n\n**讲评时间：** 08 月 14 日 18:30 ~ 21:00 （当天夜间）\n\n试卷讲评是 [2023 年 CSP 第一轮（初赛）课程](https://class.luogu.com.cn/course/yugu23acs) 的一部分，报名此课程可以参与直播讲评。本课程的其他课时也可以通过回看随时学习和复习。课程除了复习知识点外，提供了多次模拟练习和随堂测验用于查缺补漏。对于希望熟悉第一轮考点、提升第一轮能力的同学均可报名。\n\n![](https://ipic.luogu.com.cn/yugu23n/cs/banner.png)\n\n![](https://ipic.luogu.com.cn/yugu23n/cs/2.png)",
                "totalParticipants": 2070,
                "eloDone": false,
                "canEdit": false,
                "ruleType": 1,
                "visibilityType": 1,
                "invitationCodeType": 1,
                "rated": true,
                "eloThreshold": -1,
                "host": {
                    "id": 1000,
                    "name": "洛谷官方团队",
                    "isPremium": true
                },
                "problemCount": 0,
                "id": 121700,
                "name": "【LGR-(-21) 】SCP 2023 第一轮（初赛 S 组）模拟",
                "startTime": 1691994600,
                "endTime": 1692001800
            },
            "contestProblems": null,
            "isScoreboardFrozen": false,
            "accessLevel": 2,
            "joined": false,
            "userElo": null
        },
        "currentTitle": "【LGR-(-21) 】SCP 2023 第一轮（初赛 S 组）模拟 - 比赛详情",
        "currentTheme": {
            "id": 1,
            "header": {
                "imagePath": null,
                "color": [
                    [
                        35,
                        37,
                        38,
                        1
                    ],
                    [
                        65,
                        67,
                        69,
                        1
                    ]
                ],
                "blur": 0,
                "brightness": 0,
                "degree": 90,
                "repeat": 0,
                "position": [
                    50,
                    50
                ],
                "size": [
                    0,
                    0
                ],
                "type": 2,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig"
            },
            "sideNav": {
                "logoBackgroundColor": [
                    52,
                    152,
                    219,
                    1
                ],
                "color": [
                    52,
                    73,
                    94,
                    1
                ],
                "invertColor": false,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\SideNavConfig"
            },
            "footer": {
                "imagePath": null,
                "color": [
                    [
                        51,
                        51,
                        51,
                        1
                    ]
                ],
                "blur": 0,
                "brightness": 0,
                "degree": 0,
                "repeat": 0,
                "position": [
                    0,
                    0
                ],
                "size": [
                    0,
                    0
                ],
                "type": 2,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig"
            }
        },
        "currentTime": 1691716308,
        "currentUser": {
            "followingCount": 0,
            "followerCount": 0,
            "ranking": 183714,
            "eloValue": null,
            "blogAddress": null,
            "unreadMessageCount": 0,
            "unreadNoticeCount": 0,
            "uid": 1054280,
            "name": "grmine",
            "slogan": "",
            "badge": null,
            "isAdmin": false,
            "isBanned": false,
            "color": "Gray",
            "ccfLevel": 0,
            "background": "",
            "verified": false
        }
    }
    ```

- get_contest_scoreboard()	获取比赛排名

  - ```python
    参数:
    - contest_id  # 比赛ID
    - page  # 页面 默认为1
    
    Return dict
    
    例子:
    Luogu.get_contest_scoreboard(124808)
    Return:
    {
        "scoreboard": {
            "result": [
                {
                    "details": {
                        "P1001": {
                            "score": 100,
                            "runningTime": 353000
                        }
                    },
                    "user": {
                        "uid": 728260,
                        "name": "bytfr",
                        "slogan": "1+1=2",
                        "badge": null,
                        "isAdmin": false,
                        "isBanned": false,
                        "color": "Green",
                        "ccfLevel": 0,
                        "background": ""
                    },
                    "teamMember": {
                        "user": {
                            "uid": 728260,
                            "name": "bytfr",
                            "slogan": "1+1=2",
                            "badge": null,
                            "isAdmin": false,
                            "isBanned": false,
                            "color": "Green",
                            "ccfLevel": 0,
                            "background": ""
                        },
                        "type": 3,
                        "permission": 127,
                        "realName": ""
                    },
                    "score": 100,
                    "runningTime": 353000
                }
            ],
            "perPage": 50,
            "count": 1
        },
        "userScore": {
            "details": {
                "P1001": {
                    "score": 100,
                    "runningTime": 353000
                }
            },
            "user": {
                "uid": 728260,
                "name": "bytfr",
                "slogan": "1+1=2",
                "badge": null,
                "isAdmin": false,
                "isBanned": false,
                "color": "Green",
                "ccfLevel": 0,
                "background": ""
            },
            "teamMember": {
                "user": {
                    "uid": 728260,
                    "name": "bytfr",
                    "slogan": "1+1=2",
                    "badge": null,
                    "isAdmin": false,
                    "isBanned": false,
                    "color": "Green",
                    "ccfLevel": 0,
                    "background": ""
                },
                "type": 3,
                "permission": 127,
                "realName": ""
            },
            "score": 100,
            "runningTime": 353000
        },
        "userRank": 1,
        "firstBloodUID": {
            "P1001": 728260
        }
    }
    ```

    

### 关于"我的"

- get_my_information()	获取我的信息

  - ```python
    Return dict
    
    例子:
    Luogu.get_my_information()
    Return: 因为太长，复制链接查看：https://www.luogu.com.cn/user/728260?_contentOnly=1
    ```

- get_my_passed_problems()	获取我通过题目

  - ```python
    Return list
    
    例子:
    Luogu.get_my_passed_problems()
    Return:
    [
        {
            "pid": "B3614",
            "title": "【模板】栈",
            "difficulty": 2,
            "fullScore": 100,
            "type": "B"
        },
        {
            "pid": "B2001",
            "title": "入门测试题目",
            "difficulty": 1,
            "fullScore": 100,
            "type": "B"
        },
        {
            "pid": "B2002",
            "title": "Hello,World!",
            "difficulty": 1,
            "fullScore": 100,
            "type": "B"
        }
    ]
    ```
  
- get_my_teams()	获取我加入的团队

  - ```python
    Return list
    
    例子:
    Luogu.get_my_teams()
    Return:
    [
        {
            "team": {
                "id": 61684,
                "name": "乐子happy屋",
                "isPremium": true
            },
            "group": null,
            "user": {
                "uid": 728260,
                "name": "bytfr",
                "slogan": "1+1=2",
                "badge": null,
                "isAdmin": false,
                "isBanned": false,
                "color": "Green",
                "ccfLevel": 0,
                "background": ""
            },
            "type": 1,
            "permission": 2
        },
        {
            "team": {
                "id": 61862,
                "name": "Why you bully me",
                "isPremium": false
            },
            "group": null,
            "user": {
                "uid": 728260,
                "name": "bytfr",
                "slogan": "1+1=2",
                "badge": null,
                "isAdmin": false,
                "isBanned": false,
                "color": "Green",
                "ccfLevel": 0,
                "background": ""
            },
            "type": 3,
            "permission": 127
        }
    ]
    ```
  

### 关于信息

- get_message()	信息事件

  - ```python
    传入 dict
    
    例子:
    @Luogu.get_message
    def get_msg(message: dict):
        Log.Info(message)
    控制台输出:
    2023-08-10 17:41:15 |  INFO   | {'id': 17022105, 'sender': {'uid': 574822, 'name': 'CwinSpider', 'slogan': '严以律己，宽以待人', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Orange', 'ccfLevel': 0, 'background': 'https://cdn.luogu.com.cn/upload/image_hosting/cxqdrrxb.png'}, 'receiver': {'uid': 728260, 'name': 'bytfr', 'slogan': '1+1=2', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'background': ''}, 'time': 1691660476, 'status': 2, 'content': '.help'}
    ```

- send_message()	发送信息

  - ```python
    参数:
    - message # 消息信息
    - userID # 发送给的用户ID
    
    Return requests.post() # 其实没什么用(
    
    例子:
    Luogu.send_message("test", 728260)
    发送test给用户ID为728260的用户
    ```

### 关于读写插件配置文件

- Luogu.read_config()	读取插件配置文件

  - ```python
    参数:
    - file_name # 配置文件名
    
    Return dict or list
    
    例子:
    Luogu.read_config("config.json") #前提"/plugins/插件文件夹/config.json"文件存在，否则会报错
    Return:
    {"cookie": {"不告诉你"}}
    ```

- Luogu.save_config(config)	写入配置文件

  - ```python
    参数:
    - config # 配置
    - file_name # 配置文件名
    
    Return None
    
    例子:
    Luogu.save_config({"cookie": {"不告诉你"}}, "config.json")
    "/configs/插件文件夹/config.json" 内容:
    {"cookie": {"不告诉你"}}
    ```

### 关于团队

- get_my_teams()	获取我加入的团队

  - ```python
    # 其实 关于"我的" 那里也有，为了方便这里也列出来
    Return list
    
    例子:
    Luogu.get_my_passed_problems()
    Return:
    [
        {
            "team": {
                "id": 61684,
                "name": "乐子happy屋",
                "isPremium": true
            },
            "group": null,
            "user": {
                "uid": 728260,
                "name": "bytfr",
                "slogan": "1+1=2",
                "badge": null,
                "isAdmin": false,
                "isBanned": false,
                "color": "Green",
                "ccfLevel": 0,
                "background": ""
            },
            "type": 1,
            "permission": 2
        },
        {
            "team": {
                "id": 61862,
                "name": "Why you bully me",
                "isPremium": false
            },
            "group": null,
            "user": {
                "uid": 728260,
                "name": "bytfr",
                "slogan": "1+1=2",
                "badge": null,
                "isAdmin": false,
                "isBanned": false,
                "color": "Green",
                "ccfLevel": 0,
                "background": ""
            },
            "type": 3,
            "permission": 127
        }
    ]
    ```

- get_team_information()	获取团队信息

  - ```python
    参数:
    - team_id # 团队ID
    
    Return dict
    
    例子
    Luogu.get_team_information(61862)
    Return:
    样例太长，复制链接查看：https://www.luogu.com.cn/team/61862?_contentOnly=1
    ```

- get_team_real_name()	获取团队里每一个用户的团队名

  - ```python
    参数:
    - team_id  #团队ID
    - page  #第几页，默认为1
    - limit  #每一页多少个，默认为100
    
    Return dict
    
    例子:
    Luogu.get_team_real_name(61862)
    Return:
    {
        "bytfr": "样例名"
    }
    ```

- get_team_contest()	获取团队比赛

  - ```python
    参数:
    - team_id # 团队ID
    
    Return list
    
    例子:
    Luogu.get_team_contest(61862)
    Return:
    [
        {
            "ruleType": 4,
            "visibilityType": 3,
            "invitationCodeType": 1,
            "rated": false,
            "eloThreshold": null,
            "host": {
                "id": 61862,
                "name": "Why you bully me",
                "isPremium": false
            },
            "problemCount": 1,
            "id": 124808,
            "name": "测试比赛",
            "startTime": 1691662279,
            "endTime": 1691662320
        }
    ]
    ```

### 关于记录

- get_record_list()	获取题目提交记录

  - ```python
    参数:
    - problem_id  # 题目id
    - page  # 页面，默认为1
    - user_id  # 默认为None，表示获取当前题目当前页面所有记录
    - contest_id  # 比赛ID，默认None表示不从比赛获取记录
    
    Return dict
    
    例子:
    Luogu.get_record_list("P1000", 1, 728260)
    Return:
    {
        "code": 200,
        "currentTemplate": "RecordList",
        "currentData": {
            "records": {
                "result": [
                    {
                        "time": 3,
                        "memory": 684,
                        "problem": {
                            "pid": "P1000",
                            "title": "超级玛丽游戏",
                            "difficulty": 1,
                            "fullScore": 100,
                            "type": "P"
                        },
                        "contest": null,
                        "sourceCodeLength": 1717,
                        "submitTime": 1676777933,
                        "language": 3,
                        "user": {
                            "uid": 728260,
                            "name": "bytfr",
                            "slogan": "1+1=2",
                            "badge": null,
                            "isAdmin": false,
                            "isBanned": false,
                            "color": "Green",
                            "ccfLevel": 0,
                            "background": ""
                        },
                        "id": 102495958,
                        "status": 12,
                        "enableO2": true,
                        "score": 100
                    }
                ],
                "perPage": 20,
                "count": 1
            }
        },
        "currentTitle": "记录列表",
        "currentTheme": {
            "id": 1,
            "header": {
                "imagePath": null,
                "color": [
                    [
                        35,
                        37,
                        38,
                        1
                    ],
                    [
                        65,
                        67,
                        69,
                        1
                    ]
                ],
                "blur": 0,
                "brightness": 0,
                "degree": 90,
                "repeat": 0,
                "position": [
                    50,
                    50
                ],
                "size": [
                    0,
                    0
                ],
                "type": 2,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig"
            },
            "sideNav": {
                "logoBackgroundColor": [
                    52,
                    152,
                    219,
                    1
                ],
                "color": [
                    52,
                    73,
                    94,
                    1
                ],
                "invertColor": false,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\SideNavConfig"
            },
            "footer": {
                "imagePath": null,
                "color": [
                    [
                        51,
                        51,
                        51,
                        1
                    ]
                ],
                "blur": 0,
                "brightness": 0,
                "degree": 0,
                "repeat": 0,
                "position": [
                    0,
                    0
                ],
                "size": [
                    0,
                    0
                ],
                "type": 2,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig"
            }
        },
        "currentTime": 1691663216,
        "currentUser": {
            "followingCount": 0,
            "followerCount": 6,
            "ranking": 11559,
            "eloValue": 171,
            "blogAddress": "https://www.luogu.com.cn/blog/grmine/",
            "unreadMessageCount": 0,
            "unreadNoticeCount": 0,
            "uid": 728260,
            "name": "bytfr",
            "slogan": "1+1=2",
            "badge": null,
            "isAdmin": false,
            "isBanned": false,
            "color": "Green",
            "ccfLevel": 0,
            "background": "",
            "verified": true
        }
    }
    ```

- get_record_information()	获取记录信息(关于获取记录代码，要看有没有权限获取)

  - ```python
    参数:
    - record_id #记录id
    
    Return dict
    
    例子:
    Luogu.get_record_information(102495958)
    Return:
    {
        "code": 200,
        "currentTemplate": "RecordShow",
        "currentData": {
            "record": {
                "detail": {
                    "compileResult": {
                        "success": true,
                        "message": null,
                        "opt2": false,
                        "__CLASS_NAME": "Luogu\\DataClass\\Record\\JudgeResult\\CompileResult"
                    },
                    "judgeResult": {
                        "subtasks": [
                            {
                                "id": 0,
                                "score": 100,
                                "status": 12,
                                "testCases": [
                                    {
                                        "id": 0,
                                        "status": 12,
                                        "time": 3,
                                        "memory": 684,
                                        "score": 100,
                                        "signal": 0,
                                        "exitCode": 0,
                                        "description": "ok accepted",
                                        "subtaskID": 0,
                                        "__CLASS_NAME": "Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult"
                                    }
                                ],
                                "judger": "",
                                "time": 3,
                                "memory": 684,
                                "__CLASS_NAME": "Luogu\\DataClass\\Record\\JudgeResult\\SubtaskJudgeResult"
                            }
                        ],
                        "finishedCaseCount": 1,
                        "status": 0,
                        "time": 0,
                        "memory": 0,
                        "score": 0,
                        "__CLASS_NAME": "Luogu\\DataClass\\Record\\JudgeResult\\JudgeResult"
                    },
                    "version": 400,
                    "__CLASS_NAME": "Luogu\\DataClass\\Record\\RecordDetail"
                },
                "sourceCode": "#include<iostream>\r\nusing namespace std;\r\n\r\nint main(){\r\n    cout << \"                ********\" << endl;\r\n    cout << \"               ************\" << endl;\r\n    cout << \"               ####....#.\" << endl;\r\n    cout << \"             #..###.....##....\" << endl;\r\n    cout << \"             ###.......######              ###            ###\" << endl;\r\n    cout << \"                ...........               #...#          #...#\" << endl;\r\n    cout << \"               ##*#######                 #.#.#          #.#.#\" << endl;\r\n    cout << \"            ####*******######             #.#.#          #.#.#\" << endl;\r\n    cout << \"           ...#***.****.*###....          #...#          #...#\" << endl;\r\n    cout << \"           ....**********##.....           ###            ###\" << endl;\r\n    cout << \"           ....****    *****....\" << endl;\r\n    cout << \"             ####        ####\" << endl;\r\n    cout << \"           ######        ######\" << endl;\r\n    cout << \"##############################################################\" << endl;\r\n    cout << \"#...#......#.##...#......#.##...#......#.##------------------#\" << endl;\r\n    cout << \"###########################################------------------#\" << endl;\r\n    cout << \"#..#....#....##..#....#....##..#....#....#####################\" << endl;\r\n    cout << \"##########################################    #----------#\" << endl;\r\n    cout << \"#.....#......##.....#......##.....#......#    #----------#\" << endl;\r\n    cout << \"##########################################    #----------#\" << endl;\r\n    cout << \"#.#..#....#..##.#..#....#..##.#..#....#..#    #----------#\" << endl;\r\n    cout << \"##########################################    ############\" << endl;\r\n}   ",
                "time": 3,
                "memory": 684,
                "problem": {
                    "pid": "P1000",
                    "title": "\u8d85\u7ea7\u739b\u4e3d\u6e38\u620f",
                    "difficulty": 1,
                    "fullScore": 100,
                    "type": "P"
                },
                "contest": null,
                "sourceCodeLength": 1717,
                "submitTime": 1676777933,
                "language": 3,
                "user": {
                    "uid": 728260,
                    "name": "bytfr",
                    "slogan": "1+1=2",
                    "badge": null,
                    "isAdmin": false,
                    "isBanned": false,
                    "color": "Green",
                    "ccfLevel": 0,
                    "background": ""
                },
                "id": 102495958,
                "status": 12,
                "enableO2": true,
                "score": 100
            },
            "testCaseGroup": [
                [
                    0
                ]
            ],
            "showStatus": true
        },
        "currentTitle": "R102495958",
        "currentTheme": {
            "id": 1,
            "header": {
                "imagePath": null,
                "color": [
                    [
                        35,
                        37,
                        38,
                        1
                    ],
                    [
                        65,
                        67,
                        69,
                        1
                    ]
                ],
                "blur": 0,
                "brightness": 0,
                "degree": 90,
                "repeat": 0,
                "position": [
                    50,
                    50
                ],
                "size": [
                    0,
                    0
                ],
                "type": 2,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig"
            },
            "sideNav": {
                "logoBackgroundColor": [
                    52,
                    152,
                    219,
                    1
                ],
                "color": [
                    52,
                    73,
                    94,
                    1
                ],
                "invertColor": false,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\SideNavConfig"
            },
            "footer": {
                "imagePath": null,
                "color": [
                    [
                        51,
                        51,
                        51,
                        1
                    ]
                ],
                "blur": 0,
                "brightness": 0,
                "degree": 0,
                "repeat": 0,
                "position": [
                    0,
                    0
                ],
                "size": [
                    0,
                    0
                ],
                "type": 2,
                "__CLASS_NAME": "Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig"
            }
        },
        "currentTime": 1691663612,
        "currentUser": {
            "followingCount": 0,
            "followerCount": 6,
            "ranking": 11559,
            "eloValue": 171,
            "blogAddress": "https://www.luogu.com.cn/blog/grmine/",
            "unreadMessageCount": 0,
            "unreadNoticeCount": 0,
            "uid": 728260,
            "name": "bytfr",
            "slogan": "1+1=2",
            "badge": null,
            "isAdmin": false,
            "isBanned": false,
            "color": "Green",
            "ccfLevel": 0,
            "background": "",
            "verified": true
        }
    }
    ```
    

## class Log 里的函数

**本类是日志类，建议使用本类输出控制台，格式更美观**

- info()	发送一个"信息"到控制台

  - ```python
    参数:
    - *args # 信息
    
    Return None
    
    例子:
    Log.info("Hello World!")
    控制台:
    2023-08-11 18:09:30 |  INFO   | Hello World!
    ```

- warning()	发送一个"警告"到控制台

  - ```python
    参数:
    - *args # 信息
    
    Return None
    
    例子:
    Log.warning("Warning")
    控制台:
    2023-08-11 18:10:51 | WARNING | Warning
    ```

- error()	发送一个"错误"到控制台

  - ```python
    参数:
    - *args # 信息
    
    Return None
    
    例子:
    Log.error("Error")
    控制台:
    2023-08-11 18:10:51 |  ERROR  | Error
    ```

- attention()	发送一个"注意"到控制台 

  - ```python
    参数:
    - *args # 信息
    
    Return None
    
    例子:
    Log.attention("Attention")
    控制台:
    2023-08-11 18:10:51 |ATTENTION| Attention
    ```

    

