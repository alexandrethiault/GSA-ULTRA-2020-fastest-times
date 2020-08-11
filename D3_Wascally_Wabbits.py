from math import gcd as _gcd
from heapq import *

def solution(wabbits, numerator, denominator):

    gcd = _gcd

    g = gcd(numerator, denominator)
    numerator//=g
    denominator//=g
    powden = [denominator**i for i in range(400)]
    H = 1e100
    H2 = 1e25
    H3 = 1e125
    H4 = 1e75
    H5 = 1e300
    # Fraction = (num, simplified den, pow denominator in den, pow 2 in den)
    def add(n1d1,n2d2,simplify=True):
        n1,d1,p1,t1 = n1d1
        n2,d2,p2,t2 = n2d2
        if p1<p2:
            if (p2-p1) < 400:
                n1 *= powden[p2-p1]
            else:
                n1 *= denominator**(p2-p1)
            p1 = p2
        elif p2<p1:
            if (p1-p2) < 400:
                n2 *= powden[p1-p2]
            else:
                n2 *= denominator**(p1-p2)
            p2 = p1
        if t1<t2:
            n1 <<= t2-t1
            t1 = t2
        elif t2<t1:
            n2 <<= t1-t2
            t2 = t1
        n = n1*d2+d1*n2
        d = d1*d2
        if simplify and d>H2:
            g = gcd(n,d)
            return (n//g,d//g, p1, t1)
        else:
            return (n,d, p1, t1)

    def add3(liste, simplify=True):
        return add(add(liste[0], liste[1], False), liste[2], simplify)

    def mul(n1d1,n2d2, simplify = False):
        n1,d1,p1,t1 = n1d1
        n2,d2,p2,t2 = n2d2
        n = n1*n2
        d = d1*d2
        p = p1+p2
        t = t1+t2
        if simplify and d>H4:
            g = gcd(n,d)
            n//=g
            d//=g
        return (n,d, p, t)

    def div(n1d1, n2d2, simplify=True):
        n1,d1,p1,t1 = n1d1
        n2,d2,p2,t2 = n2d2
        n = n1*d2
        d = d1*n2
        p = p1-p2
        t = t1-t2
        return (n,d, p, t)

    def muldiv(n1d1, n2d2, n3d3, simplify=True):
        n1,d1,p1,t1 = n1d1
        n2,d2,p2,t2 = n2d2
        n3,d3,p3,t3 = n3d3
        n = n1*n2*d3
        d = d1*d2*n3
        p = p1+p2-p3
        t = t1+t2-t3
        if simplify and d>H3:
            g = gcd(n,d)
            n//=g
            d//=g
        return (n,d, p, t)

    def simplified(n1d1, hard=True):
        n,d,p,t = n1d1
        g = gcd(n,d)
        n, d = n//g, d//g
        if hard and n!=0:
            nd, m = divmod(n, denominator)
            while m==0:
                n = nd
                nd, m = divmod(n, denominator)
                p-=1
            nd, m = divmod(n, 2)
            while m==0:
                n = nd
                nd, m = divmod(n, 2)
                t-=1
        return (n, d, p, t)

    def heapsum(liste):
        if len(liste)<=2:
            if len(liste)==1: return liste[0]
            else: return add(liste[0], liste[1])
        liste = [(c[1],c) for c in liste]
        heapify(liste)
        for _ in range(len(liste)-1):
            c = add(heappop(liste)[1],heappop(liste)[1], (_&15)==15)
            heappush(liste, (c[1], c))
        return liste[0][1]

    p = (numerator, 1, 1, 0)
    q = (denominator - numerator, 1, 1, 0)

    pp = simplified(mul(p,p))
    qq = simplified(mul(q,q))
    pq = simplified(mul(p,q))
    pq2 = (pq[0], pq[1], pq[2], pq[3]-1)
    N = len(wabbits)

    transition = [[None]*3 for _ in range(4)]

    transition[0][0] = qq
    transition[0][1] = pq2
    transition[0][2] = pp

    transition[1][0] = pq
    transition[1][1] = simplified(add(pp,qq))
    transition[1][2] = pq

    transition[2][0] = pp
    transition[2][1] = pq2
    transition[2][2] = qq

    transition[3][0] = (1,1, 0, 2)
    transition[3][1] = (1,1, 0, 1)
    transition[3][2] = (1,1, 0, 2)


    # RR = 0, Rg = 1, gg = 2

    def compatible(v, g):
        if v == 'G':
            return g == 2
        elif v == 'R':
            return g < 2
        else:
            return True

    val = ['?']*(2*N)
    pere = [-1]*(2*N)
    fils = [[] for _ in range(2*N)]

    down = [[None]*3 for _ in range(2*N)]
    up_x_down = [[None]*3 for _ in range(2*N)]
    memTotFils = [[None]*3 for _ in range(2*N)]
    
    # divide the tree by splitting it along the nonzero green wabbits

    greens = []

    for i in range(N):
        pere[i] = wabbits[i][0]
        val[i] = wabbits[i][1]
        if i and val[i] == 'G':
            greens.append(i)
            fils[pere[i]].append(N+i)
            val[N+i] = 'G'
            pere[N+i] = pere[i]
            pere[i] = -1
        elif i:
            fils[pere[i]].append(i)

    unknowns = val[:N].count('?')
    if unknowns == N:
        n = N
        d = 4
        g = gcd(n, d)
        n//=g
        d//=g
        return f"{n}{d}"

    bigreslist = []
    #bigres = (0,1, 0, 0)
    for u,deb in enumerate([0]+greens):

        ordre_bfs = [deb]
        i=0
        while i < len(ordre_bfs):
            for j in fils[ordre_bfs[i]]:
                ordre_bfs.append(j)
            i += 1

        res = (0,1, 0, 0)
        for cur in reversed(ordre_bfs):
            #calc_down(cur)
            for gene in range(3):
                if not compatible(val[cur], gene):
                    down[cur][gene] = (0,1, 0, 0)
                    continue
                down[cur][gene] = (1,1, 0, 0)
                mulcount = 1
                for f in fils[cur]:
                    totFils = simplified(add3([mul(transition[gene][geneFils], down[f][geneFils]) for geneFils in range(3)]))
                    memTotFils[f][gene] = totFils
                    down[cur][gene] = mul(down[cur][gene], totFils)
                    mulcount += 1
                    if (mulcount & 7) == 0 and down[cur][gene][0] > H:
                        down[cur][gene] = simplified(down[cur][gene], False)
                down[cur][gene] = simplified(down[cur][gene])

        def calc_up(cur):
            if all(i is not None for i in up_x_down[cur]):
                return
            elif pere[cur] == -1:
                up_x_down[cur] = down[cur]
                return
            else:
                calc_up(pere[cur])
                up_x_down_div_totFils = [None]*3
                for gene in range(3):
                    up = (0,1, 0, 0)
                    if not compatible(val[cur], gene):
                        up_x_down[cur][gene] = (0,1,0,0)
                        continue
                    for genePere in range(3):
                        if up_x_down[pere[cur]][genePere][0] == 0: continue
                        #totFils = memTotFils[cur][genePere]
                        if up_x_down_div_totFils[genePere] is None:
                            up_x_down_div_totFils[genePere] =\
                                div(up_x_down[pere[cur]][genePere],
                                    memTotFils[cur][genePere])
                        up = add(up,
                            mul(transition[gene][genePere],
                            up_x_down_div_totFils[genePere])
                        )


                    up_x_down[cur][gene] = mul(up, down[cur][gene], len(fils[cur])>3)

        for cur in ordre_bfs:
            if val[cur] == '?':
                _ex = cur
                calc_up(cur)
                res = add(res, up_x_down[cur][2], True) #ca coute tres peu j'ai verifie

        tot = add3([mul(up_x_down[_ex][gene], transition[3][gene]) for gene in range(3)], True)
        res = simplified(muldiv(res, transition[3][2], tot,False))

        #results.append(res)
        bigreslist.append(res)
        #bigres = add(bigres, res, u&7==7)#u&15==15)
    #print(bigres[0]/bigres[1])
    bigres = heapsum(bigreslist)
    n, d, p, t = bigres
    if p>0:
        d *= denominator ** p
    elif p<0:
        n *= denominator ** (-p)
    if t>0:
        d <<= t
    elif t<0:
        n <<= (-t)
    #n -= d*len(greens)
    n += d*(len(greens) + (val[0] == 'G'))
    g = gcd(n,d)
    n//=g
    d//=g
    return f"{n}{d}"


if __name__ == "__main__":
    import pickle
    with open("sl_wascally_wabbits.pkl", "rb") as f:
        wabbits, p_numerator, p_denominator=pickle.load(f)
    wabbits = [(-1, 'R'), (0, 'G'), (0, '?'), (0, 'R'), (1, 'R'), (1, '?'), (1, 'G'), (2, 'G'), (3, '?')] # 134313175
    #wabbits = [(-1, 'R'), (0, '?'), (1, '?'), (2, '?'), (3, '?'), (4, '?'), (5, '?'), (4, '?')]
    print(wabbits, p_numerator, p_denominator)
    print(solution(wabbits, p_numerator, p_denominator), "134313175")#"32275")
