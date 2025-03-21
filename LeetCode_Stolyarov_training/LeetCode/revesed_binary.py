class Solution:
    def reverseBits(self, n: int) -> int:
        rev_buts = bin(int(''.join(reversed(str(n)))))[2:].zfill(32)
        return int(rev_buts, 2)
    

