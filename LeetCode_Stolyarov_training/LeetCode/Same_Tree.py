# 100. Same Tree
# Given the roots of two binary trees p and q, write a function to check if they are the same or not.

# Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# recursive method*
# class Solution:
#     def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:

#         if not p and not q:
#             return True
        
#         if not p or not q:
#             return False
        
#         if p.val != q.val:
#             return False
        
#         return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
    

# method with deque
from collections import deque

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        queue_1 = deque([p])
        queue_2 = deque([q])

        while queue_1 and queue_2:
            node1 = queue_1.popleft()
            node2 = queue_2.popleft()

            if not node1 and not node2:
                continue
            if not node1 or not node2:
                return False
            if node1.val != node2.val:
                return False

            queue_1.append(node1.left)
            queue_1.append(node1.right)
            queue_2.append(node2.left)
            queue_2.append(node2.right)

        return not queue_1 and not queue_2


# easy method (not optimized, but understandable)
class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        queue_1 = [p]
        queue_2 = [q]

        while queue_1 and queue_2:
            node1 = queue_1.pop(0)  # Извлекаем первый элемент
            node2 = queue_2.pop(0)

            if not node1 and not node2:
                continue
            if not node1 or not node2:
                return False
            if node1.val != node2.val:
                return False

            queue_1.append(node1.left)
            queue_1.append(node1.right)
            queue_2.append(node2.left)
            queue_2.append(node2.right)

        return not queue_1 and not queue_2
