#coding:utf-8

from MySQLTool import MySQLTool
import pandas as pd
import datetime
import tushare as ts

def DownloadFile(StartDate,EndDate,FileName):
    BasicInfoName = 'BasicInfo.csv'
    fp = open(BasicInfoName, mode='r')
    line = fp.readline()
    line = fp.readline()
    code = line.split(',')[0]
    # for code in BasicDf['code']:
    df = pd.DataFrame()
    while code != '':
        df1 = ts.get_hist_data(code, StartDate, EndDate)
        # 300750 is None
        if isinstance(df1, pd.DataFrame):  # df1 != None:
            data2 = [code for i in range(df1.shape[0])]
            df1['code'] = data2
            list1 = df1.columns
            list2 = []
            list2.append(list1[-1])
            list2.extend(list1[0:-1])
            df1 = df1.reindex(columns=list2)
            # df=df.append(df1,ignore_index=True)
            df = df.append(df1)
        line = fp.readline()
        code = line.split(',')[0]
        print code
    # save to file
    df.to_csv(FileName, encoding='gbk')

def FileToDB(FileName,TableName):
    MySQLDB = MySQLTool()
    fp=open(FileName,mode='r')
    line=fp.readline()
    line=fp.readline()
    PreCode=line.split(',')[1]
    d1=datetime.datetime.today()
    d1=d1.strftime('%Y-%m-%d %H:%M:%S')
    print '[%s] %s' % (d1,PreCode)
    count=0
    while line != '':
        count = count+1
        DataList=line.split(',')
        # print DataList[0],DataList[1]
        if DataList[1] != PreCode:
            PreCode=DataList[1]
            d1=datetime.datetime.today()
            d1 = d1.strftime('%Y-%m-%d %H:%M:%S')
            print '[%s] %s' % (d1, PreCode)
        MySQLDB.Insert(TableName,tuple(DataList))
        if count % 100 == 0:
            MySQLDB.Commit()
        line = fp.readline()
    MySQLDB.Commit()
    MySQLDB.CloseConn()

if __name__=='__main__':
    #download history data
    # StartDate = '2018-01-01'
    # EndDate = '2018-06-03'
    # HistDataName = 'HistData.csv'
    # DownloadFile(StartDate, EndDate, HistDataName)

    # # the first time file to database
    # TableName = 'tb_market_data'
    # FileToDB(HistDataName,TableName)

    #download every day data
    MySQLDB = MySQLTool()
    TableName = 'tb_market_data'
    PreDate = MySQLDB.GetNearDate(TableName)
    MySQLDB.CloseConn()
    date1 = PreDate[0] + datetime.timedelta(days=1)
    StartDate = date1.strftime('%Y-%m-%d')
    date2 = datetime.datetime.today()
    EndDate = date2.strftime('%Y-%m-%d')
    FileName='new.csv'
    DownloadFile(StartDate, EndDate, FileName)
    # write file to database
    FileToDB(FileName,TableName)

