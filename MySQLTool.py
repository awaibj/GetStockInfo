#coding:utf-8

import pymysql

class MySQLTool:
	ip = "192.168.1.113"
	port = 3306
	username = 'stock'
	password = 'stock789'
	dbname = 'db_stock_plat'

	# init
	def __init__(self):
		try:
			# self.tablename = TableName
			self.db = pymysql.connect(self.ip, self.username, self.password, self.dbname)
			self.cur = self.db.cursor()
		except pymysql.Error as e:
			print(e.args[0])

	# fechone
	def FetchOne(self,TableName):
		try:
			self.cur.execute("SELECT * from " + TableName)
			return self.cur.fetchone()
		except pymysql.Error as e:
			print(e.args[0])

	# fechall
	def FetchAll(self,TableName):
		try:
			self.cur.execute("SELECT * from " + TableName)
			return self.cur.fetchall()
		except pymysql.Error as e:
			print(e.args[0])

	def GetNearDate(self,TableName):
		try:
			sql = "select date from %s order by date desc" % (TableName)
			# print sql
			self.cur.execute(sql)
			return self.cur.fetchone()
		except pymysql.Error as e:
			print(e)

	# insert
	def Insert(self, TableName, tuple):
		try:
			sql = "INSERT INTO %s VALUES %s" % (TableName,tuple)
			# print sql
			self.cur.execute(sql)
			# self.db.commit()
		except pymysql.Error as e:
			print(e)

	# get description
	def GetDescription(self,TableName):
		try:
			self.cur.execute("SELECT * from " + TableName)
			return self.cur.description
		except pymysql.Error as e:
			print(e)

	# truncate table
	def Truncate(self,TableName):
		sql = "TRUNCATE TABLE %s" % TableName
		self.cur.execute(sql)
		self.db.commit()
		
	# commit
	def Commit(self):
		self.db.commit()

	# close
	def CloseConn(self):
		self.cur.close()
		self.db.close()