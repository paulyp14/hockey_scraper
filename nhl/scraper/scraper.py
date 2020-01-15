import json
import requests


class Scraper:

    def __init__(self):
        self.response = None

    def get(self, addr):
        self.response = requests.get(addr)

    def json_from_response_text(self, rkey=None):
        def format_key(key):
            if key == 'id':
                return 'nhl_id'
            else:
                return ''.join([(chr if chr.islower() else f'_{chr.lower()}') for chr in key])

        rt = json.loads(self.response.text)
        if rkey is not None:
            if isinstance(rkey, list):
                for k in rkey:
                    rt = rt[k]
            else:
                rt = rt[rkey]

        return {
            format_key(k): v for k, v in rt.items()
        }