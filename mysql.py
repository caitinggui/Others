import logging

import MySQLdb

logging.basicConfig(level=logging.INFO, filename='cut_legislation')
logger = logging.getLogger("main")

conn = MySQLdb.connect('192.168.112.32', 'username', '123456', 'law', charset='utf8')
cur = conn.cursor()
batch_size = 1000
all_num = 100
start = 0
while start < all_num:
    cur.execute("select id, title_short, art from law_rule_result2 where art_new is null")
    datas = cur.fetchall()
    for data in datas:
        try:
            title_short_new = data[1].split(",")
            title_short_new = " ".join(title_short_new)
        except Exception as e:
            logger.error(e)
            title_short_new = ''
        try:
            art_new = data[2].split(",")
            art_new = " ".join(art_new)
        except Exception as e:
            logger.error(e)
            art_new = ''
        # cur.execute('insert into tmp(id) values(%s)', data[0])
        try:
            cur.execute("update law_rule_result2 set title_short_new=%s, art_new=%s where id=%s", (title_short_new.encode('utf-8'), art_new.encode('utf-8'), data[0]))
        except Exception as e:
            logger.error(e)
            logger.error("failed id: %s, title: %s, art: %s", data[0], title_short_new, art_new)
    start += batch_size
    logger.info("start: %s", start)

cur.execute("INSERT INTO term_score (term, crter_max, docid_cmax) VALUES (%s, %s, %s)",(query, crter_max, docid_cmax))

import torndb
mysql = torndb.Connection(host='192.168.112.32',user='username',password='123456',database='law')
