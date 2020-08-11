def solution(a, b):
    a = [ord(c)-79>>1 for c in reversed(a)]
    b = [ord(c)-79>>1 for c in reversed(b)]
    for aa,bb in zip(a,b):
        d = aa - bb
        if d==0:
            a.append(aa)
            b.append(bb)
        elif d*(d-1)==2:
            a.append(bb)
            a.append(aa)
        else:
            b.append(aa)
            b.append(bb)
    return min(len(a),len(b))

if __name__ == "__main__":
    import pickle
    with open("sl_roshambolic.pkl", "rb") as f:
        a, b = pickle.load(f)
        a, b = "SRRRPSSPRPRPSS","PPSPSSPRSPRPRR"
    from time import time
    t=time()
    print(solution(a,b))
    print("time", time()-t)