# -*- coding:utf-8 -*-

import sys
import os
import logging

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    TEXT_PATH = sys.argv[1]
else:
    sys.exit('No path')

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
    datefmt='%a, %d %b %H:%M:%S',  
    filename='wordcloud.log',  
    filemode='a')  

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(BASE_PATH, 'msyh.ttf')

logging.info(FONT_PATH)

text_from_file = open(TEXT_PATH).read()

wordlist_after_jieba = jieba.cut(text_from_file, cut_all=True)
wl = ' '.join(wordlist_after_jieba)

wc = WordCloud(font_path=FONT_PATH)
wd = wc.generate(wl)

plt.imshow(wd)
plt.axis('off')
img_path = os.path.join(BASE_PATH, os.path.basename(TEXT_PATH) + '.png')
logging.info(img_path)
wc.to_file(img_path)
plt.show()
