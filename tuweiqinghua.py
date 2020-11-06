import requests
#https://cp.xuthus.cc/
key = ''
tuwei_api = 'https://v1.alapi.cn/api/qinghua'
def getData(api_url):
    r = requests.get(api_url)
    r.encoding = r.apparent_encoding
    res = r.json()
    try:
        if res['code'] == 200:
            data = res['data']['content']
            return data
    except:
        pass

def main(*args):
    url = tuwei_api
    push_url = "https://push.xuthus.cc/group/" + key
    post_data = getData(url)
    requests.post(push_url, post_data.encode("utf-8"))
    print(post_data)

def main_handler(event, context):
    try:
       main()
    except Exception as e:
        raise e
    else:
        return 'success'


if __name__ == '__main__':
    # print(extension)
    print(main_handler({}, {}))