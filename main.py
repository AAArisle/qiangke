import requests
import json
import re
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

import get_validate

find_token = re.compile('token":"(.*?)"')
find_msg = re.compile('msg":"(.*?)"')

def get_cookies(number,passwd):
    '''获取cookie'''
    url = 'https://jwxk.jnu.edu.cn/xsxkapp/sys/xsxkapp/student/register.do?number=%s'%number

    Options = ChromeOptions()
    # Options.add_argument('--headless')          # 浏览器无头模式，不显示，后台运行
    driver = webdriver.Chrome(options=Options,executable_path='chromedriver.exe')
    driver.get(url)

    time.sleep(5)

    # 给验证码参数赋值
    # try:
    #     validate_element = driver.find_element(by=By.CLASS_NAME, value="yidun_input")
    # except Exception as e:
    #     print("Try again")
    #     time.sleep(2)
    #     validate_element = driver.find_element(by=By.CLASS_NAME, value="yidun_input")
    # validate = get_validate.get_validate()
    # # validate = input()
    # driver.execute_script("arguments[0].value = '%s';"%validate, validate_element)
    # print("over")

    # 键入账号密码
    name_element = driver.find_element(by=By.ID, value="un")
    name_element.clear()
    name_element.send_keys(number)
    passwd_element = driver.find_element(by=By.ID, value="pd")
    passwd_element.clear()
    passwd_element.send_keys(passwd)
    button_element = driver.find_element(by=By.CLASS_NAME, value="login_box_landing_btn")
    button_element.click()
    try:
        fake_cookies = driver.get_cookies()
    except Exception as e:
        print(e)
        time.sleep(2)
        fake_cookies = driver.get_cookies()
    cookies = 'Secure;Secure;'
    for item in fake_cookies:
        temp = item['name'] + "=" + item['value'] + ";"
        cookies += temp
    driver.close()

    if cookies[-7:] == 'Secure;':
        print("获取cookie完毕：", cookies)
        return cookies
    else:
        print("获取cookie失败：", cookies)
        return None

def get_token(number, cookies):
    '''获取token'''
    url = 'https://jwxk.jnu.edu.cn/xsxkapp/sys/xsxkapp/student/register.do?number=%s'%number
    header = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control':'max-age=0',
        'cookie':cookies,
        'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'document',
        'sec-fetch-mode':'navigate',
        'sec-fetch-site':'none',
        'sec-fetch-user':'?1',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    info = requests.get(url, headers = header)
    print(info.text)
    token = re.findall(find_token,info.text)
    print("获取token完毕：", token)
    return token[0]

def class_info(number,cookie,token,electiveBatchCode,queryContent,pageSize,pageNumber):
    '''获取选课信息'''
    #注意请求头中存在cookie和token两个验证身份的信息
    header = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-length': '302',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '%s'%cookie,
        'origin': 'https://jwxk.jnu.edu.cn',
        'referer': 'https://jwxk.jnu.edu.cn/xsxkapp/sys/xsxkapp/*default/grablessons.do?token=%s'%token,
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
        'x-requested-with': 'XMLHttpRequest'
    }

    querySetting = {
        "data":{
            "studentCode":number,
            "campus":"",
            "electiveBatchCode":electiveBatchCode,
            "isMajor":"1",
            "teachingClassType":"QXKC",
            "isMajor":"1",
            "queryContent":queryContent},
            "pageSize":pageSize,
            "pageNumber":pageNumber,
            "order":""}
    data = 'querySetting=%s'%querySetting


    url = 'https://jwxk.jnu.edu.cn/xsxkapp/sys/xsxkapp/elective/publicCourse.do'
    #测试网站，可返回请求头相关信息
    # url = 'http://httpbin.org/post'
    info = requests.post(url,headers=header,data = data)
    # print(info.text)
    return info.text

def final_choice(number,cookie,token,teachingClassId,electiveBatchCode):
    '''最终确认选课'''
    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-length': '302',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '%s'%cookie,
        'origin': 'https://jwxk.jnu.edu.cn',
        'referer': 'https://jwxk.jnu.edu.cn/xsxkapp/sys/xsxkapp/*default/grablessons.do?token=%s'%token,
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
        'x-requested-with': 'XMLHttpRequest'
    }
    url = "https://jwxk.jnu.edu.cn/xsxkapp/sys/xsxkapp/elective/volunteer.do"
    addParam = {
        "data":{
            "operationType":"1",
            "studentCode":number,
            "electiveBatchCode":electiveBatchCode,
            "teachingClassId":teachingClassId,
            "isMajor":"1",
            "campus":"1",
            "teachingClassType":"QXKC"
        }
    }
    data = 'addParam=%s'%addParam
    response = requests.post(url,headers=headers,data = data)
    return response.text

def fliter(infos,num,electiveBatchCode,classList):
    '''过滤所需信息'''
    infos_json = json.dumps(infos)
    infos_str = json.loads(infos_json)
    infos_dict = json.loads(infos_str)
    if infos_dict["msg"] == "查询推荐选课成功":
        for dataList in infos_dict["dataList"]:
            if dataList["courseNumber"] in classList:
                print(dataList["courseName"]+f" nums:{num}")
                if dataList["isFull"] != "1":
                    res = final_choice(number,cookie,token,dataList["teachingClassID"],electiveBatchCode)
                    return res
    else:
        print("课程不存在")
    
if __name__ == "__main__":
    number = "1234567890"       # 学号
    passwd = "123456"           # 密码

    classList = ["课程号1","课程号2"]                         # 需要抢的课程号，可以多个
    electiveBatchCode = "cc36cc156d7a4ae1b0cac67202edbfff"   # 每轮次选课可能会改，自己手动改就行
    queryContent = "不能用中文"                               # 搜索的关键词，尽量把需要的课程号涵盖进去，不支持中文
    pageSize = 14                                            # 每页显示的条数，配合跳转页数让需要的课程在同一页
    pageNumber = 0                                           # 跳转页数


    cookie = get_cookies(number,passwd)
    if cookie == None:
        print("请检查账号密码")
        exit()
    token = get_token(number, cookie)
    start = time.time()
    num = 0
    while(True):
        num += 1
        try:
            msg = class_info(number,cookie,token,electiveBatchCode,queryContent,pageSize,pageNumber)
            msg = fliter(msg,num,electiveBatchCode,classList)
            if msg != None:
                print(msg)
                # input("输出enter继续：")
            time.sleep(10)
        except Exception as e:
            end = time.time()
            print(e)
            print(f"Cookies is unavailable:{end-start}s") 
            cookie = get_cookies(number,passwd)
            token = get_token(number, cookie)
            print("已重置cookie")
