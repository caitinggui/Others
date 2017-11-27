#-*- encoding:utf-8 -*-

class AttrDict(dict):
    """Dict that can get attribute by dot"""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if __name__ == '__main__':
    td = {'one': 1, 'two': 2, 'three': 3}
    print "----- Row -----"
    # tda is still a dict
    tda = AttrDict(td)
    print tda
    assert td['one'] == tda.one

    tdb = Row(td)
    print "----- Row -----"
    print tdb
    print tdb.one
