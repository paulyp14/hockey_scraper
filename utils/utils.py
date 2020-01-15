def format_nhl_height_for_insert(h):
    s = h.split("\' ")
    m = int(s[0]) * 0.3048
    inches = int(s[1].replace('"', '')) * (1/12) * 0.3048
    return m + inches