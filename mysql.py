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

# 用逗号连接
cur.execute("INSERT INTO term_score (term, crter_max, docid_cmax) VALUES (%s, %s, %s)",(query, crter_max, docid_cmax))

import torndb
mysql = torndb.Connection(host='192.168.112.32',user='username',password='123456',database='law')


##############  一些常用的SQL语句  ##############
# 创建表
sql = '''
CREATE TABLE `NewTable` (
`id`  integer NOT NULL AUTO_INCREMENT ,
`name`  varchar(128) NOT NULL DEFAULT '' ,
`birthday`  date NULL ,
`content`  text NOT NULL COMMENT '内容' ,
PRIMARY KEY (`id`),
INDEX `name_index` (`name`) USING BTREE
);
'''


# 插入数据
"insert into salary (id, name, sex, salary) values ('1', 'A', 'm', '2500');"


# 删
'dorp database db_name'  # 删除库
'drop table table_name'  # 删除表, 表结构也没了
"DELETE FROM salary WHERE id=2;"  # 删除某些特定的行
"DELETE FROM salary;"  # 清空表的数据，但是表结构还在


# 改

## 替换字符串
"""
update table_name set
content = replace(content, '\\n', '\n'),
name = replace(name, '\n', ' ')
"""


# 查

## 查找两个表的不同行, A表有的，但是B表没有的
sql = 'SELECT t1.*, t2.*  from A as t1 LEFT JOIN B as t2 ON t1.`name`=t2.`name` OR t1.`name`=t2.new_name WHERE t2.`name` is NULL'

## case的使用
"""
UPDATE salary SET
    sex = CASE sex
        WHEN 'm' THEN 'f' ELSE 'm'
    END;
"""


# 管理
## 修改用户连接ip权限
'''
use user;
update user set host = '%' where user = 'root';
flush privileges;
'''
