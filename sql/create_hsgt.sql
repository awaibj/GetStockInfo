CREATE TABLE IF NOT EXISTS `tb_hsgt_data`(
   `code` VARCHAR(100) NOT NULL comment '股票代码',
	`date` DATE comment '日期',
   `name` VARCHAR(100) comment '股票名称',   
   `percent` FLOAT(10,2) comment '占流通股百分比',
   `sharenum`INTEGER comment '持股数量'   
)ENGINE=InnoDB DEFAULT CHARSET=utf8 comment='北向持股数据';