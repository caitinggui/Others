# coding: utf-8
import sys
import random


class IdiomSolitaire(object):
    """成语接龙"""

    def __init__(self, path=None):
        """
        Args:
            path: 包含成语字典以及成语常用首字的文件路径
            line: 已经接了的成语
            words: 所有的成语
            most: 成语最常用的首字
        """
        self.path = path if path else 'idiom.txt'
        self.line = []
        self.words = set()
        self.most = set()
        with open(self.path, 'r') as f:
            for word in f.xreadlines():
                word = word.decode('utf-8')
                if len(word) < 4:
                    self.most.add(word)
                else:
                    self.words.add(word.strip())

    def findIdiom(self, word):
        """根据首字找到成语, 成语不在已经接龙过的成语列表中，且尾字尽量为常用成语首字"""
        result = []
        for x in self.words:
            if x.startswith(word) and x not in self.line:
                if x[-1] in self.most:
                    return x
                else:
                    result.append(x)
        if result:
            # for w in result:
                # print w
            return result[random.randint(0, len(result) - 1)]
        else:
            return None

    def autoSolitaire(self):
        """根据输入的成语自动成语接龙"""
        word = raw_input("请输入成语, 不要包含任何空格:")
        word = word.decode('utf-8')
        self.line.append(word)
        while True:
            next_word = self.findIdiom(word[-1])
            if next_word:
                print next_word
                self.line.append(next_word)
            else:
                print "can't find idiom"
                print self.line
                break
            word = next_word

    def manSolitaire(self):
        """和用户成语接龙"""
        word = raw_input("请输入成语, 不要包含任何空格:")
        while True:
            word = word.decode('utf-8')
            self.line.append(word)
            next_word = self.findIdiom(word[-1])
            if next_word:
                print next_word
                self.line.append(next_word)
            else:
                print "can't find idiom and you win"
                print self.line
                break
            word = raw_input("")


if __name__ == "__main__":
    idiomsolitire = IdiomSolitaire()
    if sys.argv[1] == "auto":
        idiomsolitire.autoSolitaire()
    else:
        idiomsolitire.manSolitaire()
