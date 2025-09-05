class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        res = [[] for _ in range(numRows)]

        i = 1
        l_i = 0

        direct = 1
        res[0].append(s[0])

        while i < len(s):
            l_i += direct

            if l_i == 0 or l_i == len(res) - 1:
                direct = -direct

            res[l_i].append(s[i])
            i += 1

        for i in range(len(res)):
            res[i] = "".join(res[i])

        return "".join(res)
