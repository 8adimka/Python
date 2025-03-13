class Fib:
    def __init__(self, n):
        self.n = n
        self.index = 0
        self.current = 1
        self.prev = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.n:
            self.index += 1
            if self.index < 3:
                return self.index - 1
            res = self.current + self.prev
            self.prev = self.current
            self.current = res
            return res
        else:
            raise StopIteration


fib = Fib(15)
result = [x for x in fib]
