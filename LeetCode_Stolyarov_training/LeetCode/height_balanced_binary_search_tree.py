from typing import List, Optional
import math


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sortedArrayToBST(self, nums: List[int]):
        if not nums:
            return None
        indx = len(nums)//2
        value = TreeNode(nums[indx])
        value.left = self.sortedArrayToBST(nums[:indx])
        value.right = self.sortedArrayToBST(nums[indx + 1:])
        return value


class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        
        # Находим середину массива
        mid = len(nums) // 2
        
        # Создаём корневой узел
        root = TreeNode(nums[mid])
        
        # Рекурсивно строим левое и правое поддеревья
        root.left = self.sortedArrayToBST(nums[:mid])
        root.right = self.sortedArrayToBST(nums[mid + 1:])
        
        return root


from typing import List
import math

class Solution:
    def sortedArrayToBST(self, nums: List[int]):
        self.nums = nums  # Сохраняем список как атрибут экземпляра
        indx = math.ceil(len(nums)//2)
        value = self.nums.pop(indx)
        self.result = [value]
        self.recurs_find(value)
        return self.result

    def recurs_find(self, num: int):
        if self.nums:  # Используем self.nums вместо передачи nums
            value_max = max(self.nums)
            self.nums.remove(value_max)
            self.result.append(value_max)

            if self.nums:  # Проверяем, остались ли элементы
                value_min = min(self.nums)
                self.nums.remove(value_min)
                self.result.append(value_min)

            self.recurs_find(value_max)
            self.recurs_find(value_min)

