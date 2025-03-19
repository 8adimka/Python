# Two Sum

# Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

# You may assume that each input would have exactly one solution, and you may not use the same element twice.
# You can return the answer in any order.

# Example 1:

# Input: nums = [2,7,11,15], target = 9
# Output: [0,1]
# Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
# Example 2:

# Input: nums = [3,2,4], target = 6
# Output: [1,2]
# Example 3:

# Input: nums = [3,3], target = 6
# Output: [0,1]
 
# Only one valid answer exists.

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        indx1 = 0
        indx2 = 0
        while indx1 < len(nums):
            if indx1 != indx2 and nums[indx1]+nums[indx2] == target:
                return [indx1, indx2]
            indx2 += 1
            if indx2 == len(nums):
                indx2 = 0
                indx1 += 1

# Runtime
# 9079ms
# Beats 5.00%

# Memory
# 18.06MB
# Beats 99.66%

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            contr = target - nums[i]
            if contr in nums and nums.index(contr) != i:
                return [i, nums.index(contr)]
