def rgb(r, g, b):
    def clamp_and_convert(value):
        # Clamp the value between 0 and 255
        value = max(0, min(value, 255))
        # Convert to hexadecimal and format to always have two digits
        return f"{value:02X}"

    # Convert each component and concatenate the results
    return clamp_and_convert(r) + clamp_and_convert(g) + clamp_and_convert(b)

# Example usage:
print(rgb(255, 255, 255))  # Output: FFFFFF
print(rgb(255, 0, 0))      # Output: FF0000
print(rgb(-20, 275, 125))  # Output: 00FF7D


pl_input = float (input ('Введите число -> '))

number = max(min(255, pl_input), 0)

print (f'Ближайщее число к вашему в диапазоне от 0 до 255 -> {round (number)}')
