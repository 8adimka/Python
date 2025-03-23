# Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the values of any two different nodes in the tree.

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:

        def inorder (q):
            if not q:
                return []
            return inorder(q.left) + [q.val] + inorder(q.right)
        
        num_list = inorder(root)
        
        min_dif = float('inf')
        for i in range(1, len(num_list)):
            min_dif = min(min_dif, abs(num_list[i]-num_list[i-1]))
        return min_dif

        