#coding:utf-8

import tushare as ts
import pandas as pd

BasicInfoName='BasicInfo.csv'

df=ts.get_stock_basics()
print df.columns
# 在tushare中股票代码作为dataframe的索引使用
df.sort_index(inplace=True)
# print df
# df.to_csv(BasicInfoName,encoding='utf-8')
df.to_csv(BasicInfoName,encoding='gbk')

