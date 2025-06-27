def room_counter(events_list: list) -> int:
    days_set = set()
    counter = 0
    if events_list:
        counter += 1

    events_list.sort(key=lambda x: sum(x))

    for event in events_list:
        current_event = set(range(event[0], event[-1]))
        for day in current_event:
            if day in days_set:
                counter += 1
                break
        days_set.update(current_event)

    return counter


print(room_counter([[1, 2], [4, 10], [3, 7]]))

print(room_counter([[1, 4], [4, 10], [11, 17]]))

print(room_counter([[1, 2], [3, 4], [5, 6], [1, 5000]]))
print(room_counter([[1, 5000], [1, 2], [3, 4], [5, 6]]))

print("_____________________________________")


def room_counter2(event_l: list) -> int:
    max_count = 0
    counter = 0
    work_l = []
    for x in event_l:
        work_l.append((x[0], 1))
        work_l.append((x[-1], -1))

    work_l.sort()
    for day in work_l:
        counter += day[-1]
        if counter > max_count:
            max_count = counter

    return max_count


print(room_counter2([[1, 2], [4, 10], [3, 7]]))

print(room_counter2([[1, 4], [4, 10], [11, 17]]))

print(room_counter2([[1, 2], [3, 4], [5, 6], [1, 5000]]))
print(room_counter2([[1, 5000], [1, 2], [3, 4], [5, 6]]))
