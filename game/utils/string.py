def line(left: str, right: str, width: int) -> str:
    return f"{left[: width - len(right)]:<{width - len(right)}}{right}"


def center(text: str, width: int, margin: int = 0) -> tuple[int, str]:
    max_len = max(0, width - 2 * margin)
    clipped = text[:max_len]

    start = margin + max(0, (width - 2 * margin - len(clipped)) // 2)

    return start, clipped


if __name__ == "__main__":
    print(f"|{line('1234567890', '', 5)}|")
