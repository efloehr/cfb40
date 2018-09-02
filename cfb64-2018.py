from data import get_cfb_data
from cfbN import print_selection, make_cfb_data, calculate_best_cfbNmax_and_min_teams
from collections import OrderedDict
import itertools
import sys

CFB64_MAX = OrderedDict([

    ('Grimm', ['Alabama','Clemson','FSU','Georgia','Kansas','OSU','Oregon St','Pitt']),
    ('Eric', ['Auburn','Baylor','Clemson','Florida','Mich. St.','Notre Dame','Texas','Washington']),
    ('Nick', ['Baylor','Clemson','Florida','FSU','Miami','Notre Dame','OSU','Texas']),
    ('Ethan', ['Florida','FSU','Nebraska','OSU','PSU','Stanford','TCU','UCLA']),
    ('CompuNick', ['Alabama','Baylor','Cal','Clemson','Florida','OSU','Texas','Washington']),
])

CFB64_MIN = OrderedDict([
    ('Grimm', ['Illinois','Indiana','Louisville','Maryland','Northwestern','Notre Dame','Oklahoma','Wisconsin']),
    ('Eric', ['Arizona State','Colorado','Kentucky','LSU','Northwestern','TCU','UVA','Washington St']),
    ('Nick', ['Kansas','LSU','Northwestern','Oregon St','S Carolina','TCU','USC','Wisconsin']),
    ('Ethan', ['Colorado','Miss St','NC State','Oklahoma State','Purdue','S Carolina','Texas Tech','Washington St']),
    ('CompuNick', ['Arizona State','Kansas','LSU','Northwestern','Ole Miss','S Carolina','UVA','Washington St']),
])


week = int(sys.argv[1])
data = get_cfb_data(2018, week)
if week > 0:
    last_week_data = get_cfb_data(2018, week-1)
else:
    last_week_data = None
preseason_data = get_cfb_data(2018, 0)
cfb_data = make_cfb_data(data)


def print_win_diff(team_diffs, current_data, previous_data):
    for team, diff in team_diffs:
        print("{0:<16} [{1:>2d}-{2:>2d}] {3:>4.1f} -> {4:>4.1f} (net {5:+4.1f})".format(
            team, current_data.loc[team]['wins'], current_data.loc[team]['losses'],
            previous_data.loc[team]['projected_wins'], current_data.loc[team]['projected_wins'], diff))


if week > 0:
    proj_diff = {team: cfb_data.loc[team]['projected_wins'] - last_week_data.loc[team]['projected_wins'] for team in cfb_data.index}
    sorted_diff = [(team, proj_diff[team]) for team in sorted(proj_diff, key=proj_diff.get)]
    print("Top 10 decreases in win projections (last week):")
    print("-------------------------------------------------")
    print_win_diff(sorted_diff[:10], cfb_data, last_week_data)
    print("")
    print("Top 10 increases in win projections (last week):")
    print("-------------------------------------------------")
    print_win_diff(reversed(sorted_diff[-10:]), cfb_data, last_week_data)
    print("")

    proj_diff = {team: cfb_data.loc[team]['projected_wins'] - preseason_data.loc[team]['projected_wins'] for team in cfb_data.index}
    sorted_diff = [(team, proj_diff[team]) for team in sorted(proj_diff, key=proj_diff.get)]
    print("Top 10 decreases in win projections (this season):")
    print("--------------------------------------------------")
    print_win_diff(sorted_diff[:10], cfb_data, preseason_data)
    print("")
    print("Top 10 increases in win projections (this season):")
    print("--------------------------------------------------")
    print_win_diff(reversed(sorted_diff[-10:]), cfb_data, preseason_data)
    print("")

print("Max Standings:")
print("--------------")
print("")
for name, teams in CFB64_MAX.items():
    print("{0}'s Entries:".format(name))
    print("----------------------------------------------------------------------------")
    print_selection(cfb_data, last_week_data, preseason_data, teams)
    print("")

best_cfb_max, best_cfb_min = calculate_best_cfbNmax_and_min_teams(cfb_data, 8)

print("Best Projected Entry:")
print("----------------------------------------------------------------------------")
#print_selection(cfb_data, last_week_data, preseason_data, best_cfb_max)
print("")

print("")
print("Min Standings:")
print("--------------")
print("")
for name, teams in CFB64_MIN.items():
    print("{0}'s Entries:".format(name))
    print("----------------------------------------------------------------------------")
    print_selection(cfb_data, last_week_data, preseason_data, teams)
    print("")

print("Best Projected Entry:")
print("----------------------------------------------------------------------------")
#print_selection(cfb_data, last_week_data, preseason_data, best_cfb_min)
print("")
