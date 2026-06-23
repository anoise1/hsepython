from itertools import permutations
print('\n'.join([''.join(list(map(str,i))) for i in permutations([j for j in range(1, int(input()) + 1)])]))