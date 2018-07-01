#coding:utf-8

from MySQLTool import MySQLTool
import pandas as pd
import datetime
import tushare as ts
import logging

def ConfigLogger(LogFileName):
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# file handle
	fh = logging.FileHandler(LogFileName,mode='w')
	fh.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	# console
	ch = logging.StreamHandler()
	# ch.setLevel(logging.WARNING)
	ch.setLevel(logging.INFO)
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	return logger

def DownloadFile(StartDate,EndDate,FileName,logger):
    logger.info('get market data from tushare.')
    BasicInfoName = './csv/BasicInfo.csv'
    fp = open(BasicInfoName, mode='r')
    line = fp.readline()
    line = fp.readline()
    code = line.split(',')[0]
    # for code in BasicDf['code']:
    df = pd.DataFrame()
    while code != '':
        logger.debug('process %s data.' % code)
        df1 = ts.get_hist_data(code, StartDate, EndDate)
        # 300750 is None
        # if isinstance(df1, pd.DataFrame):
        if len(df1) > 0:
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
    # save to file
    if len(df) > 0:
        df.to_csv(FileName, encoding='gbk')
        logger.info('save to file ok.')
        return True
    else:
        logger.info('no data update, file is empty.')
        return False

def FileToDB(FileName,TableName,logger):
    logger.info('write market data to mysql database.')
    MySQLDB = MySQLTool(logger)
    fp=open(FileName,mode='r')
    line=fp.readline()
    line=fp.readline()
    PreCode=line.split(',')[1]
    logger.debug('process %s data.' % PreCode)
    count=0
    while line != '':
        count = count+1
        # date	code	open	high	close	low	volume	price_change
        # 	p_change	ma5	ma10	ma20	v_ma5	v_ma10	v_ma20
        DataList=line.split(',')
        # print DataList[0],DataList[1]
        if DataList[1] != PreCode:
            PreCode=DataList[1]
            logger.debug('process %s data.' % PreCode)
        MySQLDB.Insert(TableName,tuple(DataList),logger)
        if count % 100 == 0:
            MySQLDB.Commit()
        line = fp.readline()
    MySQLDB.Commit()
    MySQLDB.CloseConn()
    logger.info('save to database ok.')

if __name__=='__main__':
    #download history data
    # StartDate = '2018-01-01'
    # EndDate = '2018-06-03'
    # HistDataName = 'HistData.csv'
    # DownloadFile(StartDate, EndDate, HistDataName)

    # # the first time file to database
    # TableName = 'tb_market_data'
    # FileToDB(HistDataName,TableName)

    # init logger
    strDate = datetime.datetime.today().strftime('%Y%m%d')
    LogFileName = './log/market_' + strDate + '.log'
    logger = ConfigLogger(LogFileName)
    #download every day data
    MySQLDB = MySQLTool(logger)
    TableName = 'tb_market_data'
    PreDate = MySQLDB.GetNearDate(TableName,logger)
    MySQLDB.CloseConn()
    date1 = PreDate[0] + datetime.timedelta(days=1)
    StartDate = date1.strftime('%Y-%m-%d')
    date2 = datetime.datetime.today()
    EndDate = date2.strftime('%Y-%m-%d')
    FileName='./csv/new.csv'
    flag = DownloadFile(StartDate, EndDate, FileName,logger)
    # write file to database
    if flag:
        FileToDB(FileName,TableName,logger)

