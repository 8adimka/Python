def reverse_words(text):
    word_list = text.split(' ')
    reverse_list = [''.join(reversed(list(word))) for word in word_list]
    return ' '.join(reverse_list)

test = 'word water'
test = reverse_words(test)
print(test)

def reverse_words(str):
    return ' '.join(s[::-1] for s in str.split(' '))

