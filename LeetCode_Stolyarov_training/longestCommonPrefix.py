from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(set(strs)) == 1:
            return strs[0]
        longest_prefix = ''
        for word in strs:
            for letter_indx in range (len(min(strs))):
                for word_indx in range (0, len(strs)):
                    if strs.index(word) != strs.index(strs[word_indx]):
                        if word[:letter_indx+1] == strs[word_indx][:letter_indx+1]:
                            b = True
                        else:
                            b = False
                            break
                if b:
                    longest_prefix = word[:letter_indx+1]
        return longest_prefix
                    
    
solution = Solution()
print (solution.longestCommonPrefix(["dog","racecar","car"]))
print (solution.longestCommonPrefix(["ab", "a"]))
print (solution.longestCommonPrefix(["flower","flow","flight"]))
print (solution.longestCommonPrefix(["ac","ac","a","a"]))

print (len(min(["dog","racecar","car", "ab"])))


