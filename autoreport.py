"""
sd

"""

# encoding=utf8
import sys
from ast import parse
# from ctypes import GetLastError
# import os
import argparse
import requests
# import urllib.request
# import json
import time
import datetime
import pytz
import re
from bs4 import BeautifulSoup
import  getpass


class Report(object):
    def __init__(self,stuid,password):
        self.url_login = "https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin"
        self.url_report = "https://weixine.ustc.edu.cn/2020/home"
        self.url_apply = "https://weixine.ustc.edu.cn/2020/apply/daliy/ipost"
        self.url_total = "https://weixine.ustc.edu.cn/2020/apply_total?t=d"
        self.reason = 3
        # reason=1 离校前往合肥市包河、庐阳、蜀山、瑶海区以外
        # reason=2 前往合肥市包河、庐阳、蜀山、瑶海区范围内校外
        # reason=3 前往东西南北中校区
        # reason=4 前往高新校区、先研院、国金院
        self.stuid = stuid
        self.password = password
        
        self.CAS_LT = ""
        self.cookie_login = ""
        self.token = ""
        self.PHPSESSID = ""
        self.loginsuccess = False
        self.LastTime = ""
        

    def Clock(self):
        session = self.login()
        headers_report = {
            'authority': 'weixine.ustc.edu.cn',
            'origin': 'http://weixine.ustc.edu.cn',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://passport.ustc.edu.cn/',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'PHPSESSID=' + session.cookies.get("PHPSESSID") + ";XSRF-TOKEN=" + session.cookies.get("XSRF-TOKEN") + ";laravel_session="+session.cookies.get("laravel_session"),
            'referer': 'https://weixine.ustc.edu.cn/2020/home',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1'
        }

        data = session.get(self.url_report).text
        soup = BeautifulSoup(data, 'html.parser')

        # print(soup)
        # pattern = re.compile("2022-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
        # # last_time_report = soup.find("span", {"上次上报时间"})
        # last_time_report = soup.find("span", {"style": "position: relative; top: 5px; color: #666;"}).text
        # print(last_time_report)
        # self.GetLastTime()

        # body_condition = soup.find("select",id="body-condition")
        # body_condition_choose = body_condition.find_all("option",selected = True)[0]["value"]
        # print(body_condition_choose)

        now_status = soup.find("select",id="body-status")
        now_status_choose = now_status.find_all("option",selected = True)[0]["value"]
        if now_status_choose == "2":
            now_status_choose = "1"
        # print(now_status_choose)
        text_danger = soup.find("input",{"name":"jinji_lxr"})["value"]
        # print(text_danger)
        text_danger_relation = soup.find("input",{"name":"jinji_guanxi"})["value"]
        # print(text_danger_relation )
        text_danger_mobile = soup.find("input",{"name":"jiji_mobile"})["value"]
        # print(text_danger_mobile)
        dorm_building = soup.find("input",{"name":"dorm_building"})["value"]
        dorm = soup.find("input",{"name":"dorm"})["value"]

        data_report = {
            "juzhudi": "西校区",
            "dorm_building": dorm_building,
	        "dorm": dorm,
	        "body_condition": "1",
	        "body_condition_detail": "",
	        "now_status": "1",
	        "now_status_detail": "",
	        "has_fever": "0",
	        "last_touch_sars": "0",
	        "last_touch_sars_date": "",
	        "last_touch_sars_detail": "",
	        "is_danger": "0",
	        "is_goto_danger": 0,
	        "jinji_lxr": text_danger,
	        "jinji_guanxi": text_danger_relation,
	        "jiji_mobile": text_danger_mobile,
            "other_detail": "",
	        "_token": self.token
        }
        r = session.post("https://weixine.ustc.edu.cn/2020/daliy_report", data=data_report, headers=headers_report)
        # print(r.text)
        if (len(r.text)>1000):
            print("Report Success!")
        else:
            print("Report Failed!")

        data = session.get(self.url_report).text
        soup = BeautifulSoup(data, 'html.parser')
        # pattern = re.compile("2022-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
        # # last_time_report = soup.find("span", {"上次上报时间"})
        # last_time_report = soup.find("span", {"style": "position: relative; top: 5px; color: #666;"}).text
        # print(last_time_report)
        # self.GetLastTime()
    
    def Report(self):
        # daily report to other school
        reason = self.reason
        session = self.login()

        timenow = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        current_year = int(datetime.datetime.now().strftime('%Y'))
        current_month = int(datetime.datetime.now().strftime('%m'))
        current_day = int(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%d'))
        end_date = datetime.datetime(current_year, current_month, current_day, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')

        data_apply = {
    '_token': self.token,
    'start_date': timenow,
    'end_date': end_date,
    'return_college[]': '东校区',
    'return_college[]': '西校区',
    'return_college[]': '南校区',
    'return_college[]': '北校区',
    'return_college[]': '中校区',
    'reason': "上课,实验室",
    "t": str(reason)
    }

        headers_apply = {
    'authority': 'weixine.ustc.edu.cn',
    'origin': 'http://weixine.ustc.edu.cn',
    'upgrade-insecure-requests': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'PHPSESSID=' + session.cookies.get("PHPSESSID") + ";XSRF-TOKEN=" + session.cookies.get("XSRF-TOKEN") + ";laravel_session="+session.cookies.get("laravel_session"),
    'referer': 'https://weixine.ustc.edu.cn/2020/stayinout_apply?t='+str(reason),
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1'
    }
        data = session.post(self.url_apply,data =data_apply,headers=headers_apply).text
        data = data.encode('ascii','ignore').decode('utf-8','ignore')
        soup_apply = BeautifulSoup(data, 'html.parser')
        # print(soup_apply)
        res = soup_apply.prettify()
        if (len(res)>1000):
            print("Report Success!")
        else:
            print("Report failed!")


    def GetLastTime(self):
        session = self.login()
        data = session.get(self.url_total).text
        data = data.encode('ascii','ignore').decode('utf-8','ignore')
        soup_total = BeautifulSoup(data, 'html.parser')

        lasttime = soup_total.tbody.tr.td.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element

        # data = session.get(self.url_total).text
        # soup = BeautifulSoup(data, 'html.parser')
        
        # pattern = re.compile("2022-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
        # # last_time_report = soup.find("span", {"上次上报时间"})
        # last_time_report = soup.find("span", {"style": "position: relative; top: 5px; color: #666;"}).text
        # lasttime = last_time_report.strip('*上次上报时间：').strip('，请每日按时打卡')
        
        self.LastTime = lasttime
        print("上次上报时间:",lasttime,'\n脚本每日按时打卡!\n')
        return(lasttime)


    def login(self): 
        html_login = requests.get(self.url_login)
        html_login.encoding = 'utf-8'
        soup_login = BeautifulSoup(str(html_login.text), 'html.parser')
        print(soup_login.title.text)
        self.CAS_LT = soup_login.find('input',id="CAS_LT")['value'] # get CAS_LT
        # print(self.CAS_LT)
        # print(html_login.cookies)
        self.cookie_login = 'lang=zh; JSESSIONID='+html_login.cookies['JSESSIONID']
        # print(self.cookie_login) 

        data_login = {
        'CAS_LT': self.CAS_LT,
        'model': 'uplogin.jsp',
        'service': 'https://weixine.ustc.edu.cn/2020/caslogin',
        'username': self.stuid,
        'password': str(self.password),
        }

        headers_login = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    'Cookie': self.cookie_login,
    # 'Host': 'passport.ustc.edu.cn',
    # 'Referer': 'https://weixine.ustc.edu.cn/',
    # 'Sec-Fetch-Dest': 'document',
    # 'Sec-Fetch-Mode': 'navigate',
    # 'Sec-Fetch-Site': 'same-site',
    # 'Sec-Fetch-User': '1',
    # 'Sec-GPC': '1',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Mobile Safari/537.36'
    }
        session = requests.Session()
        response_report = session.post(self.url_login,headers=headers_login, data=data_login)

        getform = session.get("https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin")

        data = getform.text
        data = data.encode('ascii','ignore').decode('utf-8','ignore')
        soup = BeautifulSoup(data, 'html.parser')
        self.token = soup.find("input", {"name": "_token"})['value']  ## 
        # response_report = requests.post(url_login,headers=headers_login, data=data_login)
        if response_report.url != self.url_report:
            print("Login Failed! Retry...")
            self.loginsuccess = False
        else:
            print("Login Successful!")
            self.loginsuccess = True

        cookies_report = session.cookies
        self.PHPSESSID = cookies_report['PHPSESSID']
        return(session)

    def GetNowTime(self):
        timenow = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
        return(timenow)


print("\n")
print("+------------------------------------------------------------------------+")
print("|                             自动打卡报备脚本                             |")
print("+------------------------------------------------------------------------+")

if __name__ == "__main__":
    everyhours = 5 # hours 每多少小时进行打卡
    waittime = 10 # seconds 等待多长时间

    parser = argparse.ArgumentParser()
    parser.description = 'USTC Health Auto Report Script.'
    parser.add_argument('-us','--username', help='Your Student ID', type=str, default="None")
    parser.add_argument('-p','--password', help='Your password', type=str, default="None")
    args = parser.parse_args()
    if(len(args.username)!=0 or len(args.password) !=0):
        print("Begin login")
        user = args.username
        password = args.password
        autorepoter = Report(stuid=args.username,password=args.password)
    else:
        print("Please Input Information:")
        user =  input('Input the Student ID:' )
        password  =  getpass.getpass( 'Input the Password:' )
        autorepoter = Report(stuid=user,password=password)

    # 打卡一次,报备一次
    autorepoter.Clock()
    autorepoter.Report()

    lastime = autorepoter.GetLastTime()


    while 1:
        try:
            timenow = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
            delta= datetime.datetime.strptime(timenow,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(lastime,'%Y-%m-%d %H:%M:%S')
            # if delta.seconds>20:
            if (delta.seconds//3600)>everyhours:
                autorepoter.Clock()
                autorepoter.Report()
                lastime = autorepoter.GetLastTime()
            else:
                time_hour = delta.seconds//3600
                time_min = (delta.seconds-time_hour*3600)//60
                time_second = delta.seconds-time_hour*3600-time_min*60
                print("User:",user,"当前时间:",timenow,"上次报备时间为:",time_hour,"hours",time_min,"min",time_second,"s 以前")
                time.sleep(waittime)
        except Exception:
            print("\033[1;31;43mLogin Failed!\033[0m")
        finally:
            time.sleep(1)

  