def find(file_path, txt):
    with open(file_path) as f:
        while True:
            try:
                line = next(f)
            except StopIteration:
                break
            if txt in line:
                yield line
