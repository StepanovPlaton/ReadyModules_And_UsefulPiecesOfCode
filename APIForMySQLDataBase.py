#! /usr/bin/python3

# -*- coding: utf-8 -*-

import MySQLdb

class DataBaseAPI():
    def __init__(self, ip, user_name, password, db_name):
        self.ip_default = ip
        self.default_user_name = user_name
        self.default_password = password
        self.default_db_name = db_name
    def Execute(self, command, ip=None, user_name=None, password=None, db_name=None, quiet=False):
        base = MySQLdb.connect((lambda x: self.ip_default if(x is None) else ip)(ip),
                               (lambda x: self.default_user_name if(x is None) else user_name)(user_name),
                               (lambda x: self.default_password if(x is None) else password)(password),
                               (lambda x: self.default_db_name if(x is None) else db_name)(db_name),
                               use_unicode=True, charset="utf8")
        return_value = None
        try:
            cursor = base.cursor()
            cursor.execute(command)
            if(command.lower().find("select") != -1):
                return_value = cursor.fetchall()
            cursor.close()
            base.commit()
        except BaseException as e:
            if(not quiet):
                print("! ERROR ! Command -", command)
                print("Transaction failed, rolling back")
            base.rollback()
        return return_value