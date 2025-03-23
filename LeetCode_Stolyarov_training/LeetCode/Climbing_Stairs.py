import math

class Solution:
    def climbStairs(self, n: int) -> int:
        ways = 1  # Все одинарные шаги
        max_twos = n // 2  # Максимальное количество двойных ступенек

        for k in range(1, max_twos + 1):
            # Количество элементов: n - k (так как каждая двойная ступенька уменьшает общее количество на 1)
            # Количество способов разместить k двойных ступенек среди (n - k) элементов
            ways += math.comb(n - k, k)

        return ways
    
import math
class Solution:
    def climbStairs(self, n: int) -> int:
        ways = 1
        max_twos = math.ceil(n / 2)

        for k in range(1, max_twos):
            ways += math.comb(n - k, k)

        if n%2 == 0:
            ways +=1

        return int(ways)

import math
class Solution:
    def climbStairs(self, n: int) -> int:
        ways = 1
        max_twos = math.ceil(n / 2)

        for k in range(1, max_twos):
            ways += math.factorial(n - k)/(math.factorial(k)*math.factorial(n - 2*k))

        if n%2 == 0:
            ways +=1

        return int(ways)
    
class Solution:

    def __init__(self):
        self.ns = {1: 1, 2: 2}

    def climbStairs(self, n: int) -> int:
        if n not in self.ns:
            self.ns[n] = self.climbStairs(n-1) + self.climbStairs(n-2)
        return self.ns[n]
    