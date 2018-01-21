from full import fullfunc

def get_index(target):
    index = []
    s = 0
    for i in target:
        s += len(i)
        index.append(s)
    return index

def calculate(mine_str):
    # calculate the result
    print("begin to caluculating ... ") 
    with open('3.txt',encoding='utf8') as f:
        content = f.read()
        res = content.split()
    # res is the split result
    # mine split result
    mine_res = mine_str.split()
    
    res1 = set(get_index(res))
    res2 = set(get_index(mine_res))
    
    res = res1 & res2
    P = round(len(res) / len(res2), 4)
    R = round(len(res) / len(res1), 4)
    return P, R

if __name__ == "__main__":
    f = fullfunc()
    r = ''
    with open('4.txt', 'r', encoding = 'utf8') as p:
        for line in p:
            r = r + ' '.join(f.func(line))
    mine_str = r
    print(r)
    print(calculate(mine_str))
