# coding: utf-8
import sys
import random

from xpinyin import Pinyin

"""还有一种改进方法：
words = {u'桂': ['桂子兰孙', '桂子飘香'],
         u'桃': ['桃之夭夭', '桃僵李代']
}
这样直接可以根据首字取words的值
然后去列表里面的成语，判断尾字对应的首字成语有多少个，比如
已经取出'桂子兰孙',那么可以判断len(words[u'孙'])，如果大于2就说明这个成语用作接龙可以
这样效率可以提高很多
"""


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
        self.little = set()
        flag = 'idiom'
        with open(self.path, 'r') as f:
            for word in f.xreadlines():
                word = word.decode('utf-8').strip()
                if word == "#little":
                    flag = 'little'
                elif word == "#most":
                    flag = 'most'
                if flag == "idiom":
                    self.words.add(word)
                elif flag == "little":
                    self.little.add(word)
                else:
                    self.most.add(word)

    def findIdiom(self, word):
        """
        根据首字找到成语, 成语不在已经接龙过的成语列表中，且尾字尽量为常用成语首字
        Args:
            word: 成语的首字，并非整个成语
        """
        result = []
        most_result = []
        little_result = []
        for x in self.words:
            if x.startswith(word) and x not in self.line:
                if x[-1] in self.most:
                    most_result.append(x)
                elif x[-1] in self.little:
                    little_result.append(x)
                else:
                    result.append(x)
        if most_result:
            result = most_result
        elif little_result:
            result = little_result
        if result:
            return result[random.randint(0, len(result) - 1)]
        else:
            return None

    def autoSolitaire(self):
        """根据输入的成语自动成语接龙"""
        word = raw_input("请输入成语, 不要包含任何空格:")
        word = word.decode('utf-8').strip()
        self.line.append(word)
        while True:
            next_word = self.findIdiom(word[-1])
            if next_word:
                print next_word
                self.line.append(next_word)
            else:
                print "can't find idiom"
                print len(self.line)
                break
            word = next_word

    def manSolitaire(self):
        """和用户成语接龙"""
        word = raw_input("请输入成语, 不要包含任何空格:")
        while True:
            word = word.decode('utf-8').strip()
            self.line.append(word)
            next_word = self.findIdiom(word[-1])
            if next_word:
                print next_word
                self.line.append(next_word)
            else:
                print "can't find idiom and you win"
                print len(self.line)
                break
            word = raw_input("")


class IdiomSolitaireNew(IdiomSolitaire):
    """速度更快一些，支持拼音的成语接龙"""

    def __init__(self, path=None, use_pinyin=True):
        self.path = path if path else 'idiom.txt'
        self.line = []
        self.words = {}
        self.use_pinyin = use_pinyin
        if self.use_pinyin:
            self.pinyin = Pinyin()
        with open(self.path, 'r') as f:
            for word in f.xreadlines():
                word = word.decode('utf-8').strip()
                # 成语长度大于等于4
                if len(word) >= 4:
                    p = self.getPinyin(word[0])
                    if p in self.words:
                        self.words[p].append(word)
                    elif p:
                        self.words[p] = []

    def getPinyin(self, word):
        """获取首字的拼音，如果初始化时不适用拼音，则原字返回"""
        if self.use_pinyin:
            return self.pinyin.get_pinyin(word, show_tone_marks=True)
        else:
            return word

    def findIdiom(self, word):
        """
        根据首字找到成语, 成语不在已经接龙过的成语列表中，且尾字尽量为常用成语首字
        Args:
            word: 成语的首字，并非整个成语
        """
        p = self.getPinyin(word)
        if p not in self.words:
            return None
        result = []
        most_result = []
        little_result = []
        for x in self.words[p]:
            if x in self.line:
                continue
            next_p = self.getPinyin(x[-1])
            tail_len = len(self.words.get(next_p, []))
            # 成语的尾字吻合多个成语的首字
            if tail_len > 2:
                most_result.append(x)
            elif tail_len > 0:
                little_result.append(x)
            else:
                result.append(x)
        if most_result:
            result = most_result
        elif little_result:
            result = little_result
        if result:
            return result[random.randint(0, len(result) - 1)]
        else:
            return None


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "hanzi":
        idiomsolitire = IdiomSolitaireNew(use_pinyin=False)
    else:
        idiomsolitire = IdiomSolitaireNew()
    if len(sys.argv) > 1 and sys.argv[1] == "auto":
        idiomsolitire.autoSolitaire()
    else:
        idiomsolitire.manSolitaire()
