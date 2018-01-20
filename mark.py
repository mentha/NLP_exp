class  Mark:
    def __init__(self, dic = {}, dic_first = {}, dic_hmm = {}):
        self.dic = dic
        self.dic_first = dic_first
        self.dic_hmm = dic_hmm
        
    def Wordtype(self, word):
        '返回单词所有词性'
        try:
            '单词词性字典dic'
            wordtypes = self.dic[word]
        except KeyError:
            '如果词典中没有对应词，设置wordtype为n'
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
                    ptag = tag
            Wordtag.append(ptag)
            '如果该词在词典中第一个出现的概率为零'
        except KeyError:
            ptag = self.Wordtype(word)
            if type(ptag) is list:
                if 'n' in ptag:
                    Wordtag.append('n')
                else:
                    Wordtag.append(ptag[0])
            else:
                Wordtag.append(ptag)
    def Wordmark(self, index, folword, Wordtag):
        '对中间词用HMM模型做词性标注'
        wordtypes = self.Wordtype(folword)
        taglead = Wordtag[index]
        max = 0
        for wordtype in wordtypes:
            p = self.dic_hmm[taglead][wordtype]
            if p > max:
                max = p
                pword = wordtype
        Wordtag.append(pword)

    def sentemark(self, wordseq = []):
        Wordtag = []
        self.Firstword(wordseq[0], Wordtag)
        for i in range(1, len(wordseq)):
            self.Wordmark(i - 1, wordseq[i], Wordtag)
        return Wordtag

if __name__ == '__main__':
    import json
    M = Mark(json.load(open('pos.json')), json.load(open('bposf.json')),json.load(open('iposf.json')))
    print(M.sentemark(['今天','天气','晴朗']))
    
