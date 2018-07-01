select * from tb_market_data where code=000001 order by date desc;
/*select * from tb_market_data where date='2018-06-01';*/
select count(distinct(code)) from tb_market_data;
select count(distinct(date)) from tb_market_data;