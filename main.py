from datetime import datetime, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os

today = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

city = os.environ['CITY']
start_date = os.environ['START_DATE']
app_id = os.environ['APP_ID']
app_secret = os.environ['APP_SECRET']
user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])


def get_count():
    delta = (datetime.now() + timedelta(hours=8)) - datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    return delta.days

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature, low, high = get_weather()
data = {"day": {"value": today}, "temperature": {"value": temperature}, "love_day": {"value": get_count()},
        "weather": {"value": wea}, "city": {"value": city}, "max_temperature": {"value": high},
        "min_temperature": {"value": low}, "body_temperature": {"value": temperature}}
res = wm.send_template(user_id, template_id, data)
print(res)
