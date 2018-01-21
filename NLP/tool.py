from .cut import Scissor
from .mark import Mark
import json
import lzma
class Tool:
    def __init__(self):
        '''
        对分词类和词性标注类进行初始化
        '''
        self.M = Mark(json.loads(lzma.open('NLP/pos.json.xz').read().decode('utf-8')), \
             json.loads(lzma.open('NLP/bposf.json.xz').read().decode('utf-8')), \
             json.loads(lzma.open('NLP/iposf.json.xz').read().decode('utf-8')))
        self.S = Scissor(json.loads(lzma.open('NLP/wf.json.xz').read().decode('UTF-8')), \
                json.loads(lzma.open('NLP/iw.json.xz').read().decode('UTF-8')))
        
    def Cut_mark(self, s):
        '''
        对一个字符串进行分词和词性标注
        :param s: 待处理的字符串
        :return: list类型的处理结果
        '''
        result = []
        cut = self.S.Cut(s)
        mark = self.M.Sentemark(cut)
        for i in range(0,len(cut)):
            result.append(cut[i]+'/'+mark[i])
        return result
    
if __name__ =='__main__':
    t = Tool()
    print('Enter: ')
    s = input()
    t.Cut_mark(s)



