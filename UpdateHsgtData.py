#coding:utf-8

import datetime
import pandas as pd
from MySQLTool import MySQLTool
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
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

def DownloadFile(StartDate, EndDate, FileName, logger):
    pass

def FileToDB(FileName,TableName,logger):
    logger.info('write hsgt data to mysql database.')
    MySQLDB = MySQLTool(logger)
    fp=open(FileName,mode='r')
    line=fp.readline()
    line=fp.readline()
    count=0
    while line != '':
        count = count+1
        # date	code	open	high	close	low	volume	price_change
        # exception count 8768
        if '"' not in line:
            strMsg='[{}] {} is discarded.'.format(count,line.split(',')[0])
            logger.warning(strMsg)
            line = fp.readline()
            continue
        elif line.count('"') == 4:
            strMsg = '[{}] {} contains 2 pairs quotations.'.format(count, line.split(',')[0])
            logger.warning(strMsg)
            line = fp.readline()
            continue
        elif line.count('"') == 2:
            if line.split('"')[0].count(',') != 4:
                strMsg = '[{}] {} exception.'.format(count, line.split(',')[0])
                logger.warning(strMsg)
                line = fp.readline()
                continue
        TempList=line.split('"')
        TempList2=TempList[0].split(',')
        TempList3=TempList2[:-1]
        TempList3.append(TempList[1])
        StockName = TempList3[2]
        # StockName1 = TempList3[2].decode('gbk')
        # StockName2=TempList3[2].decode('gbk').encode("utf-8")
        DataTuple=(TempList3[0],TempList3[1],StockName,
                   float(TempList3[3][:-1]),int(TempList3[4].replace(',','')))
        MySQLDB.Insert(TableName,DataTuple,logger)
        # MySQLDB.Commit()
        if count % 100 == 0:
            MySQLDB.Commit()
            strMsg = '[{}] {} .'.format(count, DataTuple)
            logger.warning(strMsg)
        line = fp.readline()
    MySQLDB.Commit()
    MySQLDB.CloseConn()
    logger.info('save to database ok.')


if __name__=='__main__':
    # init to create hsgt table
    # FileName = 'hsgt_2018.csv'
    # # TableName = 'tb_hsgt_data'
    # TableName = 'temp_tb_hsgt_data'
    # # write file to database
    # FileToDB(FileName,TableName)

    # init logger
    strDate = datetime.datetime.today().strftime('%Y%m%d')
    LogFileName = './log/hsgt_' + strDate + '.log'
    logger = ConfigLogger(LogFileName)
    # download every day data
    MySQLDB = MySQLTool(logger)
    TableName = 'tb_hsgt_data'
    PreDate = MySQLDB.GetNearDate(TableName, logger)
    MySQLDB.CloseConn()
    date1 = PreDate[0] + datetime.timedelta(days=1)
    StartDate = date1.strftime('%Y-%m-%d')
    date2 = datetime.datetime.today()
    EndDate = date2.strftime('%Y-%m-%d')
    FileName = './csv/hsgt_new.csv'
    DownloadFile(StartDate, EndDate, FileName, logger)
    FileToDB(FileName, TableName, logger)