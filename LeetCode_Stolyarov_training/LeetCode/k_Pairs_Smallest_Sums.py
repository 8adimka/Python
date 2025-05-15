from typing import List


class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        res = [[nums1[0], nums2[0]]]
        i = 1
        while len(res) < k*1.5 and (i < len(nums2) or i < len(nums1)):
            for j in range(0,i):
                if i < len(nums1):
                    res.append([nums1[i], nums2[j]])
                if i < len(nums2):
                    res.append([nums1[j], nums2[i]])
                if i < len(nums1) and i < len(nums2):
                    res.append([nums1[i], nums2[i]])
            i+=1
        res.sort(key=sum)
        return  res[0:k]
    
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        heap = []
        res = []

        


        

                


        