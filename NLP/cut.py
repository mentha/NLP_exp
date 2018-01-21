#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import math
import re


from base64 import b32encode


def genc(s):
#    return str(s).replace('(', 'A').replace(')', 'B').replace(' ', '_')
    return b32encode(str(s).encode('UTF-8')).decode('ASCII').replace('=', '_')

def weightProc(w):
    return -math.log(w)

def shortest(g, f, t):
    return nx.shortest_path(g, f, t, 'weight')

def dotGraph(g, s):
    s = '^' + s + '$'
    r = ''
    r += 'digraph {\n'
    r += '\tsubgraph {\n'
    r += '\t\trankdir=LR\n'
    for i in range(len(s)):
        r += '\t\t' + genc((i, i)) + ' [ label="{}" ]'.format(s[i]) + '\n'
    r += '\t}\n'
    for n in g.nodes():
        if n[0] != n[1]:
            r += '\t' + genc(n) + ' [ label="{}" ]'.format(s[n[0]:n[1] + 1]) + '\n'
    for e in g.edges():
        p, c = e
        w = g[p][c]['weight']
        g[p][c]['rweight'] = w
        nw = weightProc(w)
        g[p][c]['weight'] = nw
    p = None
    for e in shortest(g, (0, 0), (len(s) - 1, len(s) - 1)):
        if not p is None:
            g[p][e]['selected'] = 1
        p = e
    for e in g.edges():
        p, c = e
        w = g[p][c]['weight']
        rw = g[p][c]['rweight']
        if 'selected' in g[p][c]:
            r += '\t' + genc(p) + ' -> ' + genc(c) + ' [ label="{}\\n({})" color="red" ]'.format(w, rw) + '\n'
        else:
            r += '\t' + genc(p) + ' -> ' + genc(c) + ' [ label="{}\\n({})" ]'.format(w, rw) + '\n'
    r += '}\n'
    return r

def getWord(s, t):
    return s[t[0]:t[1] + 1]

