from typing import Any

black = "\u001b[30m"
grey = "\u001b[30;1m"
white = '\u001b[37m'
red = '\u001b[31m'
green = '\u001b[32m'
yellow = '\u001b[33m'
blue = '\u001b[34m'
magenta = '\u001b[35m'
cyan = '\u001b[36m'
reset = '\u001b[0m'


def k(foo: Any) -> str:
    return f"{black}{foo}{reset}"


def w(foo: Any) -> str:
    return f"{white}{foo}{reset}"


def r(foo: Any) -> str:
    return f"{red}{foo}{reset}"


def g(foo: Any) -> str:
    return f"{green}{foo}{reset}"


def y(foo: Any) -> str:
    return f"{yellow}{foo}{reset}"


def b(foo: Any) -> str:
    return f"{blue}{foo}{reset}"


def m(foo: Any) -> str:
    return f"{magenta}{foo}{reset}"


def c(foo: Any) -> str:
    return f"{cyan}{foo}{reset}"


if __name__ == '__main__':
    # Example how to use:
    print(f"{r('This is in red')} This is normal")
