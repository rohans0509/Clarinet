def distance(s1:str,s2:str):
    m = len(s1)
    n = len(s2)
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])
    return dp[m][n]


def similarity(query:str,data:str,stride_length=0):

    query_len=len(query)
    data_len=len(data)

    if stride_length not in range(1,query_len+1):
        stride_length=1

    s1=query

    score=float("inf")

    start=-1
    end=-1

    while end<data_len:
        start=start+stride_length
        end=min(start+query_len,data_len)

        s2=data[start:end]
        

        edit_distance=distance(s1,s2)
        if edit_distance<score:
            score=edit_distance

    sim=1-score/query_len
    
    return(sim)