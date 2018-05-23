def fill_from_left(src, exp_len=64, filler='0'):
    return filler * (exp_len - len(src)) + src