class Scissor:
    '''
    Chinese sentences cutter
    '''
    def __init__(self, wordfreq = {
                '^': 9,
                '$': 9,
                'ab': 1,
                'cd': 2,
                'ef': 3
            }, interword = {
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
            },
            alpha = 1e-20,
            beta = 1e-30,
            theta = 1e-40
            ):
        '''
        Construct a new Scissor class

        :param wordfreq: Dictionary of words' occurence in the corpus
        :param interword: Dictionary of relative frequencies of one word appearing after another in the corpus
        :param alpha: Possibility of a word appearing after another when such a relationship is not found in interword
        :param beta: Possibility of a word appearing after a character
        :param theta: Possibility of a character appearing after a character
        '''
        self.wordfreq = wordfreq
        self.interword = interword
        self.alpha = alpha
        self.beta = beta
        self.theta = theta
    def isChar(self, c):
        return len(c) == 1

    def isWord(self, w):
        return w in self.wordfreq

    def possChar2Char(self, p, c):
        return self.alpha
    def possChar2Word(self, p, c):
        return self.beta

    def possWord2Char(self, p, c):
        return self.beta

    def possWord2Word(self, p, c):
        try:
            return self.interword[p][c]
        except KeyError:
            if self.isWord(p) and self.isWord(c):
                return self.theta
            raise

    def graphGen(self, s, el = None, bl = None):
        '''
        Find every possible routes from the beginning to the end
        '''
        g = nx.DiGraph()
        if el is None:
            el = [[] for _ in s]
        elif isinstance(el, list):
            el.clear()
            el.extend([[] for _ in s])
        if bl is None:
            bl = [[] for _ in s]
        elif isinstance(el, list):
            bl.clear()
            bl.extend([[] for _ in s])
        for i in range(len(s) - 1):
            p = (i, i)
            n = (i + 1, i + 1)
            g.add_edge(p, n)
            bl[i].append(p)
            el[i + 1].append(n)
        for i in range(len(s) - 1):
            for j in range(i + 2, len(s)):
                if s[i:j] in self.wordfreq:
                    n = (i, j - 1)
                    g.add_node(n)
                    el[j - 1].append(n)
                    bl[i].append(n)
                    for p in el[i - 1]:
                        g.add_edge(p, n)
                    if i >= 1:
                        g.add_edge((i - 1, i - 1), n)
                    if j != len(s):
                        g.add_edge(n, (j, j))
        return g

    def graphTag(self, s, g):
        '''
        Add weight to routes
        '''
        for e in sorted(g.edges()):
            p, c = (getWord(s, i) for i in e)
            pn, cn = e
            try:
                w = self.possWord2Word(p, c)
            except KeyError:
                if self.isChar(c):
                    if self.isChar(p):
                        w = self.possChar2Char(p, c)
                    else:
                        w = self.possWord2Char(p, c)
                else:
                    if self.isChar(p):
                        w = self.possChar2Word(p, c)
                    else:
                        wtf
            g[pn][cn]['weight'] = w
        return g

    def detectnum(self, s, g, el, bl):
        '''
        Detect number entity by re
        '''
        re_number = re.compile('[0-9０-９]+|[一-九零〇十百千万]{3,}')
        #re_name = re.compile( '[王李张刘陈杨黄吴赵周徐孙马朱胡林郭何高罗郑梁谢宋唐许邓冯韩曹曾彭肖蔡潘田董袁于余蒋叶杜苏魏程吕丁沈任姚卢钟姜崔谭廖范汪陆金石戴贾韦夏邱方侯邹熊孟秦白江闫薛尹付段雷黎史龙贺陶顾龚郝毛邵万钱严洪赖武傅莫孔汤向常温康施文牛樊葛邢安齐易乔伍庞颜倪庄聂章鲁岳翟申殷詹占欧耿关兰焦俞左柳甘祝包宁符阮尚舒纪柯梅童毕凌单季成霍苗裴涂谷曲盛冉翁蓝骆路游靳辛欧管柴蒙鲍华喻祁房蒲滕萧屈饶解牟艾尤时阳穆农司古吉卓车简连芦缪项麦褚窦娄戚岑党宫景卜费冷晏覃卫习席柏米宗代桂瞿全苟闵佟应臧边卞姬邬和师仇候栾隋刁沙商寇荣巫郎桑丛阎甄敖虞仲池巩明佘查麻苑迟邝封官谈鞠匡惠荆乐冀胥郁南班储原栗燕楚鄢劳谌奚皮蔺楼粟冼盘满闻位厉伊仝区郜海阚花权强帅屠豆朴盖练廉禹井巴漆祖丰支卿国狄平计索宣晋相初门云容敬来扈晁都芮普阙戈浦伏薄鹿邸雍辜阿羊母乌亓裘修邰杭赫况那宿鲜逯印隆茹诸战慕危玉银亢公嵇哈湛宾勾茅戎利扬於呼居干揭但尉斯元束檀衣信阴展昝智幸奉植富衡尧由哀爱昂熬傲奥把百摆拜邦宝保暴北贝贲本闭碧薜别邴伯博补布步部才采彩菜仓苍藏操曽茶产昌苌畅倡唱钞超巢朝潮沉晨呈承赤敕崇瘳丑除楮揣传春淳啜慈次从催翠寸达笪答丹旦淡刀道德迪底第佃定东冬懂钭堵端敦顿多朵鄂恩尔佴法番藩凡芳飞斐风酆逢凤俸扶苻洑浮福甫府复淦刚皋杲格庚弓恭拱贡供缑菇贯冠光广归贵呙虢果过还寒汉行蒿好昊浩禾合河荷黑恒弘红宏鸿后厚忽湖虎户滑化怀淮槐环桓宦皇辉回会火伙基稽及汲戢籍记继暨加佳家嘉郏荚甲菅翦蹇见建剑将降娇矫徼缴教接节杰颉介京经靖静酒咎琚菊巨句具俱剧矍军君俊卡开凯勘堪考科可克空库蒯郐旷奎蒉阔喇稂朗勒蕾类梨礼里理力历立丽励郦莲良粱疗寥列吝泠零另令留庐炉禄伦洛雒闾侣律绿买曼茆卯冒么枚美梦弥糜弭宓秘密妙闽敏名谬磨墨默木沐牧睦纳娜乃铙能尼年念乜钮鸥偶攀泮逄朋蓬澎骈濮溥柒其奇祈耆綦千乾潜羌谯郄钦琴勤青清庆丘秋求渠璩却荛绕仁日融如汝瑞闰润若撒萨赛伞森厦山闪陕善赏上韶卲绍厍莘神甚慎升生绳圣诗拾矢士世侍是释守首寿殳书疏树双水税 顺思松送素眭睢随所锁塔台太泰郯潭塘桃淘腾藤提遆天帖铁通同徒脱陀庹拓完宛旺望威巍伟隗未蔚问瓮沃无毋吾仵兀西希郗息溪袭洗喜霞仙先贤咸线香湘象宵箫潇晓孝校忻星刑兴雄吁须顼绪续轩禤玄学雪寻郇荀牙雅焉延言岩彦艳宴洋仰养样幺侥药要冶野业依仪夷怡宜乙蚁弋义奕羿益裔翼英盈营永勇犹油友有迂鱼宇羽庾遇誉毓员源远院月悦越允运恽载宰迮增甑粘斩长仉掌钊招兆肇折真阵镇征正政只职郅治中忠衷种皱邾珠竹竺主壮禚资子紫訾自字纵俎佐].{1,3}')
        for i in range(0, len(s)):
            num = re_number.match(s[i:])
            if num is not None:
                n = (i, i + num.end() - 1)
                g.add_node(n)
                for p in el[i - 1]:
                    g.add_edge(p, n)
                    g[p][n]['weight'] = 100
                for ne in bl[i + num.end()]:
                    g.add_edge(n, ne)
                    g[n][ne]['weight'] = 1

    def Graph(self, s):
        '''
        Generate weighted graph of routes
        :param s: String of chinese characters to be analysed
        :return: Weighted networkx.DiGraph of routes
        '''
        s = '^' + s + '$'
        el = []
        bl = []
        g = self.graphTag(s, self.graphGen(s, el, bl))
        self.detectnum(s, g, el, bl)
        return g
    
    def Cut(self, s):
        '''
        Cut sentences into lists
        :param s: String of chinese characters to be cut
        :return: List of cutted words
        '''
        g = self.Graph(s)
        for e in g.edges():
            f, t = e
            g[f][t]['weight'] = weightProc(g[f][t]['weight'])
        r = shortest(g, (0, 0), (len(s) + 1, len(s) + 1))
        return [getWord('^' + s + '$', i) for i in r[1:-1]]

if __name__ == '__main__':
    import json
    import lzma
    from subprocess import Popen, PIPE
    s = Scissor(json.loads(lzma.open('wf.json.xz').read().decode('UTF-8')), \
                json.loads(lzma.open('iw.json.xz').read().decode('UTF-8')))
    while True:
        print('Enter: ', end = '')
        v = input()
        d = Popen('dot -Tpng -o g.png', stdin = PIPE, shell = True)
        d.stdin.write(dotGraph(s.Graph(v), v).encode('UTF-8'))
        d.stdin.close()
        d.wait()
        print('Result: ', s.Cut(v))
