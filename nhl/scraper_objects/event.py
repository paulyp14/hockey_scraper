class Event:

    def __init__(self,
                 event_type,
                 contributors,
                 event_num=-1,
                 period=None,
                 time_of_game=None,
                 time_left_period=None,
                 game_state=None,
                 secondary_type=None,
                 attacking_team=None,
                 defending_team=None,
                 home_players_on_ice=None,
                 away_players_on_ice=None,
                 zone=None,
                 distance=None,
                 unparsed_on_ice=None,
                 type_miss=None,
                 coordinates=None):
        """

        :param event_type:
        :param contributors: list of tuples of the form ( str ( contribution type ), NHL_Object.Player ( contributor ) )
        :param event_num:
        :param period:
        :param time_of_game:
        :param time_left_period:
        :param game_state:
        :param secondary_type:
        :param attacking_team:
        :param defending_team:
        :param home_players_on_ice:
        :param away_players_on_ice:
        :param zone:
        :param distance:
        :param unparsed_on_ice:
        :param type_miss:
        :param coordinates:
        """
        self.event_num = event_num
        self.event_type = event_type
        self.period = period
        self.time_of_game = time_of_game
        self.time_left_period = time_left_period
        self.game_state = game_state
        self.secondary_type = secondary_type
        self.contributors = contributors
        self.attacking_team = attacking_team
        self.defending_team = defending_team
        self.attacking_players_on_ice = home_players_on_ice
        self.defending_players_on_ice = away_players_on_ice
        self.zone = zone
        self.distance = distance
        self.unparsed_on_ice = unparsed_on_ice
        self.type_miss = type_miss
        self.coordinates = coordinates
        self.complete_info = False

    def convert_time_of_game(self, time_of_game):
        self.time_of_game = str(int(time_of_game.split(":")[0]) + ((int(self.period)-1)*20)) + ":" + time_of_game.split(":")[1]

    def completed(self):
        self.complete_info = True

    def print_event(self):
        if "PSTR" in self.event_type or "PEND" in self.event_type or "GEND" in self.event_type or "PERIOD_START" in self.event_type or "PERIOD_END" in self.event_type or "GAME_END" in self.event_type:
            print(f"{self.event_type}, period {self.period}")
        elif "STOP" in self.event_type and "ICING" not in self.secondary_type:
            print(f"{self.event_type}, {self.secondary_type}")
            print(f"    Occurred in period {self.period} at time {self.time_of_game} with {self.time_left_period} left in period, at {self.game_state}")
        else:
            contributions = ""
            for t, p in self.contributors:
                contributions += "      {} contributed as {}\n".format(p.full_name, t)
            print("{}, {}, involved {}".format(self.event_type, self.secondary_type if self.secondary_type is not None
                    else "", [p[1].full_name for p in self.contributors]))
            print(f"    Occurred in period {self.period} at time {self.time_of_game} with {self.time_left_period} left in period, at {self.game_state} in {self.zone} from {self.distance if len(self.distance) != 0 else '{}'} at position x:{self.coordinates[0] if type(self.coordinates) is tuple else ''}, y:{self.coordinates[1] if type(self.coordinates) is tuple else ''}")
            print(f"    Positive event for {self.attacking_team.team_name}")
            print(f"    Negative event for {self.defending_team.team_name}")
            print("{}".format(contributions), end="")
            print(f"         {self.attacking_team.team_name} has on ice {[p.full_name for p in self.attacking_players_on_ice]}")
            print(f"         {self.defending_team.team_name} has on ice {[p.full_name for p in self.defending_players_on_ice]}")

        print("")

    def int_time_of_game(self):
        """
        simple method to return time_of_game as an integer
        :return: integer representing time elapsed since start of game in seconds
        """
        mins = int(self.time_of_game.split(":")[0])
        secs = int(self.time_of_game.split(":")[1])
        return (mins*60) + secs