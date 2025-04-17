def valid (test_str):
    valid_dict = {'(': ')', '{': '}', '[': ']'}
    stack = []
    for char in test_str:
        if char in valid_dict.keys():
            stack.append(char)
        elif char in valid_dict.values():
            if char == valid_dict[stack[-1]]:
                del stack [-1]
                continue
            else:
                return False
    if not stack:
        return True
    return False
