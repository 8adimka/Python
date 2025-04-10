from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        w_ind = 1
        b = True
        for i in range (1, len(nums)):
            if nums[i] != nums[i-1]:
                nums[w_ind] = nums[i]
                w_ind += 1
                b = True
            else:
                if b:
                    nums[w_ind] = nums[i]
                    w_ind += 1
                    b = False
        return w_ind
        