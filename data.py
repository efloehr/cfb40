import lxml.html
import requests
import itertools
import collections

# ESPN Standings by Year

BASE_URL = 'http://www.espn.com/college-football/standings/_/season/'

STANDINGS_2015_URL = BASE_URL + '2015'
STANDINGS_2016_URL = BASE_URL + '2016'
STANDINGS_2017_URL = BASE_URL + '2017'

TEAM_REC_HEADERS = ['ovr_win', 'ovr_loss', 'pf', 'pa', 'home_win', 'home_loss', 'away_win', 'away_loss', 'ap_win',
                    'ap_loss', 'usa_win', 'usa_loss']

POWER_FIVE_CONFS = ['Atlantic Coast Conference', 'Big 12 Conference', 'Big Ten Conference', 'Pac-12 Conference',
                    'Southeastern Conference']


def get_espn_standings_data(url, cache=True):
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
            ovr_win, ovr_loss = __get_espn_win_loss(data[3])
            pf = data[4].text
            pa = data[5].text
            home_win, home_loss = __get_espn_win_loss(data[6])
            away_win, away_loss = __get_espn_win_loss(data[7])
            ap_win, ap_loss = __get_espn_win_loss(data[9])
            usa_win, usa_loss = __get_espn_win_loss(data[10])
            raw_data = [int(x) for x in
                        [ovr_win, ovr_loss, pf, pa, home_win, home_loss, away_win, away_loss, ap_win, ap_loss, usa_win,
                         usa_loss]]
            team_data.append(dict(zip(TEAM_REC_HEADERS, raw_data)))

        team_dict_by_conf.append(dict(zip(team_names, team_data)))

    conference_dict = dict(zip(conference_names, team_dict_by_conf))

    return conference_dict


def get_power5_espn_stnadings(url, include_ind = False):
    conference_data = get_cfb_data(url)
    conferences = POWER_FIVE_CONFS
    if include_ind:
        conferences += ['FBS Independents']
    power_five_teams = {team: data for conf_team in [conference_data[conf] for conf in conferences] for team, data in conf_team.items()}
    return power_five_teams


def __get_espn_win_loss (win_loss_element):
    win_loss_text = win_loss_element.text
    wins = losses = 0
    if win_loss_text != '--':
        wins, losses = win_loss_text.split('-')
    return wins, losses

