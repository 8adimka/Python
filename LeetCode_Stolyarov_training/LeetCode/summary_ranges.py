from typing import List


class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if nums:
            a,b = None,None
            result = []
            for i in range(len(nums)):
                if not a and a != 0:
                    a = nums[i]
                    try:
                        if a+1 != nums[i+1]:
                            result.append(str(a))
                            a = None
                    except:
                        result.append(str(a))
                        a = None
                    continue
                b = nums[i]
                try:
                    if b+1 != nums[i+1]:
                        result.append(f'{a}->{b}')
                        a,b = None,None
                except:
                    result.append(f'{a}->{b}')
                    a,b = None,None
            return result

        else:
            return []
        
sol = Solution()
print(sol.summaryRanges([1, 3, 5, 7, 9, 11]))

print(sol.summaryRanges([0, 2, 3, 4, 6, 8, 9]))

from typing import List

class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        if not nums:
            return []

        result = []
        start = nums[0]  # Начало текущего диапазона

        for i in range(1, len(nums)):
            # Если текущий элемент не является следующим числом в последовательности
            if nums[i] != nums[i - 1] + 1:
                # Если диапазон состоит из одного числа
                if start == nums[i - 1]:
                    result.append(str(start))
                else:
                    result.append(f"{start}->{nums[i - 1]}")
                start = nums[i]  # Начинаем новый диапазон

        # Обработка последнего диапазона
        if start == nums[-1]:
            result.append(str(start))
        else:
            result.append(f"{start}->{nums[-1]}")

        return result

