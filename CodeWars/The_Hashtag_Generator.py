def generate_hashtag(s):
    s_list = s.split(' ')
    cap_s_list = [word.capitalize() for word in s_list]
    return False if len(s) == 0 or len(''.join(cap_s_list)) > 140 else '#' + ''.join(cap_s_list)

