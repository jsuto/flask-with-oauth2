def fix_base64_padding(s):
    missing_padding = 4 - len(s) % 4
    if missing_padding:
        s += '='* missing_padding
    return s
