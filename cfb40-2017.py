from data import get_cfb_data
from cfb40 import print_selection, make_cfb40_data, calculate_best_cfb40max_and_min_teams
import itertools
import sys

CFB40_MAX = {
    'Grimm': ['OSU','FSU','USC','Texas','Oregon'],
    'Eric': ['OSU','Oklahoma','Auburn','TCU','Oregon'],
    'Nick': ['OSU','FSU','USC','Texas','Oregon'],
    'Ethan': ['Oklahoma','FSU','USC','Texas','Notre Dame'],
}

CFB40_MIN = {
    'Grimm': ['Colorado','Michigan','Texas A&M','UVA','West Virginia'],
    'Eric': ['Boston College','Cal','Minnesota','Utah','West Virginia'],
    'Nick': ['Clemson','Colorado','Illinois','Purdue','West Virginia'],
    'Ethan': ['BYU','Colorado','Minnesota','Missouri','UNC'],
}


week = int(sys.argv[1])
data = get_cfb_data(2017, week)
cfb_data = make_cfb40_data(data)


def print_win_diff(team_diffs, current_data, previous_data):
    for team, diff in team_diffs:
        print("{0:<16} [{1:>2d}-{2:>2d}] {3:>2.1f} -> {4:>2.1f}".format(
            team, current_data.ix[team]['wins'], current_data.ix[team]['losses'],
            previous_data.ix[team]['projected_wins'], current_data.ix[team]['projected_wins']))


if week > 0:
    last_week_data = get_cfb_data(2017, week-1)
    proj_diff = {team: cfb_data.ix[team]['projected_wins'] - last_week_data.ix[team]['projected_wins'] for team in cfb_data.index}
    sorted_diff = [(team, proj_diff[team]) for team in sorted(proj_diff, key=proj_diff.get)]
    print("Top 10 decreases in win projections (last week):")
    print("------------------------------------------------")
    print_win_diff(sorted_diff[:10], cfb_data, last_week_data)
    print("")
    print("Top 10 increases in win projections (last week):")
    print("------------------------------------------------")
    print_win_diff(sorted_diff[-10:], cfb_data, last_week_data)
    print("")

    preseason_data = get_cfb_data(2017, 0)
    proj_diff = {team: cfb_data.ix[team]['projected_wins'] - preseason_data.ix[team]['projected_wins'] for team in cfb_data.index}
    sorted_diff = [(team, proj_diff[team]) for team in sorted(proj_diff, key=proj_diff.get)]
    print("Top 10 decreases in win projections (this season):")
    print("--------------------------------------------------")
    print_win_diff(sorted_diff[:10], cfb_data, preseason_data)
    print("")
    print("Top 10 increases in win projections (this season):")
    print("--------------------------------------------------")
    print_win_diff(sorted_diff[-10:], cfb_data, preseason_data)
    print("")

best_cfb_max, best_cfb_min = calculate_best_cfb40max_and_min_teams(cfb_data, 5)

print("Max Standings:")
print("--------------")
print("")
for name, teams in CFB40_MAX.items():
    print("{0}'s Entries:".format(name))
    print("----------------------")
    print_selection(cfb_data, teams)
    print("")

print("Best Projected Entry:")
print("----------------------")
print_selection(cfb_data, best_cfb_max)
print("")

print("")
print("Min Standings:")
print("--------------")
print("")
for name, teams in CFB40_MIN.items():
    print("{0}'s Entries:".format(name))
    print("----------------------")
    print_selection(cfb_data, teams)
    print("")

print("Best Projected Entry:")
print("----------------------")
print_selection(cfb_data, best_cfb_min)
print("")

    # cfb40max_best, cfb40min_best = calculate_best_cfb40max_and_min_teams(data, 5)
#
# print()
# print("My CFB40 Max selection:")
# print_selection(data, cfb40max_best)
#
# print()
# print("My CFB40 Min selection:")
# print_selection(data, cfb40min_best)