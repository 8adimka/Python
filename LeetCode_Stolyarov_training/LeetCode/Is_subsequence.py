# import re
# class Solution:
#     def isSubsequence(self, s: str, t: str) -> bool:
#         if s == t:
#             return True
#         reg_exp = ''.join([r'.*']+[rf'{letter}.*' for letter in s])
#         m = re.match(reg_exp, t)
#         if m:
#             return bool(m.group(0))
#         return False

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if s == t or s == '':
            return True
        i = 0
        try: 
            for j in t:
                if j == s[i]:
                    i += 1
        except:
            pass
        return i == len(s)


sol = Solution()
print (sol.isSubsequence("aza", "abzba"))
print (sol.isSubsequence("aaaaaa", "bbaaaa"))
print (sol.isSubsequence("abc", "gaghbgdc"))
print (sol.isSubsequence("", ""))
