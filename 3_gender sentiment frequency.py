# -*- coding:utf-8 -*-
'''
posters' gender, sentiment score, word frequency
168Topic_KeyWord.xls and original_data.csv
'''
import json
import os
import csv
import time
import random
import gevent
import jieba
import requests
import xlwt
from snownlp import SnowNLP
from collections import Counter


class KeyWords(object):
    # prepare stop words list
    def stopwordslist(self):
        stopwords = [line.strip() for line in open('chinesestopwordtxt', encoding='UTF-8').readlines()]
        # print('stopwords:', stopwords)
        return stopwords

    def get_document(self, single_topic_list):
        out_list = []
        # print(data_list)
        for data in single_topic_list:
            # split words
            segments = []
            segs = jieba.cut(str(data), cut_all=True)
            for seg in segs:
                if len(seg) > 1:
                    segments.append(seg)
            
            # take out stop words
            stopwords = self.stopwordslist()
            for word in segments:
                if word not in stopwords:
                    if word != '\t':
                        out_list.append(word)
            # print('out_list:', out_list)
        return out_list

    #  calculate first 22 high frequency words for each Weibo topic
    def count_words(self, single_topic_list): #each topic
        count_dic = dict() 
        out_list = self.get_document(single_topic_list) #
        for word in out_list:
            if word not in count_dic:
                count_dic[word] = 1
            else:
                count_dic[word] += 1
        count_dic = Counter(count_dic).most_common(22)
        # print(count_dic) 
        # {"杨笠":200,"张三":180,...,...  * 22}
        return count_dic 


def getSex(uid): #last part of the URL
    try:
        cook = '_ga=GA1.2.539218203.1637041130; SINAGLOBAL=5567700935681.114.1637041157941; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF8z9GZu54L_3PDy4k1cHVm5JpX5KMhUgL.FoqXeKq41h271h.2dJLoIEBLxKBLB.BLBK5LxKML1-2L1hBLxK-LBKBLBKMLxKqL1-eLB-qt; UOR=www.baidu.com,weibo.com,login.sina.com.cn; ULV=1637739312932:8:8:1:6204344053328.072.1637739312928:1637285374427; ALF=1669429901; SSOLoginState=1637893902; SCF=AnHsqlYuVS-HacGC8x7BvIUH65MOlCGo6u1C-HnAMqffh0VEJ_M5cl9E_UENCfZgLzJeT_lRLFjg8EgOLxPqqh0.; SUB=_2A25MpDdeDeRhGeBK6lQY-C_MwzWIHXVv0C-WrDV8PUNbmtAKLU3ekW9NR_NwQHNG377UVVepP-KrAqNTDkiX8Fju; XSRF-TOKEN=DXZ9vPZ-brWvAcFi-KqFxaCZ; WBPSESS=7lK2OOKOB329kn3o1ZW7C8oiE6UCIDcKCKHRpHpgeeZGLIB6rhUofk2IGI5YOdS9ai5ApcWQl9IzAcNuXFfCH03FFExQYl9aNTu-Mgtj0i6XZLoWFMVf80RQlJa2ttrNIJEccKV0TlwRcjDFjYKdgQ=='
        headers = {
            'accept': 'application/json, text/plain, */*',
            'cookie': cook,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        #requesrs personal information interface --> return json
        u = requests.get('https://weibo.com/ajax/profile/info?custom={}'.format(uid), headers=headers)
        uinfo = json.loads(u.text) #userinfo
        try:
            sex = uinfo['data']['user']['gender'] #"gender":"m",
            print('性别：', sex)
            if sex == 'f':
                return '女'
            elif sex == 'm':
                return '男'
        except:
            return 'None'
    except:
        return 'None'


def getGrade(content):
    
    try:
        s1 = SnowNLP(content).sentiments
        return s1
    except:
        return 0


def toExcel(sec_name, single_count_dic):
    # creat a worksheet
    name = sec_name.replace('_posts.txt', '')
    worksheet = workbook.add_sheet(name)
    style = xlwt.XFStyle()  
    font = xlwt.Font()  # font
    font.name = ''
    font.bold = True  # 黑体
    style.font = font  
    n = 0 # row of Excel
    for i in single_count_dic: #i是{}里面22个词语的每一个
        worksheet.write(n, 0, i[0], style) #n是行，0是列，i[0]是数据 这里写的是“杨笠”
        worksheet.write(n, 1, i[1], style) #这里写的是200（词频）
        print('Insert one data···')
        n += 1 
        print('写入excel···')


def toCsv(single_data_item):
    #  archive to csv
    csv_writer.writerow(
        [single_data_item['author'], single_data_item['sex'], single_data_item['attestation'], single_data_item['url'],
         single_data_item['content'], single_data_item['release_time'],
         single_data_item['grade'], single_data_item['num']])
    print('成功写入csv···')


if __name__ == '__main__':
    # creat a workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    fc = open('original_data.csv', 'w', encoding='utf-8-sig')
    csv_writer = csv.writer(fc)
    # csv header
    csv_writer.writerow(["author", "sex", "attestation", "url", "content", "release_time", "grade", "num"])
    first_dirs = os.listdir('results_clear_moreThan50')
    # calculate high frequency words of all posts
    all_topic_list = []
    
    
    # distinguished by topics
    topic = 1
    for sec_name in first_dirs:
        print('话题：', sec_name)
        with open(f'results_clear_moreThan50/{sec_name}', "r", encoding='utf-8', newline="") as f:  # 打开文件
            datas = f.readlines()  
            # print(datas)
            # create a list to store high frequency words for each topic 
            single_topic_list = []
            for data in datas:
                try:
                    single_data_item = {}
                    # print("single_data:", data)
                    cut_data = data.split('||')
                    author = cut_data[0]
                    attestation = cut_data[1]
                    url = cut_data[2]
                    content = cut_data[3]
                    release_time = cut_data[4]
                    # get sentiment score
                    grade = getGrade(content)
                    # get posters' gender 
                    sex = getSex(url.split('/')[-1]) #//weibo.com/5882316869 数字
                    single_data_item['author'] = author
                    single_data_item['sex'] = sex
                    single_data_item['attestation'] = attestation
                    single_data_item['url'] = url
                    single_data_item['content'] = content
                    single_data_item['release_time'] = release_time
                    single_data_item['grade'] = grade
                    single_data_item['num'] = topic
                    print('数据', single_data_item)
                    print('·············', single_data_item['num'])
                    toCsv(single_data_item)
                    single_topic_list.append(content)
                    all_topic_list.append(content) #169th sheetc --> store high frequency words of all posts
                except:
                    pass
                # time.sleep(random.randint(1,3)+random.random())
            # calculate word frequency of posts within each Weibo topic
            single_count_dic = KeyWords().count_words(single_topic_list)
            print(single_count_dic)
            # stored in excel      
            toExcel(sec_name, single_count_dic) 
        topic += 1 #proceed next topic
    # calculate word frequency of all posts
    all_count_dic = KeyWords().count_words(all_topic_list) #同178
    # all_KeyWords 为 sheetname
    toExcel('all_KeyWords', all_count_dic) #同181
    print(all_count_dic)
    workbook.save('168Topic_KeyWord.xls')
  
    fc.close()
