CREATE TABLE IF NOT EXISTS `tb_market_data`(
   `date` DATE comment '日期',
   `code` VARCHAR(100) NOT NULL comment '股票代码',
   `open` FLOAT(10,2) NOT NULL comment '开盘价',
   `high` FLOAT(10,2) NOT NULL comment '最高价',
   `close` FLOAT(10,2) NOT NULL comment '收盘价',
   `low` FLOAT(10,2) NOT NULL comment '最低价',
   `volume` FLOAT(20,2) NOT NULL comment '成交量',
   `price_change` FLOAT(10,2) NOT NULL comment '价格变动',
   `p_change` FLOAT(10,2) NOT NULL comment '涨跌幅',
   `ma5` FLOAT(10,3) NOT NULL comment '5日均价',
   `ma10` FLOAT(10,3) NOT NULL comment '10日均价',
   `ma20` FLOAT(10,3) NOT NULL comment '20日均价',
   `v_ma5` FLOAT(20,2) NOT NULL comment '5日均量',
   `v_ma10` FLOAT(20,2) NOT NULL comment '10日均量',
   `v_ma20` FLOAT(20,2) NOT NULL comment '20日均量'   
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='股票行情数据';