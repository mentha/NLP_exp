class  Mark:
    def __init__(self, dic = {
                '^': 9,
                '$': 9,
                'ab': 1,
                'cd': 2,
                'ef': 3
            }, firstword = {
                '^': {
                    'ab': 1
                    },
                'ab': {
                    'cd': 4,
                    'ef': 5
                    },
                'cd': {
                    'ef': 6
                    }
            }, dic_hmm = {
                '^': {
                    'ab': 1
                    },
                'ab': {
                    'cd': 4,
                    'ef': 5
                    },
                'cd': {
                    'ef': 6
                    }
            }):
        self.dic = dic
        self.dic_first = firstword
        self.dic_hmm = dic_hmm
    def Wordtype(self, word):
        '返回单词所有词性'
        try:
            '单词词性字典dic'
            wordtypes = self.dic[word]
        except KeyError:
            '设置wordtype为n'
            wordtypes = 'n'
        return wordtypes
        
    def Firstword(self, word, Wordtag):
        '返回第一个单词词性'
        try:
            max = 0
            for tag in self.dic_first[word]:
                p = self.dic_first[word][tag]
                if p > max:
                    max = p
                    Wordtag[word] = tag
            '如果该词在词典中第一个出现的概率为零'
        except KeyError:
            pass

    def Wordmark(self, leadword, folword, Wordtag):
        '对中间词用HMM模型做词性标注'
        wordtypes = self.Wordtype(folword)
        taglead = Wordtag[leadword]
        max = 0
        for wordtype in wordtypes:
            p = self.dic_hmm[taglead][wordtype]
            if p > max:
                max = p
                Wordtag[folword] = wordtype

    #def word2seq(self, wordseq = [])
        '将输入的字符串对应成相应的位置信息'
        '防止输入中有两个相同词时wordtag字典出错' 

    def sentemark(self, wordseq = []):
        Wordtag = {}
        self.Firstword(wordseq[0], Wordtag)
        for i in range(1, len(wordseq)):
            self.Wordmark(wordseq[i - 1], wordseq[i], Wordtag)
        return Wordtag

if __name__ == '__main__':
    import json
    M = Mark(json.load(open('pos.json')), json.load(open('bposf.json')),json.load(open('iposf.json')))
    print(M.sentemark(['我','是','吴彦祖']))
    
