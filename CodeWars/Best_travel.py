import itertools
def choose_best_sum(t, k, ls):
    try: 
        return max(sum(i) for i in itertools.combinations(ls,k) if sum(i)<=t)
    except:
        return None


# def choose_best_sum(t, k, ls):
#     mut_list = [sum(var) for var in itertools.permutations(ls, r=k) if sum(var) <= t]
#     max_var = 0
#     for sum_var in mut_list:
#         if max_var < sum_var:
#             max_var = sum_var
#     if max_var == 0:
#         return None
#     return max_var

import itertools
def choose_best_sum(t, k, ls):
    mut_list = itertools.combinations(ls, r=k)
    max_var = 0
    for var in mut_list:
        sum_var = sum(var)
        if max_var < sum_var <= t:
            max_var = sum_var
    return max_var



ts = [50, 55, 56, 51, 58]
print(choose_best_sum (163, 3, ts))
print(choose_best_sum (160, 3, ts))
print(choose_best_sum (0, 3, ts))
print(choose_best_sum (163, 0, ts))