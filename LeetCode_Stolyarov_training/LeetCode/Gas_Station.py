# There are n gas stations along a circular route, where the amount of gas at the ith station is gas[i].

# You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from the
# ith station to its next (i + 1)th station. You begin the journey with an empty tank at one of the gas stations.

# Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the
# circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique.

from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        current_gas = total_gas = start = 0

        for i in range(len(gas)):
            current_gas += gas[i] - cost[i]
            total_gas += gas[i] - cost[i]
            if current_gas < 0:
                current_gas = 0
                start = i+1
        return start if total_gas >= 0 else -1

                


# class Solution:
#     def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
#         class Linked_list:
#             def __init__ (self, gas=0, cost=0, next=None):
#                 self.gas = gas
#                 self.cost = cost
#                 self.next = next

#             def __iter__ (self):
#                 current = self
#                 while current is not None:
#                     yield current
#                     current = current.next


#         stantions = [Linked_list(g,c) for g,c in zip(gas,cost)]

#         lenth = len(stantions)
#         for i in range(lenth-1):
#             stantions[i].next = stantions[i+1]
#         stantions[-1].next = stantions[0]

#         for start in stantions:
#             amount = start.gas - start.cost
#             if amount >= 0:
#                 current = start.next
#                 while current is not start:
#                     amount += current.gas - current.cost
#                     if amount < 0:
#                         break
#                     current = current.next
#                 if start is current:
#                     return stantions.index(start)
#         return -1
        


        
