class Letters:
    def __init__(self, letters="""abcdefghijklmnopqrstuvwxyz"""):
        self.letters = letters
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            val = self.letters[self.i]
            self.i += 1
            return val
        except IndexError:
            raise StopIteration


for letter in Letters():
    print(letter)

for l in Letters("1,2,3"):
    print(l)
