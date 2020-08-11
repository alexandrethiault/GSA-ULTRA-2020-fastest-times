# A solution with understandable code
def solution_(a, b):
    inf = 2000000001
    dp0 = [[None]*(len(b)+1) for _ in range(len(a)+1)]
    dp1 = [[None]*(len(b)+1) for _ in range(len(a)+1)]
    dp0[0][0] = 0
    dp0[1][0] = dp0[0][0] + a[0]
    dp0[0][1] = inf
    dp1[0][0] = 0
    dp1[1][0] = inf
    dp1[0][1] = dp1[0][0] + b[0]
    for i in range(1, len(a)):
        dp0[i+1][0] = dp0[i][0] + abs(a[i]-a[i-1])
        dp1[i+1][0] = inf
    for j in range(1, len(b)):
        dp0[0][j+1] = inf
        dp1[0][j+1] = dp1[0][j] + abs(b[j]-b[j-1])
    for i in range(len(a)):
        for j in range(len(b)):
            dp0[i+1][j+1] = min(
                dp0[i][j+1] + abs(a[i]-a[i-1]),
                dp1[i][j+1] + abs(a[i]-b[j])
            )
            dp1[i+1][j+1] = min(
                dp0[i+1][j] + abs(b[j]-a[i]),
                dp1[i+1][j] + abs(b[j]-b[j-1])
            )
    return min(dp0[len(a)][len(b)], dp1[len(a)][len(b)])

# The same solution but optimized
def solution(a, b):
    _abs = abs
    inf = 2000000001
    dp0 = [None]*(len(b)+1)
    dp1 = [None]*(len(b)+1)
    dp0[0] = 0
    dp0[1] = inf
    dp1[0] = 0
    dp1[1] = dp1[0] + b[0]
    diffa = [_abs(a[i]-a[i-1]) for i in range(len(a))]
    diffb = [_abs(b[i]-b[i-1]) for i in range(len(b))]
    for j in range(1, len(b)):
        dp0[j+1] = inf
        dp1[j+1] = dp1[j] + diffb[j]
    B = list(range(len(b)))
    for i in range(len(a)):
        diffai = diffa[i]
        ai = a[i]
        if i==0:
            dp0[0] += ai
            dp1[0] = inf
        else:
            dp0[0] += diffai
        for j,bj in enumerate(b):
            absdif = bj-ai
            if absdif < 0: absdif *= -1
            dp0[j+1] += diffai
            other = dp1[j+1] + absdif
            if dp0[j+1] > other:
                dp0[j+1] = other
            dp1[j+1] = dp0[j] + absdif
            other = dp1[j] + diffb[j]
            if dp1[j+1] > other:
                dp1[j+1] = other
    return min(dp0[len(b)], dp1[len(b)])
    