# -*- coding: utf-8 -*-

class  Mark:
    '''
    词性标注
    '''
    def __init__(self, dic_word = {}, dic_first = {}, dic_hmm = {}):
        '''
        构造一个词性标注类，对输入的list进行词性标注
        :param dic_word:查询一个词所有词性的词典
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
        获取输入list中第一个词的词性
        :param word:第一个词
        :param Wordtag:和输入list对应的词性list
        :return:第一个词对应的词性
        '''
        try:
            #找出最有可能的词性，加在Wordtag中
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
        用HMM进行词性标注
        :param index:上一个词在输入list中的位置
        :param folword:待查询的词
        :param Wordtag:同上
        '''
        wordtypes = self.Wordtype(folword)
        taglead = Wordtag[index]
        max = 0
        #找出最有可能的词性，将其加在Wordtag中
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
        对一个输入list进行词性标注
        :param wordseq:输入的list
        :return:Wordtag
        """
        Wordtag = []
        self.Firstword(wordseq[0], Wordtag)
        for i in range(1, len(wordseq)):
            self.Wordmark(i - 1, wordseq[i], Wordtag)
        return Wordtag

if __name__ == '__main__':
    import lzma
    import json
    M = Mark(json.loads(lzma.open('pos.json.xz').read().decode('utf-8')), \
             json.loads(lzma.open('bposf.json.xz').read().decode('utf-8')),\
             json.loads(lzma.open('iposf.json.xz').read().decode('utf-8')))
    print(M.Sentemark(['今天','天气','晴朗']))
    
