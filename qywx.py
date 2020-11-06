import json
import requests
import redis
import time
import datetime


def connect_redis():
    REDIS_DB_URL = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 0
    }
    return redis.Redis(**REDIS_DB_URL)

#存到redis了获取access_token企业微信有次数限制。
def get_token():
    conn = connect_redis()
    token_tmpl = conn.get('access_token')
    if not token_tmpl:
        # 具体参照官方文档 https://work.weixin.qq.com/api/doc/90000/90135/91039
        # 我有管理员权限所以走的是官方的接口。如果没有权限的话，自己得抓包了。
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET"
        result = requests.get(url).json()
        token = result.get('access_token')  # 获取token
        expires_in_seconds = int(result.get('expires_in') * 0.9)  # 获取token的过期时间
        conn.set(
            name='access_token',  # redis key
            value=token,
            ex=expires_in_seconds  # 第三个参数表示Redis过期时间
        )
        # 存到Redis
    else:
        token = token_tmpl.decode("utf8")  # 解码

    return token


def get_template_detail():
    # 具体参看官方文档
    access_token = get_token()
    url = "https://qyapi.weixin.qq.com/cgi-bin/oa/gettemplatedetail?access_token=" + access_token
    param = {
        "template_id": "Bs7yoTh2ADimTHU3BmutqvmSFJpzKp1Qx7FnRKfkt"
    }
    param = (bytes(json.dumps(param), 'utf-8'))
    result = requests.post(url, data=param).json()
    print(result)


def tijiao():
    access_token = get_token()
    url = "https://qyapi.weixin.qq.com/cgi-bin/oa/applyevent?access_token=" + access_token
    # 请假理由，每天都是不同的，7天。
    reason = ["眼镜腿断了出去修眼镜", "去牙科门诊检查智齿,看一看能不能拔",
              "肚子不舒服去医院看一下", "手机屏碎了修手机",
              "外出去药店买药", "眼镜度数不够,看不清了,配一下眼镜",
              "电脑坏了,需要去苹果店修电脑"]
    today = datetime.date.today()
    # 今天请明天的假
    tomorrow = today + datetime.timedelta(days=1)
    day_week = tomorrow.weekday()
    timestamp = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
    param = {
        "creator_userid": "wang",
        "template_id": "Bs7yoTh2ADimTHU3BmutqvmSFJpzKp1Qx7FnRKfkt",
        "use_template_approver": 1,
        "approver": [
            {
                "attr": 1,
                "userid": ["wang"]
            }
        ],
        "notifyer": ["zhang"],
        "notify_type": 1,
        "apply_data": {
            "contents": [
                {
                    "control": "Selector",
                    "id": "Selector-1601027796295",
                    "value": {
                        "selector": {
                            "type": "single",
                            "options": [
                                {
                                    "key": "option-1601027796295",
                                }
                            ]
                        }
                    }
                },
                {
                    "control": "Date",
                    "id": "Date-1601027970855",
                    "value": {
                        "date": {
                            "type": "day",
                            "s_timestamp": str(timestamp)
                        }
                    }
                },
                {
                    "control": "Textarea",
                    "id": "Textarea-1601027836214",
                    "value": {
                        "text": reason[day_week]
                    }
                },
                {
                    "control": "Selector",
                    "id": "Selector-1601028065972",
                    "value": {
                        "selector": {
                            "type": "single",
                            "options": [
                                {
                                    "key": "option-1601028065972",
                                }
                            ]
                        }
                    }
                }
            ]
        },
        "summary_list": [
            {
                "summary_info": [{
                    "text": "摘要第1行",
                    "lang": "zh_CN"
                }]
            },
            {
                "summary_info": [{
                    "text": "摘要第2行",
                    "lang": "zh_CN"
                }]
            },
            {
                "summary_info": [{
                    "text": "摘要第3行",
                    "lang": "zh_CN"
                }]
            }
        ]
    }

    param = (bytes(json.dumps(param), 'utf-8'))
    result = requests.post(url, data=param).json()
    if result.get("errcode")==0:
        sendMessage()
# 调用http://sc.ftqq.com/3.version微信消息接口
def sendMessage():
    sckey=""
    url = 'https://sc.ftqq.com/' + sckey + '.send'
    title="企业微信已经请假"
    response = requests.get(url, params={"text": title, "desp": " "})
    data = json.loads(response.text)
    if data['errno'] == 0:
        print('Server酱推送成功')
    else:
        print('Server酱推送失败,请检查sckey是否正确')

# 用的腾讯云函数，方便云函数启动。
def main_handler(event, context):
    try:
      tijiao()
    except Exception as e:
        raise e
    else:
        return 'success'

if __name__ == '__main__':
    # print(extension)
    print(main_handler({}, {}))
