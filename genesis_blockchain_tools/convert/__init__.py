def fill_from_left(src, exp_len=64, filler='0'):
    return filler * (exp_len - len(src)) + src

def int_to_hex_str(value, exp_len=64):
    return fill_from_left(format(value, 'x'), exp_len=exp_len, filler='0')
