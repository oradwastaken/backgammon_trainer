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

    print()
    print(f'║ 13 ║ 14 ║ 15 ║ 16 ║ 17 ║ 18 ║ {y("BAR")} ║ 19 ║ 20 ║ 21 ║ 22 ║ 23 ║ 24 ║ {y("OFF")} ║')
    print(f'╠════╩════╩════╩════╩════╩════╬═════╬════╩════╩════╩════╩════╩════╬═════╣')
    print(
        f'║  {y("·")}    ·    {y("·")}    ·    {y("·")}    · ║     ║  {y("·")}    ·    {y("·")}    ·    {y("·")}    · ║     ║'
        )
    print(f'║  {r("X")}                   {g("O")}      ║     ║  {g("O")}                        {r("X")} ║     ║')
    print(f'║  {r("X")}                   {g("O")}      ║     ║  {g("O")}                        {r("X")} ║     ║')
    print(f'║  {r("X")}                   {g("O")}      ║     ║  {g("O")}                          ║     ║')
    print(f'║  {r("X")}                          ║     ║  {g("O")}                          ║     ║')
    print(f'║  {r("X")}                          ║     ║  {g("O")}                          ║     ║')
    print(f'║                             ║ {y("BAR")} ║                             ║     ║')
    print(f'║  {g("O")}                          ║     ║  {r("X")}                          ║     ║')
    print(f'║  {g("O")}                          ║     ║  {r("X")}                          ║     ║')
    print(f'║  {g("O")}                   {r("X")}      ║     ║  {r("X")}                          ║     ║')
    print(f'║  {g("O")}                   {r("X")}      ║     ║  {r("X")}                        {g("O")} ║     ║')
    print(f'║  {g("O")}                   {r("X")}      ║     ║  {r("X")}                        {g("O")} ║     ║')
    print(
        f'║  ·    {y("·")}    ·    {y("·")}    ·    {y("·")} ║     ║  ·    {y("·")}    ·    {y("·")}    ·    {y("·")} ║     ║'
        )
    print(f'╠════╦════╦════╦════╦════╦════╬═════╬════╦════╦════╦════╦════╦════╬═════╣')
    print(f'║ 12 ║ 11 ║ 10 ║  9 ║  8 ║  7 ║ {y("BAR")} ║  6 ║  5 ║  4 ║  3 ║  2 ║  1 ║ {y("OFF")} ║')
    print()
