#coding:utf-8

import tushare as ts
import pandas as pd

BasicInfoName='BasicInfo.csv'
HistDataName='HistData.csv'
StartDate='2018-01-01'
EndDate='2018-06-03'

# 使用pandas读取，股票代码前面的零被去掉了
# BasicDf=pd.DataFrame.from_csv(BasicInfoName,encoding='gbk')
# BasicDf=pd.read_csv(BasicInfoName,encoding='gbk')
# a=BasicDf['code']
# print a.shape
fp=open(BasicInfoName,mode='r')
line=fp.readline()
line=fp.readline()
code = line.split(',')[0]
# for code in BasicDf['code']:
df=pd.DataFrame()
while code != '':
    df1=ts.get_hist_data(code,StartDate,EndDate)
    data2 = [code for i in range(df1.shape[0])]
    df1['code']=data2
    # df=df.append(df1,ignore_index=True)
    df = df.append(df1)
    line = fp.readline()
    code = line.split(',')[0]

