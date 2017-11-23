import pymongo, torndb

mysql = torndb.Connection(host='192.168.12.35',user='root',password='123456',database='law')

mongo = pymongo.MongoClient('192.168.10.219', port=23521)

legislation = mongo.law_platform.legislation
legislation.drop()
start = 0
while True:
    size = 50000
    r = legislation.insert(mysql.query("select * from law_rule_result2 limit %d, %d;" % (start, size))) 
    print 'insert start: %s, size: %s' % (start, size)
    start += size
print 'OK'
