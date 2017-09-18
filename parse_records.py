import lxml.html
import requests
import itertools
import collections

BASE_URL = 'http://www.espn.com/college-football/standings/_/season/'
STANDINGS_2014_URL = BASE_URL + '2014'
STANDINGS_2015_URL = BASE_URL + '2015'
TEAM_REC_HEADERS = ['ovr_win', 'ovr_loss', 'pf', 'pa', 'home_win', 'home_loss', 'away_win', 'away_loss', 'ap_win',
                    'ap_loss', 'usa_win', 'usa_loss']
POWER_FIVE_CONFS = ['Atlantic Coast Conference', 'Big 12 Conference', 'Big Ten Conference', 'Pac-12 Conference',
                    'Southeastern Conference']

def get_cfb_data(url):
    html = requests.get(url)

    htmldoc = lxml.html.document_fromstring(html.text)

    conferences = htmldoc.find_class('long-caption')

    teams_by_conference = htmldoc.xpath('//table')

    if len(conferences) != len(teams_by_conference):
        print("Teams and conference number not equal! {0} vs {1}".format(len(conferences), len(teams_by_conference)))
        exit(1)

    conference_names = [conference.text for conference in conferences]

    team_dict_by_conf = []

    for conf in teams_by_conference:
        team_names = [name.text for name in conf.xpath('.//tr//span[@class="team-names"]')]
        raw_team_data = [data[1:] for data in conf.xpath('.//tr')[1:]]
        team_data = []
        for data in raw_team_data:
            if len(data) == 3:  # header
                continue
            ovr_win, ovr_loss = data[3].text.split('-')
            pf = data[4].text
            pa = data[5].text
            home_win, home_loss = data[6].text.split('-')
            away_win, away_loss = data[7].text.split('-')
            ap_win, ap_loss = data[9].text.split('-')
            usa_win, usa_loss = data[10].text.split('-')
            raw_data = [int(x) for x in
                        [ovr_win, ovr_loss, pf, pa, home_win, home_loss, away_win, away_loss, ap_win, ap_loss, usa_win,
                         usa_loss]]
            team_data.append(dict(zip(TEAM_REC_HEADERS, raw_data)))

        team_dict_by_conf.append(dict(zip(team_names, team_data)))

    conference_dict = dict(zip(conference_names, team_dict_by_conf))

    return conference_dict

def get_power5_data(url):
    conference_data = get_cfb_data(url)
    power_five_teams = {team: data for conf_team in [conference_data[conf] for conf in POWER_FIVE_CONFS] for team, data in conf_team.items()}
    return power_five_teams

power5_2014 = get_power5_data(STANDINGS_2014_URL)
power5_2015 = get_power5_data(STANDINGS_2015_URL)

print("Number of Power 5 Teams in 2014: {0}".format(len(power5_2014)))
print("Number of Power 5 Teams in 2015: {0}".format(len(power5_2015)))

all_five_teams = itertools.combinations(power5_2014.keys(), 5)

cfb40_teams = {}

for five_team in all_five_teams:
    wins_2014 = [power5_2014[team]['ovr_win'] for team in five_team]
    wins_2015 = [power5_2015[team]['ovr_win'] for team in five_team]
    total_wins_2014 = sum(wins_2014)
    total_wins_2015 = sum(wins_2015)
    if total_wins_2014 <= 40:
        if 'Alabama' not in five_team and 'Clemson' not in five_team and 'Michigan State' not in five_team and 'Oklahoma' not in five_team:
            cfb40_teams[five_team] = {'2014_wins': total_wins_2014, '2015_wins': total_wins_2015}

print("Number of 40 or less teams: {0}".format(len(cfb40_teams)))
print()

win_counts_2014_2015 = collections.Counter([(teams['2014_wins'], teams['2015_wins']) for teams in cfb40_teams.values()])
win_counts_2015 = collections.Counter([teams['2015_wins'] for teams in cfb40_teams.values()])

for wins, num in win_counts_2014_2015.items():
    print("{0},{1},{2}".format(wins[0], wins[1], num))

print()

def print_selection(teams, data):
    total2014 = 0
    total2015 = 0
    for team in teams:
        w2014 = power5_2014[team]['ovr_win']
        w2015 = power5_2015[team]['ovr_win']
        total2014 += w2014
        total2015 += w2015
        print("{0:<16} {1:>2d} -> {2:>2d}".format(team, w2014, w2015))

    print("{0:<16} {1:>2d} -> {2:>2d}".format("TOTAL:", total2014, total2015))

for cfb40_team, cfb40_team_data in cfb40_teams.items():
    if cfb40_team_data['2015_wins'] == 57:
        print_selection(cfb40_team, cfb40_team_data)
        print()

print(win_counts_2015)