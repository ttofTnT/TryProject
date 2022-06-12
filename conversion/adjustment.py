from conversion.toBraille import toBraille as tb
import pypinyin


class Adjustment(object):
    def __init__(self, word):
        self.ogword = word
        self.pinyin = Adjustment.chineseToPinyin(word)
        self.braille = Adjustment.chineseToBraille(word)
        self.machinedata = []
        for i in self.braille:
            self.machinedata.append(Adjustment.brailleToMachine(i))

    @staticmethod
    def chineseToPinyin(word):  # 汉字转换成拼音
        pinyin = pypinyin.lazy_pinyin(word)  # 列表
        return pinyin

    @staticmethod
    def chineseToBraille(word):  # 汉字转换成盲文
        result = []
        a = tb(word)[1].split("-")
        for i in a:
            data = []
            for j in i:
                data.append(int(j))
            result.append(tuple(data))
        return result

    @staticmethod
    def brailleToMachine(tp):  # 盲文转换成机器数据
        t = [0, 0, 0, 0, 0, 0]
        for i in tp:
            t[i - 1] = 1
        return tuple(t)


def putout(word):
    a = Adjustment(word)
    print("原始句子")
    print(a.ogword)
    print("拼音")
    print(a.pinyin)
    print("盲文序列")
    print(a.braille)
    print("机器序列")
    print(a.machinedata)


if __name__ == '__main__':
    putout("我爱中国")
