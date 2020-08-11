from math import log2
def special_solution(a,m):
    #m = 2**n-1
    n = len(bin(m))-2
    ans = 0
    for aa in a:
        ans += pow(2,aa%n)
    return ans%m

def solution(a, m):

    if all(i=='1' for i in bin(m)[2:]):
        return special_solution(a,m)
    def expo(q):
        res,exp=1,q
        exp=bin(exp)
        i=0
        for j in range(len(exp)-1, 1, -1):
            if exp[j]=='1': res=aux[i]*res%m
            i+=1
            #exp>>=1
        return res
    phim = m-1
    a = sorted([aa%phim for aa in a+[0]])
    maxa = max(a)
    sup = int(log2(maxa))+1
    aux = [2]
    for _ in range(sup):
        aux.append(aux[-1]*aux[-1]%m)
    ans = 0
    for j in range(len(a)-1, 0, -1):
        ans += 1
        ans = ans*expo(a[j]-a[j-1])%m
    return ans
