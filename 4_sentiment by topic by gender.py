# -*- coding:utf-8 -*-
'''
number of posts within each topic, total sentiment score of each topic, average sentiment score of each topic
number of posts by male/female, total sentiment score of male/female, average sentiment score of male/female
out: average.txt  
'''
import pandas as pd
import xlwt

#start from 0, 读一个加一次
#  total_grade: overall sentiment of each topic
total_grade = 0
# count_item: number of posts within each topic
count_item = 0
# col_num: column number in excel
col_num = 0
# sex_count：number of post by male
sex_count = 0


def toExcel(ind, res):
 
    style = xlwt.XFStyle()  
    font = xlwt.Font()  
    font.name = ''
    font.bold = True  
    style.font = font  
    worksheet.write(ind, 0, res, style)
    print('写入excel···')


def countScore(col_num, num, sex_count, count_item, total_grade):
    data_csv = pd.read_csv("original_data.csv", header=None,
                           names=["author", "sex", "attestation", "url", "content", "release_time", "grade", "num"],
                           encoding="UTF-8") #header
    # delete title row 
    data = data_csv.drop(data_csv.index[0])
    # traverse dataframe
    for index, row in data.iterrows():
        # distinguish Weibo topic by num
        if int(row["num"]) == num:
            if row["sex"] == "男":
                sex_count += 1
            data_dict = {}
            data_dict['author'] = row["author"]
            data_dict['sex'] = row["sex"]
            data_dict['attestation'] = row["attestation"]
            data_dict['url'] = row["url"]
            data_dict['content'] = row["content"]
            data_dict['release_time'] = row["release_time"].split('来自')[0].strip()
            data_dict['grade'] = row["grade"]
            data_dict['num'] = row["num"]
            # print(data_dict)
            count_item += 1 #count the number of data (posts) within each topic 
            total_grade += float(row["grade"]) #if is data from num 1(first topic),add sentiment score
    try:
        avage = total_grade / count_item #calculate average sentiment score total --> grade/number of posts
    except:
        avage = 0
    res = '话题{}，一共{}条数据，总情感分数为：{},平均分为：{},其中男性：{}条，女性：{}条'.format(num, count_item, total_grade,
                                                                  avage, sex_count,
                                                                  count_item - sex_count)
    print(res)
    toExcel(col_num, res)


if __name__ == '__main__':
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('aveage_score')
    # loop 168 topics
    for num in range(1, 169):
        countScore(col_num, num, sex_count, count_item, total_grade)
        col_num += 1
    workbook.save('average.xls')
