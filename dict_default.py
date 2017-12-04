# coding: utf-8

# 方法2.1

wdict = {}
for word in words:
    if word not in wdict:
        wdict[word] = 0
    wdict[word] += 1

# 方法2.2

# try ... except ... 几乎不怎么影响性能
wdict = {}
for word in words:
    try:
        wdict[word] += 1
    except KeyError:    # 指定KeyError效率会更高
        wdict[word] = 1

# 方法2.3

wdict = {}
get = wdict.get
for word in words:
    wdict[word] = get(word, 0) + 1    # 不直接用wdic.get，这样可以避免每次寻找函数地址

# 方法2.4

wdict.setdefault(key, []).append(new_element)    # 仅在值为可变变量时可用

# 方法2.5

from collections import defaultdict
wdict = defaultdict(int)
for word in words:
    wdict[word] += 1

# 除了方法一，其他都是好办法啊
