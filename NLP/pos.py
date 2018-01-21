#!/usr/bin/env python3

# Word freq

import json

def main():
    ipos = {}
    def addpos(p, n):
        if not p in ipos:
            ipos[p] = {}
        if not n in ipos[p]:
            ipos[p][n] = 0
        ipos[p][n] += 1
    try:
        while True:
            l = input()
            wl = l.split()
            pw = 'w'
            for w in wl:
                try:
                    w = w.split('/')[-1]
                except IndexError:
                    print('err: `' + l + '`')
                    print('at: ' + w)
                    raise
                    continue
                addpos(pw, w)
                pw = w
    except EOFError:
        pass
    json.dump(ipos['w'], open('bposc.json', 'w'), indent=4)
    json.dump(ipos, open('iposc.json', 'w'), indent=4)
    for p in ipos:
        s = 0
        for w in ipos[p]:
            s += ipos[p][w]
        for w in ipos[p]:
            ipos[p][w] /= s
    json.dump(ipos['w'], open('bposf.json', 'w'), indent=4)
    json.dump(ipos, open('iposf.json', 'w'), indent=4)

main()
