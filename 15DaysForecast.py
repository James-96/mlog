# coding=UTF-8

import urllib2
import re
import json
import datetime
import timedelta
import oss2

pro = ['北京', '江苏', '上海', '浙江']
f = open('15DaysForecast.txt', "w")
f.write("\n")
for num in pro:
    url = 'http://47.95.37.78/areacode/get_data?name=%s' % num
    username = 'bi2018'
    password = 'bi2018'
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(p)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    ref = response.read()

    line = json.loads(ref)

    a = line.keys()
    now_time = datetime.datetime.now().strftime('%Y%m%d')
    fore_time = datetime.datetime.now()+datetime.timedelta(days=15)
    fore_time = fore_time.strftime('%Y%m%d')

    for index in a:
        lon = line[index][index][1]
        lat = line[index][index][2]
        url = 'http://api.mlogcn.com/weatherservice/v2/cma15d/nearest/range/zone?lon=%s&lat=%s&start=%s' \
            '&end=%s&token=e42af58fd4d64e1496f7426da9b19d21' % (lon, lat, now_time, fore_time)
        response = urllib2.urlopen(url)
        data = response.read()
        forecast = json.loads(data)

        f = open('15DaysForecast.txt',"a")
        f.write("\n")
        b = index.encode("UTF-8")
        f.write(b)
        for i in forecast:
            f.write("\n")
            c = json.dumps(i, ensure_ascii=False)
            c = c.encode("UTF-8")
            f.write(c)


# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth('LTAIEWc2Kv9Uht3X', 'DN1S3Tgx9SqeB85RJdIAQOVatZj2tF')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '15-days-forecast')

bucket.put_object_from_file('15DaysForecast.txt', '15DaysForecast.txt')
get_url = bucket.sign_url('GET','15DaysForecast.txt',60)
print get_url

