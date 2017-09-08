#-*- encoding:utf-8 -*-

class AttrDict(dict):
    """Dict that can get attribute by dot"""

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


if __name__ == '__main__':
    td = {'one': 1, 'two': 2, 'three': 3}
    # tda is still a dict
    tda = AttrDict(td)
    print tda
    print assert td['one'] == tda.one
