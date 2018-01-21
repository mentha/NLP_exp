from cut import Scissor
from mark import Mark
import json
class Tool:
    def __init__(self):
        '用字典对分词和词性标注类初始化'
        self.M = Mark(json.load(open('pos.json')), json.load(open('bposf.json')),json.load(open('iposf.json')))
        self.S = Scissor(json.load(open('wf.json')), json.load(open('iw.json')))
    
    def cut_mark(self, s):
        result = []
        cut = self.S.Cut(s)
        mark = self.M.Sentemark(cut)

        #print(mark)

        #for i in range(0,len(cut)):
            #result.append(cut[i]+'/'+mark[i]+' ')
        return cut
        #print(result)
            #print(cut[i] + '/' + mark[i] +'  ')
if __name__ =='__main__':
    print('Enter: ')
    s = input()
    t = Tool()
    print(t.cut_mark(s))



