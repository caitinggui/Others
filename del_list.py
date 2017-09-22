# coding: utf-8
"""
循环时删除列表中的元素可以采用倒序的方式
"""
test = [3, 6, 2, 8, 9, 5, 232, 52, 12, 5, 23, 1, 2]
for x in test[::-1]:
    if x % 2 == 0:
        test.remove(x)
        print test
print test
