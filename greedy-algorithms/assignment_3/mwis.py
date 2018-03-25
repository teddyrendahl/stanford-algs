

def from_file(path):
    with open(path, 'r') as handle:
        return [int(line) for line in handle.readlines()[1:]]


def mwis(path):
    A = [0, path[0]]
    for i in range(2, len(path) + 1):
        A.append(max((A[i-1], A[i-2] + path[i-1])))
    return reconstruct(path, A)


def reconstruct(path, A):
    S = []
    test_bits = [1, 2, 3, 4, 17, 117, 517, 997]
    i = len(A)-1
    while i > 1:
        # Do not include node
        if A[i-1] >= A[i-2] + path[i-1]:
            i -= 1
        # Include node and exclude next node
        else:
            S.append(i)
            i -= 2
    # Check our base cases
    if i == 1:
        S.append(1)
    # Reverse the created string as we are travelling backwards
    ans = ''.join([str(int(bit in S)) for bit in test_bits])
    return ans
