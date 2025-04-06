# Given an integer array nums and an integer k,
# return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k.

from typing import List


class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        seen = {}
        for i, num in enumerate(nums):
            if num in seen and i - seen[num] <= k:
                return True
            seen[num] = i
        return False
    
# # Window_Solution
# class Solution:
#     def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
#         for i in range(len(nums)):
#             start = max (0, i-k)
#             end = min (i+k+1, len(nums))
#             for j in range(start, end):
#                 if i != j and nums[i] == nums[j]:
#                     return True
#         return False

sol = Solution()

print (sol.containsNearbyDuplicate([1,0,1,1], 1))

