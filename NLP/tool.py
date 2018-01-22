from .cut import Scissor
from .mark import Mark

import json
import lzma
import pkg_resources as pkgres

rc = lambda n: pkgres.resource_filename(__name__, n)

M = Mark(json.loads(lzma.open(rc('pos.json.xz')).read().decode('utf-8')), json.loads(lzma.open(rc('bposf.json.xz')).read().decode('utf-8')), json.loads(lzma.open(rc('iposf.json.xz')).read().decode('utf-8')))
S = Scissor(json.loads(lzma.open(rc('wf.json.xz')).read().decode('UTF-8')), json.loads(lzma.open(rc('iw.json.xz')).read().decode('UTF-8')))

def CutMark(s):
    '''
    对一个字符串进行分词和词性标注
    :param s: 待处理的字符串
    :return: list类型的处理结果
    '''
    result = []
    cut = S.Cut(s)
    mark = M.Sentemark(cut)
    return (cut, mark)

if __name__ =='__main__':
    print('Enter: ')
    s = input()
    CutMark(s)
