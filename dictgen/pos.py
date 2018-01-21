#!/usr/bin/env python3

# Part Of Speech freq

import json

def main():
    ipos = {}
    pos = {}
    def addpos(p, n):
        'Add pos pair to dict ipos'
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
                wf = None
                try:
                    wf = '/'.join(w.split('/')[:-1])
                    w = w.split('/')[-1]
                except IndexError:
                    # detect malformed input
                    print('err: `' + l + '`')
                    print('at: ' + w)
                    raise
                    continue
                addpos(pw, w)
                if not wf in pos:
                    pos[wf] = set()
                pos[wf].add(w)
                pw = w
    except EOFError:
        pass
    for e in pos:
        pos[e] = list(pos[e])
    json.dump(pos, open('pos.json', 'w'), indent=4)
    json.dump(ipos['w'], open('bposc.json', 'w'), indent=4)
    json.dump(ipos, open('iposc.json', 'w'), indent=4)
    for p in ipos:
        # normalize
        s = 0
        for w in ipos[p]:
            s += ipos[p][w]
        for w in ipos[p]:
            ipos[p][w] /= s
    json.dump(ipos['w'], open('bposf.json', 'w'), indent=4)
    json.dump(ipos, open('iposf.json', 'w'), indent=4)

main()
