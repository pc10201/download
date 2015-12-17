#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created  on 2015/10/29

'''
获取课程id的json请求URL
http://api.maiziedu.com/v2/getCareerDetail/?UUID=680c2c9cc8f147dc8b157b48aa9ddfc9&careerId=13&client=android
'''

import requests
import io

# aria2c命令行绝对地址
download_exe = r'd:\Program Files\aria2\aria2c.exe'
# 视频的保存位置
download_dir = ur'm:\maiziedu'
# 生成的bat脚本路径
bat_file = r's:\urls.bat'
# 此处为课程id列表,例如http://maiziedu.com/course/python/310-8203/的课程id为310
course_id_list = [631, 622]


def download(course_id):
    result = []

    url = 'http://api.maiziedu.com/v2/getCoursePlayInfo/?courseId=%d&client=android' % course_id

    r = requests.get(url)

    json_data = r.json()

    course_name = json_data['data']['course_name']

    video_list = json_data['data']['video_list']

    for video in video_list:
        video_id = video['video_id']
        video_name = video['video_name']
        video_url = video['video_url']
        cmd = ur'"%s" "%s" --file-allocation=none --max-connection-per-server=4  -d "%s\%s" -o "%d_%s.mp4"' \
              % (download_exe, video_url, download_dir, course_name, video_id, video_name)
        print cmd
        result.append(cmd)

    return result


result = []
for course_id in course_id_list:
    result = result + download(course_id)

bat_file = io.open(bat_file, 'w+', encoding='gbk')
for cmd in result:
    bat_file.writelines(cmd + '\r\n')
bat_file.close()
