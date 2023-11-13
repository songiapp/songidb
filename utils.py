# Character range function
def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))