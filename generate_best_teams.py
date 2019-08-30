from data import get_cfb_data
from cfbN import calculate_best_cfbNmax_and_min_teams, print_selection, make_cfb_data
import itertools

data = get_cfb_data(2019, 0)
num_teams = 8

cfbNframe = make_cfb_data(data)
cfbNdict = cfbNframe.to_dict(orient='index')

# Get all combinations of n teams
all_n_teams = itertools.combinations(cfbNdict.keys(), num_teams)
cfbN_num = 0

# Get all combinations of n teams with 8n wins or less
cfbNmax_selection = None
cfbNmax_predicted_wins = -1
cfbNmax_num = 0

cfbNmin_selection = None
cfbNmin_predicted_wins = 999999
cfbNmin_num = 0

n8wins = num_teams * 8

for n_team in all_n_teams:
    cfbN_num += 1
    wins = sum([cfbNdict[team]['ovr_win'] for team in n_team])
    proj_wins = sum([round(cfbNdict[team]['projected_wins']) for team in n_team])
    if wins <= n8wins:
        cfbNmax_num += 1
        if proj_wins > cfbNmax_predicted_wins:
            cfbNmax_predicted_wins = proj_wins
            cfbNmax_selection = n_team
            print("Current MAX wins: {}".format(proj_wins))
    if wins >= n8wins:
        cfbNmin_num += 1
        if proj_wins < cfbNmin_predicted_wins:
            cfbNmin_predicted_wins = proj_wins
            cfbNmin_selection = n_team
            print("Current min wins: {}".format(proj_wins))

print("Number of total team combinations: {}".format(cfbN_num))
print("Number of team combinations greater than {} wins: {}".format(n8wins, cfbNmax_num))
print("Number of team combinations less than {} wins: {}".format(n8wins, cfbNmin_num))
    
print("----- MAX {} -----".format(cfbNmax_predicted_wins))
print_selection(data, data, data, cfbNmax_selection)
print("------------------")
print("")

print("----- min {} -----".format(cfbNmin_predicted_wins))
print_selection(data, data, data, cfbNmin_selection)
print("------------------")
print("")
