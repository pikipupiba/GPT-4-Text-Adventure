def next_non_whitespace(s, start_position):
    # Find next non-whitespace character
    for i in range(start_position, len(s)):
        if not s[i].isspace():
            return i, s[i]
    return None

def next_non_number(s, start_position):
    # Find next non-number character
    for i in range(start_position, len(s)):
        if not s[i].isdigit() and s[i] != "." and s[i] != "-":
            return i, s[i]
    return None