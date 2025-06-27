from typing import List


class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:

        stack = []

        for a in asteroids:
            while True:
                if not stack or a > 0 or stack[-1] < 0:
                    stack.append(a)
                    break
                elif stack[-1] > abs(a):
                    break
                elif stack[-1] < abs(a):
                    stack.pop()
                elif stack[-1] == abs(a):
                    stack.pop()
                    break

        return stack
