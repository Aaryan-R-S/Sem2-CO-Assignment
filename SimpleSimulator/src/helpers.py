def dec_to_bin(x, l):
    t = bin(x)
    t = t[2:]
    t = t[-l:]
    if(len(t)!=l):
        t = '0'*(l-len(t))+t
    return t

