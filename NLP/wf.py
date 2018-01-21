#!/usr/bin/env python3

# Word freq

import json

def main():
    wf = {}
    try:
        while True:
            l = input()
            wl = l.split()
            for w in wl:
                w = '/'.join(w.split('/')[:-1])
                if not w in wf:
                    wf[w] = 0
                wf[w] += 1
    except EOFError:
        pass
    json.dump(wf, open('wf.json', 'w'), indent=4)

main()
