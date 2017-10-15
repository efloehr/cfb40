import itertools


def print_selection(data, teams):
    for team in sorted(teams):
        team_data = data.ix[team]
        print("{0:<16} [{3:>2d}-{4:>2d}] {1:>2d} -> {2:>4.1f}".format(
            team_data['team'], team_data['ovr_win'], team_data['projected_wins'],
            team_data['wins'], team_data['losses']))

    wins = sum([data.ix[team]['ovr_win'] for team in teams])
    proj_wins = sum([data.ix[team]['projected_wins'] for team in teams])
    current_wins = sum([data.ix[team]['wins'] for team in teams])
    current_losses = sum([data.ix[team]['losses'] for team in teams])

    print("{0:<16} [{3:>2d}-{4:>2d}] {1:>2d} -> {2:>4.1f}".format(
        "TOTAL:", wins, proj_wins, current_wins, current_losses))


# Get power 5 win loss last year
def make_power5_data(data):
    return data[data.conference.isin(['Atlantic Coast Conference','Big Ten Conference', 'Big 12 Conference', 'FBS Independents', 'Pac-12 Conference', 'Southeastern Conference'])]


def make_cfb40_data(data):
    power5_data = make_power5_data(data)
    return power5_data[~power5_data.team.isin(['Army','UMass'])]


def calculate_best_cfb40max_and_min_teams(data, num_teams):
    cfb40frame = make_cfb40_data(data)
    cfb40dict = cfb40frame.to_dict(orient='index')

    # Get all combinations of n teams
    all_n_teams = itertools.combinations(cfb40dict.keys(), num_teams)

    # Get all combinations of 5 teams with 8n wins or less
    cfb40max_selection = None
    cfb40max_predicted_wins = 0
    cfb40min_selection = None
    cfb40min_predicted_wins = 999999

    n8wins = num_teams * 8

    for n_team in all_n_teams:
        wins = sum([cfb40dict[team]['ovr_win'] for team in n_team])
        proj_wins = sum([cfb40dict[team]['projected_wins'] for team in n_team])
        if wins <= n8wins:
            if proj_wins > cfb40max_predicted_wins:
                cfb40max_selection = n_team
                cfb40max_predicted_wins = proj_wins
        if wins >= n8wins:
            if proj_wins < cfb40min_predicted_wins:
                cfb40min_selection = n_team
                cfb40min_predicted_wins = proj_wins

    return cfb40max_selection, cfb40min_selection
