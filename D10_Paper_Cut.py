from math import gcd

def bezout(a,b): #au+bv=d
    r=max(a,b)
    rr=min(a,b)
    u,v,uu,vv=1,0,0,1
    while rr>0.5:
        q=r//rr
        rr,r=r%rr,rr
        uu,u=u-q*uu,uu
        vv,v=v-q*vv,vv
    if a>b:
        return (u,v)
    return (v,u)
    
def ok(a,b,c,d):
    # notice the inversion a,b <-> c,d
    # here it's c*d dominoes inside a a*b rectangle
    g = gcd(c,d)
    if a%g or b%g: return 0
    ag = a//g
    bg = b//g
    cg = c//g
    dg = d//g
    if (a*b)%(c*d): return 0
    u,v = bezout(c,d)
    assert c*u+d*v == g
    ua, va = u*ag, v*ag
    if ua < 0:
        diff = (ua%dg) - ua
        ua = ua + diff
        va = va - diff//dg*cg
        assert c*ua+d*va == a
        if va <0: return 0
    elif va < 0:
        diff = (va%cg) - va
        va = va + diff
        ua = ua - diff//cg*dg
        assert c*ua+d*va == a
        if ua <0: return 0
    ub, vb = u*bg, v*bg
    if ub < 0:
        diff = (ub%dg) - ub
        ub = ub + diff
        vb = vb - diff//dg*cg
        assert c*ub+d*vb == b
        if vb <0: return 0
    if vb < 0:
        diff = (vb%cg) - vb
        vb = vb + diff
        ub = ub - diff//cg*dg
        assert c*ub+d*vb == b
        if ub <0: return 0

    if a%c and b%c: return 0
    if a%d and b%d: return 0
    return 1

def solution(qs):
    ans = 0
    mod=10**9+7
    for i in range(len(qs)):
        a,b,c,d = qs[i]
        if ok(c,d,a,b):
            ans+=pow(2,i,mod)
    ans %= mod
    return ans
    