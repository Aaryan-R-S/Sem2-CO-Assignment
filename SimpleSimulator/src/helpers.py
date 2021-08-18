def dec_to_bin(x, l):
    t = bin(x)
    t = t[2:]
    t = t[-l:]
    if(len(t)!=l):
        t = '0'*(l-len(t))+t
    return t

def bin_to_dec(s):
    ans=0
    power=0
    for i in range(len(s)-1,-1,-1):
        ans+=(1<<power)*int(s[i])
        power+=1
    return(ans)

