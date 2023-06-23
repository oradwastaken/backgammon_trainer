def clear_lines(n: int = 1) -> None:
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def read_int(prompt: str) -> int:
    output = input(prompt)
    return int(output.strip().split()[0])


if __name__ == '__main__':
    while True:
        out = read_int('give me an int')
        print(out)
        print(type(out))
