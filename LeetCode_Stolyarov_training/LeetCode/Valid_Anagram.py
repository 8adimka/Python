class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        from collections import Counter

        count_s = Counter(s)
        count_t = Counter(t)

        return count_s == count_t

  
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        count_s = {}
        count_t = {}
        for ch in s:
            count_s[ch] = count_s.get(ch, 0) + 1
        
        for ch in t:
            count_t[ch] = count_t.get(ch, 0) + 1

        return count_s == count_t
    

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        count_s = {ch:s.count(ch) for ch in s}
        count_t = {ch:t.count(ch) for ch in t}

        return count_s == count_t
    

class Solution:
    def isAnagram(self, s, t) -> bool:
        t = list(t)
        s = list(s)
        if not t and not s:
            return True
        if s:
            letter = s.pop(-1)
            if letter not in t:
                return False
            t.pop(t.index(letter))
            return self.isAnagram(s,t)
        return False
    

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        t_l = list(t)
        for letter in s:
            if letter not in t_l:
                return False
            t_l.pop(t_l.index(letter))

        if len(s) == len(t):
            return True
        return False
        