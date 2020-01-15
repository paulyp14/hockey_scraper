from nhl.scraper.scraper import Scraper
from utils import utils


class PlayerScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.player_info = None

    def scrape_player_info(self, playerid):
        self.get(PlayerScraper.player_info.format(playerid))
        self.player_info = self.json_from_response_text(rkey=['people', 0])
        self.player_info['current_team'] = self.player_info['current_team']['id']
        self.player_info['primary_position'] = self.player_info['primary_position']['code']

        # 'nhl_id', 'current_age', 'height', 'alternate_captain', 'teams'
        nhl_id = self.player_info.pop('nhl_id')
        self.player_info['reference_ids'] = {'1': nhl_id}

        self.player_info.pop('full_name')
        self.player_info.pop('current_age')
        self.player_info.pop('alternate_captain')
        self.player_info.pop('roster_status')

        self.player_info['height'] = utils.format_nhl_height_for_insert(self.player_info['height'])
        self.player_info['teams'] = [self.player_info['current_team']]
        self.player_info['birth_state'] = self.player_info.pop('birth_state_province')
        self.player_info['primary_number'] = int(self.player_info['primary_number'])

        self.format_birthday()

    def get_player_info(self, playerid):
        self.scrape_player_info(playerid)
        return self.player_info

    def format_birthday(self):
        y, m, d = self.player_info.pop('birth_date').split('-')
        self.player_info['birth_day'] = int(d)
        self.player_info['birth_month'] = int(m)
        self.player_info['birth_year'] = int(y)

    player_info = "https://statsapi.web.nhl.com/api/v1/people/{}"
