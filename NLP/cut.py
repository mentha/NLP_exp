#!/usr/bin/env python3

import networkx as nx
import math

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
    def graphGen(self, s):
        '''
        Find every possible routes from the beginning to the end
        '''
        g = nx.DiGraph()
        for i in range(len(s) - 1):
            g.add_edge((i, i), (i + 1, i + 1))
        c = [[] for _ in s]
        for i in range(len(s) - 1):
            for j in range(i + 2, len(s)):
                if s[i:j] in self.wordfreq:
                    n = (i, j - 1)
                    g.add_node(n)
                    c[j - 1].append(n)
                    for p in c[i - 1]:
                        if True or getWord(s, p) in self.interword and \
                                getWord(s, n) in self.interword[getWord(s, p)]:
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
    def Graph(self, s):
        '''
        Generate weighted graph of routes
        :param s: String of chinese characters to be analysed

        :return: Weighted networkx.DiGraph of routes
        '''
        s = '^' + s + '$'
        return self.graphTag(s, self.graphGen(s))
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
    from subprocess import Popen, PIPE
    s = Scissor(json.load(open('wf.json')), json.load(open('iw.json')))
    while True:
        print('Enter: ', end = '')
        v = input()
        d = Popen('dot -Tpng -o g.png', stdin = PIPE, shell = True)
        d.stdin.write(dotGraph(s.Graph(v), v).encode('UTF-8'))
        d.stdin.close()
        d.wait()
        print('Result: ', s.Cut(v))