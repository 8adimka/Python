# Average of Levels in Binary Tree
# Given the root of a binary tree, return the average value of the nodes on each level
# in the form of an array. Answers within 10-5 of the actual answer will be accepted.

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import List, Optional


class Solution:
    def averageOfLevels(self, root: Optional[TreeNode]) -> List[float]:
        queue = [root]
        result = []
        while queue:
            sum_level = 0
            next_level=[]
            for i in queue:
                sum_level += i.val

                if i.left:
                    next_level.append(i.left)
                if i.right:
                    next_level.append(i.right)

            result.append(sum_level/len(queue))
            queue = next_level
        return result

