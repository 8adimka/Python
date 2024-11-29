string_words = 'Мама, я графоман, спасити!'
letters_count = 0
words_count = 0

strind_without_simbols = string_words.translate(str.maketrans('','',',!'))
strind_without_spaces = strind_without_simbols.replace (' ', '')
letters_count = len(strind_without_spaces)
words_count = len (strind_without_simbols.split (' '))

print (f'Букв в строке: {letters_count}, а слов в строке: {words_count}')

def has_rrr(word):
    if 'р' in word or 'Р' in word:
            result = True
    else:
            result = False
    return result

# word = input()
# result = has_rrr(word)
# print(result)


player_input = input('Введите два числа через пробел\nи мы заполним список четными числами, которые есть в промежутке.\nОба числе не входят в промежуток\n->')

player_list = player_input.split (' ')
player_max = max (int(player_list[0]), int(player_list[1]))
player_min = min (int(player_list[0]), int(player_list[1]))

[print (i) for i in range ((player_min+1), player_max) if i%2==0]

