def solution(targets):
    intervals = []
    for center, height in targets:
        intervals.append((center-height, center+height))
    intervals.sort()
    end=beg=-20000

    ans = 0
    for i in range(len(intervals)):
        if intervals[i][0] > end:
            ans += (end-beg)
            beg = intervals[i][0]
            end = intervals[i][1]
        else:
            end = max(end, intervals[i][1])
    ans += end-beg
    return ans//2