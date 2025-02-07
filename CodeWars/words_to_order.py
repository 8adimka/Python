def order(sentence):
    if sentence:
        word_list = sentence.split(' ')
        result = {}
        for word in word_list:
            for letter in word:
                if letter.isdigit():
                    result[int(letter)] = word
        return ' '.join([result[index+1] for index in range(len(word_list))])
    return ''


def order(s):
    z = []
    for i in range(1,10):
        for j in list(s.split()):
            if str(i) in j:
               z.append(j)
    return " ".join(z)

