def printc(text: str, foreground: int, background: int):
    print(f'\033[{30 + foreground}m\033[{40 + background}m' + str(text) + "\033[0m", end="")

def ito36(n):
    if n < 10: return n
    else: return chr(ord('A') - 10 + n)

def coord(n):
    a, b = divmod(n, 36)

    if a == 0: return str(ito36(b))

    return str(ito36(a)) + str(coord(b))