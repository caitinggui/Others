# coding: utf-8

import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
if zh_pattern.search('no chinese'):
    print('have chinese')
if zh_pattern.search(u"有中文"):
    print('have chinese')
