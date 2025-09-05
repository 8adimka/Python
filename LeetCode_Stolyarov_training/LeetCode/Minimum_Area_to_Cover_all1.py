from typing import List


class Solution:
    def minimumArea(self, grid: List[List[int]]) -> int:
        min_hor = None

        i = 0
        j = 0

        while j < len(grid[0]):
            if grid[i][j] == 1:
                if min_hor is None:
                    min_hor = j
                    max_hor = j
                    min_ver = i
                    max_ver = i

                elif min_ver > i:
                    min_ver = i
                    if max_hor < j:
                        max_hor = j

                elif max_ver < i:
                    max_ver = i
                    if max_hor < j:
                        max_hor = j

                elif max_hor < j:
                    max_hor = j

            i += 1

            if i >= len(grid):
                j += 1
                i = 0
        if min_hor is None:
            return 0

        return (max_hor - min_hor + 1) * (max_ver - min_ver + 1)
