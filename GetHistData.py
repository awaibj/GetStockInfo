#coding:utf-8

import tushare as ts
import pandas as pd

BasicInfoName='BasicInfo.csv'
HistDataName='HistData.csv'
StartDate='2018-01-01'
EndDate='2018-06-03'

# BasicDf=pd.DataFrame.from_csv(BasicInfoName,encoding='gbk')
BasicDf=pd.read_csv(BasicInfoName,encoding='gbk')
a=BasicDf['code']
print a.shape
for code in BasicDf['code']:
    pd1=ts.get_hist_data(code,StartDate,EndDate)
    print pd1
    break
