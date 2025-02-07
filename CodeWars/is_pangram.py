def is_pangram(st):
    for indx in range (ord('a'), ord('z')):
        if chr(indx) in st.lower():
            continue
        else:
            return False
    return True
