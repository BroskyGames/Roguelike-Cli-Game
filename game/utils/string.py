def line(left: str, right: str, width: int) -> str:
    return f"{left[:width - len(right)]:<{width - len(right)}}{right}"


if __name__ == '__main__':
    print(f"|{line('1234567890', '', 5)}|")
