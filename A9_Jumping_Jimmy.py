def solution(a, qs):

    pow2 = 1
    while pow2 < len(a):
        pow2 *= 2
        
    tab = [0]*(pow2*2)
    tab[pow2:pow2+len(a)] = a[:]
    size = pow2
    for i in range(pow2-1, 0, -1):
        tab[i] = max(tab[2*i], tab[2*i+1])

    def query(i, j, sd=0, se=size-1, tabindex=1):
        if i<=sd and se<j:
            return tab[tabindex]
        if sd>=j or se<i:
            return 0
        sm = sd+se>>1
        return max(
            query(i,j,sd,sm,tabindex*2),
            query(i,j,sm+1,se,tabindex*2+1)
        )
        
    ans = 0
    sa = sorted([(a[i],i) for i in range(len(a))])
    for i,j in qs:
        for k in range(-1, -min(100, len(a)), -1):
            if i<=sa[k][1]<j:
                ans += sa[k][0]
                break
        else:
            ans += query(i,j)
    return ans

if __name__ == "__main__":
    import pickle
    with open("sl_jumping_jimmy.pkl", "rb") as f:
        a, qs = pickle.load(f)
        a = [3, 6, 6, 1, 9, 8, 4, 7, 1, 1]
        qs = [(1, 7), (5, 7), (0, 1)]
    print(a, qs)
    from time import time
    t=time()
    print(solution(a, qs))
    print("time", time()-t)