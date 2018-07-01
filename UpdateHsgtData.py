#coding:utf-8

import datetime
import pandas as pd
from MySQLTool import MySQLTool
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

def FileToDB(FileName,TableName):
    MySQLDB = MySQLTool()
    fp=open(FileName,mode='r')
    line=fp.readline()
    line=fp.readline()
    count=0
    d1 = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print '[%s] start.' % (d1)
    while line != '':
        count = count+1
        # date	code	open	high	close	low	volume	price_change
        # exception count 8768
        if '"' not in line:
            strMsg='[{}] {} is discarded.'.format(count,line.split(',')[0])
            print strMsg
            line = fp.readline()
            continue
        elif line.count('"') == 4:
            strMsg = '[{}] {} contains 2 pairs quotations.'.format(count, line.split(',')[0])
            print strMsg
            line = fp.readline()
            continue
        elif line.count('"') == 2:
            if line.split('"')[0].count(',') != 4:
                strMsg = '[{}] {} exception.'.format(count, line.split(',')[0])
                print strMsg
                line = fp.readline()
                continue
        TempList=line.split('"')
        TempList2=TempList[0].split(',')
        TempList3=TempList2[:-1]
        TempList3.append(TempList[1])
        StockName = TempList3[2]
        StockName1 = TempList3[2].decode('gbk')
        StockName2=TempList3[2].decode('gbk').encode("utf-8")
        DataTuple=(TempList3[0],TempList3[1],StockName,
                   float(TempList3[3][:-1]),int(TempList3[4].replace(',','')))
        MySQLDB.Insert(TableName,DataTuple)
        MySQLDB.Commit()
        if count % 100 == 0:
            MySQLDB.Commit()
            strMsg = '[{}] {} .'.format(count, DataTuple)
            print strMsg
        line = fp.readline()
    MySQLDB.Commit()
    MySQLDB.CloseConn()
    d1 = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print '[%s] end.' % (d1)

if __name__=='__main__':
    FileName = 'hsgt_2018.csv'
    # TableName = 'tb_hsgt_data'
    TableName = 'temp_tb_hsgt_data'
    # write file to database
    FileToDB(FileName,TableName)