#!/usr/bin/env python
# coding: utf-8

import MySQLdb

conn = MySQLdb.connect(host='192.168.10.9', port=3307,
                       user='username', passwd='password', db='mydb')
cursor = conn.cursor()
cursor.execute(" SELECT ID,QUESTION,RICH_TEXT,PURE_TEXT,DATA_CLASS_ID,STATE,USER_ID,COMPANY_CODE,DATA_SOURCE,"
               + "CONSULT_AMOUNT,USE_CHANNEL"
               + " from T_DATA_DICTIONARIES  where QUESTION is not NULL;")
data = cursor.fetchall()
print data
