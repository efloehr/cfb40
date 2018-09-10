from data import get_espn_standings_data, get_espn_power_index_data
from cfbN import calculate_best_cfbNmax_and_min_teams, print_selection, make_cfb_data
import pandas as pd
import itertools

year = 2018
week = 0
num_teams = 8

standings = get_espn_standings_data(year-1)
power = get_espn_power_index_data(year, week)
combined = pd.concat([standings, power], axis=1, join='inner')

standings_teams = sorted(standings.index)
power_teams = sorted(power['team'])

print("{}/{} -> {}".format(len(standings_teams), len(power_teams), len(combined)))

for team in standings_teams:
    if team not in power_teams and team != 'Idaho':
        print("'{}' not found in ESPN PI data".format(team))

teams = sorted(combined['team'])
for team in teams:
    team_data = combined.loc[team]
    print(
    "{0:<16} {1:>2d} -> {2:>4.1f}".format(
        team_data['team'], team_data['ovr_win'], team_data['projected_wins']))
