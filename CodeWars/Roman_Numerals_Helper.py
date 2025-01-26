roman_to_int = {
            "M": 1000,
            "CM": 900,
            "D": 500,
            "CD": 400,
            "C": 100,
            "XC": 90,
            "L": 50,
            "XL": 40,
            "X": 10,
            "IX": 9,
            "V": 5,
            "IV": 4,
            "I": 1
                    }

class RomanNumerals:
    @staticmethod
    def to_roman(val : int) -> str:
        roman_num = []
        while val > 0:
            for num, values in roman_to_int.items():
                if values <= val:
                    val -= values
                    roman_num.append(num)
                    break
        return "".join(roman_num)

    @staticmethod
    def from_roman(roman_num : str) -> int:
        roman_list = list(roman_num)
        val = 0
        a = 0
        for roman_number in reversed(roman_list):
            for num, values in roman_to_int.items():
                if num == roman_number:
                    if a <= values:
                        val += values
                        a = values
                    else:
                        val -= values
        return val

print (RomanNumerals.from_roman(RomanNumerals.to_roman(540)))
print (RomanNumerals.from_roman(RomanNumerals.to_roman(600)))
print (RomanNumerals.from_roman(RomanNumerals.to_roman(1100)))
print (RomanNumerals.from_roman((RomanNumerals.to_roman(1800))))

print (RomanNumerals.from_roman('III'))
print (RomanNumerals.from_roman('IV'))
print (RomanNumerals.from_roman('LXX'))


