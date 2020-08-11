def solution(ps):
    inf = 1_000_000_000

    dp = [[(5,5)] for _ in range(len(ps[0]))]
    
    for i in range(1, len(ps)):
        p = ps[i]
        pm = ps[i-1]
        pmdic = {pm[i]:i for i in range(len(pm))}
        newdp = []
        reachable = []
        mindeb = 0
        for hp in p:
            hp_reachable = False
            newdpi = [inf]*11
            for hm in [hp-5,hp-4,hp-3,hp-2,hp-1]:
                if hm not in pmdic: continue
                jm = pmdic[hm]
                hp_reachable = True
                for pacejm,record in dp[jm]:
                    pacej = pacejm + (pacejm < 10)
                    other = record + pacej
                    if newdpi[pacej] > other:
                        newdpi[pacej] = other
            #hm = hp
            if hp in pmdic:
                jm = pmdic[hp]
                hp_reachable = True
                for pacejm,record in dp[jm]:
                    other = record + pacejm
                    if newdpi[pacejm] > other:
                        newdpi[pacejm] = other
            for hm in [hp+1,hp+2,hp+3,hp+4,hp+5]:
                if hm not in pmdic: continue
                jm = pmdic[hm]
                hp_reachable = True
                for pacejm,record in dp[jm]:
                    pacej = pacejm - (pacejm>1)
                    other = record + pacej
                    if newdpi[pacej] > other:
                        newdpi[pacej] = other
            if hp_reachable:
                reachable.append(hp)
                compressed = []
                rec = inf
                for pacej in range(1,11):
                    if newdpi[pacej] < rec:
                        rec = newdpi[pacej]
                        compressed.append((pacej,rec))
                newdp.append(compressed)
        ps[i] = reachable
        dp = newdp

    return min(min(dpii[1] for dpii in dpi) for dpi in dp)

if __name__ == "__main__":
    import pickle
    with open("sl_hardcore_parkour.pkl", "rb") as f:
        ps=pickle.load(f)[0]
    print(ps)
    print(solution(ps))