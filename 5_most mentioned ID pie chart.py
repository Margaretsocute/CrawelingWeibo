# -*- coding:utf-8 -*-
'''
most mentioned IDs-->pie chart
out：pie chart
'''
import re
import pandas as pd
import xlwt
import matplotlib.pyplot as plt


def read_csv_file():
    data_csv = pd.read_csv("original_data.csv", header=None,
                           names=["author", "sex", "attestation", "url", "content", "release_time", "grade", "num"],
                           encoding="UTF-8")
    # delete title row
    data = data_csv.drop(data_csv.index[0])
    # traverse dataframe
    num = 0
    # res_dict   similar to “张三”:180
    res_dict = {}
    for index, row in data.iterrows():
        try:
            content = row['content']
            if '@' in content:
                # print("content:",content)
                result = re.compile('(@.*?)(?=:)').findall(content) #regular expression matching --> match the content comes after @
                if result == []:
                    result = re.compile('(@.*?)(?= )').findall(content)
                print("result:", result)
                for r in result:
                    res = r.strip()
                    if len(res) > 20:
                        pass
                    elif res == '@':
                        pass
                    else:
                        if res not in res_dict: #res is the id matched by previous step
                            res_dict[res] = 1 #if new id occurs, add it to the list and mark the frequency as 1
                        else:
                            res_dict[res] += 1 #if old id, num +1
                        num += 1
            print(index)
            # print("res_dict:",index, res_dict)
        except:
            pass
    print("res_dict:", res_dict)
    print(num)
    return num, res_dict


def toExcel(excel_data):
    # crear a workbook
    worksheet = workbook.add_sheet('count_person')
    style = xlwt.XFStyle() 
    font = xlwt.Font() 
    font.name = ''
    font.bold = True  
    style.font = font  
    n = 0
    for i in excel_data:
        worksheet.write(n, 0, i[0], style)
        worksheet.write(n, 1, i[1], style)
        print('Insert one data···')
        n += 1
        print('写入excel···')
    workbook.save('Mention_Count.xls')


def sortDict():

    num, res_dict = read_csv_file()
    excel_data = sorted(res_dict.items(), key=lambda pair: pair[1], reverse=True)[:50] #rank --> first 50
    map_data = sorted(res_dict.items(), key=lambda pair: pair[1], reverse=True)[:10] #rank --> first 10 
    return num, excel_data, map_data #num is the total numver of @,  excel_data is the data of the first 50（id and corresponding frequency） mapdata is the data of first 10


def mapData(num, map_data):
    labels = [] #name of the firsr 10 ID
    value = [] #corresponding being mentioned frequency 
    for k, v in map_data:
        labels.append(k)
        value.append(v)
        print('总提及数为：{}，<{}> 被提及{}次，占比：{}'.format(num, k, v, v / num))
    return labels, value


def make_autopct(value):
    def my_autopct(pct): #pct is the name of firsr 10 ID
        total = sum(value) #calculate total mentioned frequency of the first 10 ID
        val = int(round(pct * total / 100.0)) #calculate the proportion
        # display both ID name and proportion
        return '{p:.2f}%({v:d})'.format(p=pct, v=val) #pie chart

    return my_autopct


if __name__ == '__main__':
    # creat a workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    num, excel_data, map_data = sortDict() 
    toExcel(excel_data)
    labels, value = mapData(num, map_data)
    make_autopct(value) 
    # select font
    plt.rcParams['font.sans-serif'] = ['simhei']
    plt.rcParams['axes.unicode_minus'] = False
    # name of pie chart
    plt.title("Percentage of the Top 10 Mentioned Accounts ")
    # making pie chart, keep 2 decimal
    plt.pie(value, labels=labels, autopct=make_autopct(value))
    plt.show()
