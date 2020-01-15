import os

fpath = os.path.dirname(__file__)
with open(os.path.join(fpath, 'player_ids.txt'), 'r') as pidf:
    ids = [pid for pid in pidf.read().split('\n') if pid != '']