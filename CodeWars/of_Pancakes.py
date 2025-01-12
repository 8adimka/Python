def get_largest_index(stack):
    """Находит индекс первого максимального элемента в стеке."""
    return stack.index(max(stack))


def flip_pancakes(stack):
    """Сортирует блины и возвращает порядок переворотов."""
    position = []
    sorted_stack = stack[:]  # Копируем оригинальный стек для работы

    while len(stack) > 1:
        largest_index = get_largest_index(stack)

        # Если наибольший элемент уже наверху
        if largest_index == 0:
            position.append(len(stack) - 1)
            sorted_stack = sorted_stack[:len(stack)][::-1] + sorted_stack[len(stack):]
            stack = sorted_stack[:len(stack)]
            stack.pop(len(stack) - 1)

        # Если наибольший элемент не на своем месте
        elif largest_index != len(stack) - 1:
            position.append(largest_index)
            sorted_stack = sorted_stack[:largest_index + 1][::-1] + sorted_stack[largest_index + 1:]
            stack = sorted_stack[:len(stack)]

        else:
            # Если наибольший элемент уже в конце, удаляем его
            stack.pop(largest_index)

    return position
print (flip_pancakes([1,5,8,3]))