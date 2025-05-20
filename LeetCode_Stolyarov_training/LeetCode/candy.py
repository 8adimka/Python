from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        c_min = 1
        c_current = c_min
        i = 0
        res = []

        while i < len(ratings)-1:
            if ratings[i] < ratings[i+1]:
                res.append(c_current)
                c_current += 1
                if i < len(ratings)-1:
                    i += 1
                else:
                    i += 1
                    break

            if i < len(ratings)-1 and ratings[i] > ratings[i+1]:
                c_current = c_min
                cur_i = i
                while ratings[cur_i] > ratings[cur_i+1] and cur_i < len(ratings)-1:
                    c_current += 1
                    cur_i += 1
                res.append(c_current)
                while c_current > c_min and i < len(ratings)-1:
                    c_current -= 1
                    res.append(c_current)                    
                    i += 1

        if ratings[i] > ratings[i-1]:
            res.append(c_current+1)
        else:
            res.append(c_min)

        return sum(res)
    

sol = Solution()
print (sol.candy([0,1,2,3,2,1,0]))
