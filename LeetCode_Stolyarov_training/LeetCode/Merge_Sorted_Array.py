# You are given two integer arrays nums1 and nums2, sorted in non-decreasing order,
# and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

# Merge nums1 and nums2 into a single array sorted in non-decreasing order.

# The final sorted array should not be returned by the function, but instead be stored inside the
# array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote
# the elements that should be merged, and the last n elements are set to 0 and should be ignored.
# nums2 has a length of n.
# Constraints:

# nums1.length == m + n
# nums2.length == n
# 0 <= m, n <= 200
# 1 <= m + n <= 200
# -109 <= nums1[i], nums2[j] <= 109


from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        for i in range (1, n+1):
            nums1[-i] = nums2[-i]
        nums1.sort()
