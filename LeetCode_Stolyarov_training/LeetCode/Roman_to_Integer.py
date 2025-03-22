class Solution:
    def romanToInt(self, s: str) -> int:
        nums_dict = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
        last = s[-1]
        total = nums_dict[last]
        s = s[:-1]
        for num in s[::-1]:
            if nums_dict[num] < nums_dict[last]:
                total -= nums_dict[num]
            else:
                total += nums_dict[num]
                last = num
        return total
    