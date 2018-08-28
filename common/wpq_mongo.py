# -*- coding: utf-8 -*-

from pymongo import MongoClient

class mongodb():

    #初始化
    def __init__(self, dbname, colname, port = 27017, ip = 'localhost'):
        self.CON = MongoClient(ip,port)
        self.DB = self.CON[dbname]
        self.COL = self.DB[colname]

    #切换数据库
    def switch(self, colname, dbname = ''):
        if dbname != '':
            self.DB = self.CON[dbname]
        self.COL = self.CON[colname]

    #插入函数
    def insert(self, values):
        self.COL.insert(values)

    #查询函数
    def select(self,  parameter='', one = False):
        if parameter != '':
            if one:
                return self.COL.find_one(parameter)
            else:
                return self.COL.find(parameter)
        else:
            if one:
                return self.COL.find_one()
            else:
                return self.COL.find()

    #更新函数
    def update(self, par_val, par_sel ):
        self.COL.update(par_sel, {'$set':par_val})

    #删除函数
    def delete(self, par_sel = ''):
        if par_sel == '':
            self.COL.remove()
        else:
            self.COL.remove(par_sel)