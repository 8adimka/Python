# Write an algorithm to determine if a number n is happy.

# A happy number is a number defined by the following process:

# Starting with any positive integer, replace the number by the sum of the squares of its digits.
# Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
# Those numbers for which this process ends in 1 are happy.
# Return true if n is a happy number, and false if not.

class Solution:
    def isHappy(self, n: int) -> bool:
        used_nums = []
        while n != 1:
            nums_sq = list(map(lambda x: int(x)**2, str(n)))
            n = sum(nums_sq)
            if n in used_nums:
                return False
            used_nums.append(n)
        return True                
        
sol = Solution()

print(sol.isHappy(19))
print(sol.isHappy(2))

