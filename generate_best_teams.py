from data import get_cfb_data
from cfbN import calculate_best_cfbNmax_and_min_teams, print_selection, make_cfb_data
import itertools

data = get_cfb_data(2018, 0)
num_teams = 8

cfb40frame = make_cfb_data(data)
cfb40dict = cfb40frame.to_dict(orient='index')

# Get all combinations of n teams
all_n_teams = itertools.combinations(cfb40dict.keys(), num_teams)

# Get all combinations of 5 teams with 8n wins or less
cfb40max_selection = None
cfb40max_predicted_wins = 74  # 76
cfb40min_selection = None
cfb40min_predicted_wins = 45  # 43

n8wins = num_teams * 8

for n_team in all_n_teams:
    wins = sum([cfb40dict[team]['ovr_win'] for team in n_team])
    proj_wins = sum([round(cfb40dict[team]['projected_wins']) for team in n_team])
    if wins <= n8wins:
        if proj_wins > cfb40max_predicted_wins:
            print("##### MAX {} #####".format(proj_wins))
            print_selection(data, data, data, n_team)
            print("##################")
            print("")
    if wins >= n8wins:
        if proj_wins < cfb40min_predicted_wins:
            print("----- min {} -----".format(proj_wins))
            print_selection(data, data, data, n_team)
            print("------------------")
            print("")
