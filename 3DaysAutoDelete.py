# -*- coding: utf-8 -*-

import oss2
import json
import datetime
import pytz
import re
import time


# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth('LTAIEWc2Kv9Uht3X', 'DN1S3Tgx9SqeB85RJdIAQOVatZj2tF')
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '15-days-forecast')
prefix = []
filename = []
for obj in oss2.ObjectIterator(bucket, delimiter = '/'):
	# 通过is_prefix方法判断obj是否为文件夹。
    if obj.is_prefix():  # 文件夹
        print('directory: ' + obj.key)
        prefix.append(obj.key)
    else:                # 文件
        print('file: ' + obj.key)
        filename.append('%s' % (obj.key))

for index in filename:
    # 获取文件的部分元信息
    simplifiedmeta = bucket.get_object_meta("%s" % (index))
    get_time = simplifiedmeta.headers['Last-Modified']
    get_time = re.sub(' GMT','',get_time)
    filetime = time.strptime(get_time, '%a, %d %b %Y %H:%M:%S')
    timeStamp = int(time.mktime(filetime))
    now_time = time.time()
    last = now_time-timeStamp-28800
    if last>28800:
        bucket.delete_object('%s'% (index))
    else:
        print index

