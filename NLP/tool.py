from .cut import Scissor
from .mark import Mark
import json
import lzma
class Tool:
    def __init__(self):
        '用字典对分词和词性标注类初始化'
        self.M = Mark(json.loads(lzma.open('pos.json.xz').read().decode('utf-8')), \
             json.loads(lzma.open('bposf.json.xz').read().decode('utf-8')),\
             json.loads(lzma.open('iposf.json.xz').read().decode('utf-8')))
        self.S = Scissor(json.loads(lzma.open('wf.json.xz').read().decode('UTF-8')), \
                json.loads(lzma.open('iw.json.xz').read().decode('UTF-8')))
    def cut_mark(self, s):
        result = []
        cut = self.S.Cut(s)
        mark = self.M.Sentemark(cut)

        #print(mark)

        for i in range(0,len(cut)):
            result.append(cut[i]+'/'+mark[i])
        return cut
        #print(result)
            #print(cut[i] + '/' + mark[i] +'  ')
if __name__ =='__main__':
    t = Tool()
    print('Enter: ')
    s = input()
    print(t.cut_mark(s))



