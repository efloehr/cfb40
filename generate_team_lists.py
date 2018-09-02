from data import get_cfb_data
from cfbN import calculate_best_cfbNmax_and_min_teams, print_selection, make_cfb_data
import itertools

data = get_cfb_data(2018, 0)
num_teams = 8

teams = sorted(data['team'])
for team in teams:
    team_data = data.ix[team]
    print(
    "{0:<16} {1:>2d} -> {2:>4.1f}".format(
        team_data['team'], team_data['ovr_win'], team_data['projected_wins']))
