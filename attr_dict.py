#-*- encoding:utf-8 -*-

"""
Row的方式好一些，可以自定义没有key时的处理方案，而且不破坏原有的__dict__
"""

class AttrDict(dict):
    """Dict that can get attribute by dot"""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def noUse():
        print 'nouse'


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def noUse():
        print 'nouse'

if __name__ == '__main__':
    td = {'one': 1, 'two': 2, 'three': 3}
    print "----- Row -----"
    # tda is still a dict
    tda = AttrDict(td)
    assert td['one'] == tda.one
    tda.test = '3'
    print tda
    print tda.__dict__
    print AttrDict.__dict__

    tdb = Row(td)
    print "----- Row -----"
    print tdb.one
    tdb.test = '4'
    print tdb
    print tdb.__dict__
    print Row.__dict__
