import itertools


def print_selection(data, last_week_data, preseason_data, teams):
    if last_week_data is None:
        last_week_data = preseason_data
    for team in sorted(teams):
        team_data = data.ix[team]
        proj_this_week = data.ix[team]['projected_wins']
        proj_last_week = last_week_data.ix[team]['projected_wins']
        proj_preseason = preseason_data.ix[team]['projected_wins']
        games_last_week = last_week_data.ix[team]['wins'] + last_week_data.ix[team]['losses']
        games_this_week = data.ix[team]['wins'] + data.ix[team]['losses']
        new_wins = data.ix[team]['wins'] - last_week_data.ix[team]['wins']
        if games_this_week == games_last_week:
            new_wins = '-'
        else:
            new_wins = str(new_wins)
        print("{0:<16} [{9:1s}] [{2:>2d}-{3:>2d}] {1:>2d} -> {4:>4.1f} / {5:>4.1f} (net {6:>+3.1f}) / {7:>4.1f} (net {8:>+5.1f})".format(
            team_data['team'], team_data['ovr_win'], team_data['wins'], team_data['losses'],
            proj_this_week, proj_last_week, proj_this_week - proj_last_week, proj_preseason, proj_this_week - proj_preseason,
            new_wins))

    wins = sum([data.ix[team]['ovr_win'] for team in teams])
    proj_wins_this_week = sum([data.ix[team]['projected_wins'] for team in teams])
    proj_wins_last_week = sum([last_week_data.ix[team]['projected_wins'] for team in teams])
    proj_wins_preseason = sum([preseason_data.ix[team]['projected_wins'] for team in teams])
    current_wins = sum([data.ix[team]['wins'] for team in teams])
    current_losses = sum([data.ix[team]['losses'] for team in teams])

    print("{0:<16}     [{2:>2d}-{3:>2d}] {1:>2d} -> {4:>4.1f} / {5:>4.1f} (net {6:>+3.1f}) / {7:>4.1f} (net {8:>+5.1f})".format(
        "TOTAL:", wins, current_wins, current_losses,
        proj_wins_this_week, proj_wins_last_week, proj_wins_this_week - proj_wins_last_week,
        proj_wins_preseason, proj_wins_this_week - proj_wins_preseason))


# Get power 5 win loss last year
def make_power5_data(data):
    return data[data.conference.isin(['Atlantic Coast Conference','Big Ten Conference', 'Big 12 Conference', 'FBS Independents', 'Pac-12 Conference', 'Southeastern Conference'])]


def make_cfb_data(data):
    power5_data = make_power5_data(data)
    return power5_data[~power5_data.team.isin(['Army','UMass','BYU'])]


def calculate_best_cfbNmax_and_min_teams(data, num_teams):
    cfbframe = make_cfb_data(data)
    cfbdict = cfbframe.to_dict(orient='index')

    # Get all combinations of n teams
    all_n_teams = itertools.combinations(cfbdict.keys(), num_teams)

    # Get all combinations of num_teams teams with 8n wins or less
    cfbmax_selection = None
    cfbmax_predicted_wins = 0
    cfbmin_selection = None
    cfbmin_predicted_wins = 999999

    n8wins = num_teams * 8

    for n_team in all_n_teams:
        wins = sum([cfbdict[team]['ovr_win'] for team in n_team])
        proj_wins = sum([cfbdict[team]['projected_wins'] for team in n_team])
        if wins <= n8wins:
            if proj_wins > cfbmax_predicted_wins:
                cfbmax_selection = n_team
                cfbmax_predicted_wins = proj_wins
        if wins >= n8wins:
            if proj_wins < cfbmin_predicted_wins:
                cfbmin_selection = n_team
                cfbmin_predicted_wins = proj_wins

    return cfbmax_selection, cfbmin_selection
