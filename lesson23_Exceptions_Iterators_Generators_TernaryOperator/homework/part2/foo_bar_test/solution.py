foo = lambda n: (i**2 for i in range(n))

if __name__ == "__main__":
    print([x for x in foo(5)])
