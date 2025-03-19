class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if ransomNote == '':
            return True
        magazine = list(magazine)
        for letter in ransomNote:
            if letter in magazine:
                magazine.remove(letter)
                print (magazine)
            else:
                return False
        return True
    
sol = Solution()
print (sol.canConstruct("a","a"))
print (sol.canConstruct("a","b"))
print (sol.canConstruct("aa","ab"))
