#!/usr/bin/env python3

# Word freq

import json

def main():
    iw = {}
    def addiw(p, n):
        if p == '。':
            p = '^'
        if n == '。':
            n = '$'
        if not p in iw:
            iw[p] = {}
        if not n in iw[p]:
            iw[p][n] = 0
        iw[p][n] += 1
    try:
        while True:
            l = input()
            wl = l.split()
            pw = '^'
            for w in wl:
                w = '/'.join(w.split('/')[:-1])
                addiw(pw, w)
                pw = w
            addiw(pw, '$')
    except EOFError:
        pass
    json.dump(iw, open('iwc.json', 'w'), indent=4)
    for p in iw:
        s = 0
        for w in iw[p]:
            s += iw[p][w]
        for w in iw[p]:
            iw[p][w] /= s
    json.dump(iw, open('iw.json', 'w'), indent=4)

main()
