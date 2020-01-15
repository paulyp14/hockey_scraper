import itertools

class Team:
    """
    Team class used for scraping NHL games
    Allows for keeping track of who is on which team
    Allows for keeping track of shifts, line combinations

    :var team_name: the name of the team as a string
    :var coach: the name of the coach as a string
    :var roster: a dictionary of the player's playing for the team in the game
                    { player_num (str): Player object}
    :var abbrev: the regularized three letter abbreviation for the team
    :var shift_chart: a dictionary of all a team's players' shifts
                    { player_num: {shift_num: (period, shift_start, shift_end, shift_duration)}
                    NOTE:
                        The last entry in each dictionary associated with each player_num is:
                        {"final": (all_toi, ev_toi, pp_toi, pk_toi)}

    :var combo_chart: combo_chart will be identical to shift chart, except for
              1- the fact that there won't be 'final' row representing
                 official nhl data
              2- each shift tuple will have a strength entry at the last index
                 if the shift lasts long enough that there is a strength change in the middle, then there will be a
                 a verbose 'separator' in the final index of the tuple indicating when the strength changed and what the
                 the change was
                 if the shift lasts between two periods, the verbose separator will be there but there as well but there
                 two strengths that are different might be the same
    """

    def __init__(self, team_name, coach="", roster=None, abbrev=""):
        """
        The constructor, initializes all vars
        Allows for team_name, coach, roster and abbrev to be passed to the constructor
        shift_chart and combo_chart will be updated by GenerateGameStats and IceTimeParser, respectively

        :param team_name: the name of the team as a string
        :param coach: the name of the coach as a string
        :param roster: a dictionary of the player's playing for the team in the game
                { player_num (str): Player object}
        :param abbrev: the regularized three letter abbreviation for the team
        """
        self.team_name = team_name
        self.coach = coach
        self.roster = roster
        self.abbrev = abbrev
        self.shift_chart = None
        self.combo_chart = None

    def get_combo(self, *args):
        """
        a function meant to get the icetimes for whatever combinations are passed
        :param args: must be player numbers as strings, the args will be permuted until the key used in combo_chart
                     is found, or until all permutations have been tried, in which case this combination was never on
                     the ice at the same time
        :return: nothing, prints either "combo not used" or the combination's icetime
        """
        combo_results = None
        key = None
        for poss_combo in list(itertools.permutations(args)):
            poss_key = " - ".join(poss_combo)
            try:
                combo_results = self.combo_chart[poss_key]
                key = poss_key
                break
            except KeyError:
                pass
        if combo_results is None:
            print("Combo not used in the game")
        else:
            print(f"Combo used: {key}\n{combo_results}")
