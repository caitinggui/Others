# coding:utf-8

import os
import json

from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED
from jieba.analyse import ChineseAnalyzer

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 创建schema, 在此处有定义的说明可以被用来检索,但STORED不可被检索,只是\
#    表面会出现在搜索的结果中
# stored=True表示可以出现在检索结果中，如果content内容较多\
#    为避免占用空间过大，可以定义为False，然后通过ID定位到数据库\
#    中，通过数据库获取
schema = Schema(
    title=TEXT(stored=True, analyzer=analyzer, vector=True),
    path=ID(stored=True),
    # 可被检索，但content的内容不出现在检索的结果中
    content=TEXT(stored=False, analyzer=analyzer),
    id=STORED()
    )

# 存储schema信息到'indexdir'目录下
indexdir = 'indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
ix = create_in(indexdir, schema)

# 安照schema定义信息，增加需要建立索引的文档
# 注意：字符串格式需要为Unicode格式
writer = ix.writer()
writer.add_document(title=u'第一篇文档', path=u'www.baidu.com', id=u'1',
                    content=u'这是我们增加的第一篇文脏，又名文档')
writer.add_document(title=u'第二篇文档', path=u'www.google.com', id=u'2',
                    content=u'这是我们增加的第二篇文档, very interesting')
writer.commit()

# 创建一个检索器
searcher = ix.searcher()

# 检索标题中出现“文档”的文档
results = searcher.find("content", u"我们")
results_path = searcher.find("path", u"www.google.com")

# 检索出来的第一个结果，数据格式为dict{'title':.., 'content':,,,}
firstdoc = results[0].fields()

jsondoc = json.dumps(firstdoc, ensure_ascii=False)

print results[0]
print 'search title'
print jsondoc # 打印检索出的文档全部内容
print results[0].highlights("title") # 高亮标题中的检索词
print results[0].score # bm25分数
print 'search path'
print json.dumps(results_path[0].fields(), ensure_ascii=False)
