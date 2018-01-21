class  Mark:
    '''
    中文分词
    '''
    def __init__(self, dic_word = {}, dic_first = {}, dic_hmm = {}):
        '''
        构造一个中文分词类
        :param dic_word:
        :param dic_first:
        :param dic_hmm:
        '''
        self.dic_word = dic_word
        self.dic_first = dic_first
        self.dic_hmm = dic_hmm

    def Wordtype(self, word):
        '''
        Get type of certain word
        :param word:
        :return:part of speech as a list
        '''
        try:
            wordtypes = self.dic_word[word]
        except KeyError:
            wordtypes = 'n'
        return wordtypes
        
    def Firstword(self, word, Wordtag):
        '''

        :param word:
        :param Wordtag:
        :return:
        '''
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
        '''
        Marking word by HMM
        :param index: the position of
        :param folword:
        :param Wordtag:
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

        :param wordseq:
        :return:
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
    
