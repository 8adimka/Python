def sum_of_intervals(intervals):
    s, top = 0, float("-inf")
    for a,b in sorted(intervals):
        if top < a: top    = a
        if top < b: s, top = s+b-top, b
    return s

def sum_of_intervals(intervals):
    union_num = set()
    for interval in intervals:
        list_num =  [i for i in range (interval[0], (interval[-1]+1))]
        union_num = union_num.union(list_num)
    list(union_num).sort()
    counter = 0
    b = -1
    for num in union_num:
        if num == b+1:
            counter += 1
            b = num
        else:
            b = num
    return counter
    

print (sum_of_intervals([(1, 5), (6, 10)]))

def sum_of_intervals(intervals):
    if not intervals:
        return 0

    # Sort intervals by their starting point
    intervals.sort(key=lambda x: x[0])

    # Merge intervals and calculate the total length
    merged_intervals = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end:  # Overlapping intervals
            current_end = max(current_end, end)
        else:  # Non-overlapping interval
            merged_intervals.append((current_start, current_end))
            current_start, current_end = start, end

    # Add the last interval
    merged_intervals.append((current_start, current_end))

    # Calculate the total length of the merged intervals
    total_length = sum(end - start for start, end in merged_intervals)
    return total_length