
import requests
# qq推送 申请参考https://cp.xuthus.cc/
key = ''
def main():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'  # API地址，必须配合城市代码使用
        city_code = '101070201'  # 进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()  # 将数据以json形式返回，这个d就是返回的json数据
        print(d['status'])
        if (d['status'] == 200):  # 当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"]  # 省
            city = d["cityInfo"]["city"]  # 市
            update_time = d["time"]  # 更新时间
            date = d["data"]["forecast"][0]["ymd"]  # 日期
            week = d["data"]["forecast"][0]["week"]  # 星期
            weather_type = d["data"]["forecast"][0]["type"]  # 天气
            wendu_high = d["data"]["forecast"][0]["high"]  # 最高温度
            wendu_low = d["data"]["forecast"][0]["low"]  # 最低温度
            shidu = d["data"]["shidu"]  # 湿度
            pm25 = str(d["data"]["pm25"])  # PM2.5
            pm10 = str(d["data"]["pm10"])  # PM10
            quality = d["data"]["quality"]  # 天气质量
            fx = d["data"]["forecast"][0]["fx"]  # 风向
            fl = d["data"]["forecast"][0]["fl"]  # 风力
            ganmao = d["data"]["ganmao"]  # 感冒指数
            tips = d["data"]["forecast"][0]["notice"]  # 温馨提示
            cpurl = "https://push.xuthus.cc/group/" + key # 推送到QQ群
            # cpurl = '[/font][/size][size=4][font=宋体][size=4][font=宋体]请求地址[/font][/size]/send/'+spkey   #推送到个人QQ
            # 天气提示内容
            tdwt ="-----------------------------------------" + "\n【今日份天气】\n城市： " + parent + city + \
                   "\n日期： " + date + "\n星期:  " + week + "\n天气:  " + weather_type + "\n温度:  " + wendu_high + " / " + wendu_low + "\n湿度:  " + \
                   shidu + "\nPM25:  " + pm25 + "\nPM10:  " + pm10 + "\n空气质量:  " + quality + \
                   "\n风力风向:  " + fx + fl + "\n感冒指数:  " + ganmao + "\n温馨提示：  " + tips + "\n更新时间:  " + update_time
            print(tdwt)
            requests.post(cpurl, tdwt.encode('utf-8'))  # 把天气数据转换成UTF-8格式，不然要报错。
    except:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        print(error)

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