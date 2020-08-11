from itertools import combinations
from math import gcd as _gcd

def solution(skills):
    H = 1e140
    gcd = _gcd

    def F(a,b,simplify=True):
        if simplify:
            g=gcd(a,b)
            if g>1:
                a//=g
                b//=g
        return (a,b)

    def addto(n1d1,n2d2):
        n1,d1 = n1d1
        n2,d2 = n2d2
        n = n1*d2+d1*n2
        d = d1*d2
        if d>H:
            g = gcd(n,d)
            return (n//g,d//g)
        else:
            return (n,d)

    def mul(n1d1,n2d2):
        n1,d1 = n1d1
        n2,d2 = n2d2
        return (n1*n2,d1*d2)

    def mul3(n1d1,n2d2,n3d3):
        n1,d1 = n1d1
        n2,d2 = n2d2
        n3,d3 = n3d3
        n = n1*n2*n3
        d = d1*d2*d3
        g = gcd(n,d)
        n//=g
        d//=g
        return (n,d)

    def addlist(liste):
        while len(liste) > 1:
            liste = [addto(liste[i], liste[i+1]) for i in range(0, len(liste)-1, 2)] + ([liste[-1]] if len(liste)&1 else [])
        return liste[0]

    def solution4(skills, ref=0):
        skillskeys = [k[0] for k in skills]
        skillsvalues = [k[1] for k in skills]
        if skills[0][0] == 0:
            s,b,c,d = skillsvalues
            den = (s+b)*(s+c)*(s+d)*(b+c)*(b+d)*(c+d)
            num = s*s*(
                (b+d)*(c+d)*(b*(s+c)+c*(s+b))+\
                (c+b)*(d+b)*(c*(s+d)+d*(s+c))+\
                (d+c)*(b+c)*(d*(s+b)+b*(s+d))
            )
            return ((ref, F(num,den)),)
        players = skillskeys
        s,b,c,d = skillsvalues
        l=[None]*4
        for i in range(4):
            den = (s+b)*(s+c)*(s+d)*(b+c)*(b+d)*(c+d)
            num = s*s*(
                (b+d)*(c+d)*(b*(s+c)+c*(s+b))+\
                (c+b)*(d+b)*(c*(s+d)+d*(s+c))+\
                (d+c)*(b+c)*(d*(s+b)+b*(s+d))
            )
            l[i] = (players[i], F(num,den))
            s,b,c,d = b,c,d,s
        return l

    keylist = list(skills.keys())
    keylist.remove("Andy")
    keylist.insert(0, "Andy")
    skills = [(keylist.index(i),s) for i,s in skills.items()]
    proba1v1 = [F(sa,sa+sb) for _,sa in skills for _,sb in skills]
    if len(skills) == 2:
        num, den = skills[0][1], skills[0][1]+skills[1][1]
    elif len(skills) == 4:
        _,f = solution4(skills,0)[0]
        num, den = f[0], f[1] * 3
    elif len(skills) == 8:
        four = {}
        ans = F(0,1,False)
        for combi4 in combinations(skills, 4):
            sol1 = solution4(combi4,0)
            four[combi4] = sol1
            othcombi = tuple((p,s) for p,s in skills if (p,s) not in combi4)
            if othcombi in four:
                sol2 = four[othcombi]
                if sol1[0][0]==0:
                    _, p_Andy_in_semis = sol1[0]
                    for winner2, p_win in sol2:
                        ans = addto(ans,mul3(p_Andy_in_semis,p_win,proba1v1[0*8+winner2]))
                else:
                    _, p_Andy_in_semis = sol2[0]
                    for winner1, p_win in sol1:
                        ans = addto(ans, mul3(p_Andy_in_semis,p_win,proba1v1[0*8+winner1]))
        num, den = ans[0], ans[1]*315

    else:
        players = tuple(range(16))
        group = [None]*(2**16)
        pow2 = 2**16
        for combi4 in combinations(skills, 4):
            sol1 = solution4(combi4,0)
            combi4 = sum(1<<i for i,_ in combi4)
            group[combi4] = sol1
        ans = (0,1)
        for combi8 in combinations(players, 8):
            # In order: those containing 0, then the others
            combi8bin = sum(1<<i for i in combi8)
            if combi8[0] == 0:
                ans8 = (0,1)
                ans8list = []
                for combi4 in combinations(combi8[1:], 4):
                    combi4bin = sum(1<<i for i in combi4)
                    othcombi4bin = combi8bin-combi4bin
                    sol1 = group[combi4bin]
                    sol2 = group[othcombi4bin]
                    tmp = mul(sol1[0][1], proba1v1[sol1[0][0]])
                    _, p_Andy_in_quarters = sol2[0]
                    for winner1, p_win in sol1[1:]:
                        tmp = addto(tmp, mul(p_win,proba1v1[winner1]))
                    #ans8 = addto(ans8,mul(p_Andy_in_quarters,tmp))
                    ans8list.append(mul(p_Andy_in_quarters,tmp))
                ans8 = addlist(ans8list)
                group[combi8bin] = ans8
            else:
                eightcombi8 = [(0,1) for i in range(16)]
                for combi4 in combinations(combi8[1:], 4):
                    combi4bin = sum(1<<i for i in combi4)
                    othcombi4bin = combi8bin-combi4bin
                    sol1 = group[combi4bin]
                    sol2 = group[othcombi4bin]
                    for winner1, p_1_in_quarters in sol1:
                        for winner2, p_2_in_quarters in sol2:
                            p_fight = mul(p_1_in_quarters,p_2_in_quarters)
                            eightcombi8[winner1] = addto(eightcombi8[winner1], mul(p_fight, proba1v1[winner1*16+winner2]))
                            eightcombi8[winner2] = addto(eightcombi8[winner2], mul(p_fight, proba1v1[winner2*16+winner1]))
                #group[combi8bin] = tuple((i,eightcombi8[i]) for i in combi8)

                # at that point, the probabilities from the other half has already been computed
                othcombi8bin = pow2-1-combi8bin
                tmp = mul(eightcombi8[combi8[0]],proba1v1[combi8[0]])
                p_Andy_in_semis = group[othcombi8bin]
                for winner1 in combi8[1:]:#winner1, p_win in sol1:
                    p_win = eightcombi8[winner1]
                    tmp = addto(tmp, mul(p_win,proba1v1[winner1]))
                ans = addto(ans, mul(p_Andy_in_semis,tmp))
        num, den = ans[0], ans[1]*638512875
    g=gcd(num,den)
    den//=g
    num//=g
    return str(num)+str(den)


if __name__ == "__main__":
    from time import time
    t=time()
    skills = {'Andy': 7, 'Novak': 5, 'Roger': 3, 'Rafael': 2}
    print(solution(skills))
    skills = {'Andy':1,'B':1,'C':1,'D':1,'E':1,'F':1,'G':1,'H':1}
    print(solution(skills))
    skills = {'Andy':17,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,
                'I':9,'J':10,'K':11,'L':12,'M':13,'N':14,'O':15,'P':16}
    #skills = {'Andy':1,'B':1,'C':1,'D':1,'E':1,'F':1,'G':1,'H':1,
    #            'I':1,'J':1,'K':1,'L':1,'M':1,'N':1,'O':1,'P':1}
    print(solution(skills)) #1236537281162390587362321632635564988951942276721777816919943758579701083165235678318549178599103679510240782691103542286152515885679716555619918191090640337203200000000000000000
    print(time()-t)