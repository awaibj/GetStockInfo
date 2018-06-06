#coding:utf-8

from MySQLTool import MySQLTool
import pandas as pd

HistDataName='HistData.csv'
TableName = 'tb_market_data'

MySQLDB = MySQLTool()
# df = pd.read_csv(HistDataName)
# tuples = [tuple(x) for x in df.values]
# print tuples

fp=open(HistDataName,mode='r')
line=fp.readline()
line=fp.readline()
while line != '':
    DataList=line.split(',')
    print DataList[0],DataList[1]
    MySQLDB.Insert(TableName,tuple(DataList))
    line = fp.readline()
MySQLDB.CloseConn()

