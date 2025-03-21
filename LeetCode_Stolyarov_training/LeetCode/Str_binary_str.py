class Solution:
    def addBinary(self, a: str, b: str) -> str:
        ba = int(a, 2)
        bb = int(b, 2)
        s = bin(sum([ba,bb]))[2:]
        return s
    
    