

def max_permutations(M):
    res = set()
    def backtrack(i):
        #feil plass og neste er på feil plass
        if i != M[i] and M[M[i]] != M[M[M[i]]]:
            temp = M[M[i]]
            M[M[i]] = M[i]
            backtrack(temp)
            if temp != M[temp]:
                M[M[i]] = temp
            else:
                res.add(M[i])
    for i in range(len(M)):
        backtrack(i)
    return res

print(max_permutations([1,0]))