#coding:utf-8

from MySQLTool import MySQLTool
import matplotlib.pyplot as plt

import matplotlib
#指定默认字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['figure.figsize'] = (10.0, 6.0) # 设置figure_size尺寸
matplotlib.rcParams['savefig.dpi'] = 100 #图片像素
matplotlib.rcParams['figure.dpi'] = 100 #分辨率

def ShowHsgtTrend(MySQLDB, TableName, StockCode):
    sql = 'select * from %s where code=\'%s\'' % (TableName,StockCode)
    DataTuple = MySQLDB.Execute(sql)
    x = [DataTuple[i][1] for i in range(len(DataTuple))]
    y = [DataTuple[i][3] for i in range(len(DataTuple))]
    plt.plot(x,y)
    plt.title('Holding proportion of circulation share')
    plt.xlabel('date')
    plt.ylabel('percent')
    # plt.legend()
    plt.grid(True)
    plt.show()

def SearchPercentData(x,data):
    PercentList=[]
    for i in range(len(x)):
        d1=x[i]
        flag=False
        for j in range(len(data)):
            if d1 == data[j][1]:
                PercentList.append(data[j][3])
                flag=True
                break
        if flag == False:
            PercentList.append(0)
    return PercentList

def ShowAllTrend(MySQLDB, TableName, TableName2, StockCode):
    sql = 'select * from %s where code=\'%s\' and date >= \'2018-04-01\' order by date desc' % (TableName2, StockCode)
    DataTuple = MySQLDB.Execute(sql)
    x = [DataTuple[i][0] for i in range(len(DataTuple))]
    y = [DataTuple[i][4] for i in range(len(DataTuple))]
    sql = 'select * from %s where code=\'%s\' and date >= \'2018-04-01\' order by date desc' % (TableName, StockCode)
    DataTuple2 = MySQLDB.Execute(sql)
    y2 = SearchPercentData(x,DataTuple2)
    fig, ax1 = plt.subplots()

    # color = 'tab:red'
    color = 'green'
    # color = '#008000'
    # color = '#000800'
    ax1.set_xlabel('date')
    ax1.set_ylabel('percent', color=color)
    # ax1.plot(x, y2, color=color)
    ax1.bar(x, y2, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    # color = 'tab:blue'
    color = 'red'
    ax2.set_ylabel('close price', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, y, color=color, linewidth=2)
    # ax2.bar(x,y2,color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # label=['percent','close price']
    # plt.legend(label, loc = 0, ncol = 1)
    # plt.grid(True)

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title(u'%s 北向资金持股比例及收盘价' % StockCode)
    plt.savefig('./image/%s.png' % StockCode)
    plt.show()

if __name__=='__main__':
    MySQLDB = MySQLTool()
    TableName='tb_hsgt_data'
    StockCode = '000860'
    # StockCode = '300347'
    # ShowHsgtTrend(MySQLDB, TableName, StockCode)
    TableName2 = 'tb_market_data'
    ShowAllTrend(MySQLDB, TableName, TableName2, StockCode)