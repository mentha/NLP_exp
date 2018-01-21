class  Mark:
    '''
    词性标注
    '''
    def __init__(self, dic_word = {}, dic_first = {}, dic_hmm = {}):
        '''
        构造一个词性标注类，对list进行词性标注
        :param dic_word:查询一个字所有词性的词典
        :param dic_first:查询第一个词相关信息的词典
        :param dic_hmm:包含条件概率信息的词典
        '''
        self.dic_word = dic_word
        self.dic_first = dic_first
        self.dic_hmm = dic_hmm

    def Wordtype(self, word):
        '''
        获得一个词所有可能的词性
        :param word:待查询的词
        :return:该词所有可能词性的list
        '''
        try:
            wordtypes = self.dic_word[word]
        except KeyError:
            wordtypes = 'n'
        return wordtypes
        
    def Firstword(self, word, Wordtag):
        '''
        获取list中第一个词的词性
        :param word:第一个词
        :param Wordtag:和输入list对应的词性list
        :return:第一个词的所有可能词性
        '''
        try:
            max = 0
            for tag in self.dic_first[word]:
                p = self.dic_first[word][tag]
                if p > max:
                    max = p
                    ptag = tag
            Wordtag.append(ptag)
            #如果该词在第一个位置未出现过
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
        '''
        用HMM模型进行词性标注
        :param index:上一个词在list中的位置
        :param folword:待查询的词
        :param Wordtag:同上
        :return:
        '''
        wordtypes = self.Wordtype(folword)
        taglead = Wordtag[index]
        max = 0
        for wordtype in wordtypes:
            try:
                p = self.dic_hmm[taglead][wordtype]
            except KeyError:
                p = 0
            if p >= max:
                max = p
                pword = wordtype
        Wordtag.append(pword)

    def Sentemark(self, wordseq = []):
        """
        对一个list进行分词
        :param wordseq:输入的list
        :return:Wordtag
        """
        Wordtag = []
        self.Firstword(wordseq[0], Wordtag)
        for i in range(1, len(wordseq)):
            self.Wordmark(i - 1, wordseq[i], Wordtag)
        return Wordtag

if __name__ == '__main__':
    import json
    M = Mark(json.load(open('pos.json')), json.load(open('bposf.json')),json.load(open('iposf.json')))
    print(M.sentemark(['今天','天气','晴朗']))
    
