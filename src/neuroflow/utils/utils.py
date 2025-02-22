def _format_text(text, bold=False, underline=False, italic=False, color=None):
    codes = []
    if bold:
        codes.append("1")  # Bold code
    if underline:
        codes.append("4")  # Underline code
    if italic:
        codes.append("3") # Italics code
    colors = {
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
    }
    if color in colors:
        codes.append(colors[color])

    if codes:
        return f"\033[{';'.join(codes)}m{text}\033[0m"  # Combine codes
    else:
        return text