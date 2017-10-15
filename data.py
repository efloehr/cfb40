import lxml.html
import requests
import itertools
import collections
import pandas as pd

# ESPN Standings by Year

ESPN_STANDINGS_URL = 'http://www.espn.com/college-football/standings/_/season/{year}'

TEAM_REC_HEADERS = ['ovr_win', 'ovr_loss', 'pf', 'pa', 'home_win', 'home_loss', 'away_win', 'away_loss', 'ap_win',
                    'ap_loss', 'usa_win', 'usa_loss', 'team', 'conference']

POWER_FIVE_CONFS = ['Atlantic Coast Conference', 'Big 12 Conference', 'Big Ten Conference', 'Pac-12 Conference',
                    'Southeastern Conference']

ESPN_STANDINGS_TEAM_CONVERSION = \
    {
        'Appalachian State': 'Appalachian St',
#        'C. Carolina':,
        'California': 'Cal',
        'Central Michigan': 'Cent Michigan',
        'Eastern Michigan': 'E Michigan',
        'East Carolina': 'ECU',
        'Florida Atlantic': 'FAU',
        'Florida Intl': 'FIU',
        'Florida State': 'FSU',
        'Georgia Southern': 'Ga Southern',
        'Louisiana Tech': 'LA Tech',
        'Middle Tennessee': 'Mid Tennessee',
        'Mississippi State': 'Miss St',
        'Northern Illinois': 'N Illinois',
        'New Mexico State': 'New Mexico St',
        'Ohio State': 'OSU',
        'Pittsburgh': 'Pitt',
        'San José State': 'San Jose State',
        'Southern Mississippi': 'Southern Miss',
 #       'UAB',
        'Connecticut': 'UConn',
        'Louisiana Monroe': 'UL Monroe',
        'North Carolina': 'UNC',
        'South Florida': 'USF',
        'UT San Antonio': 'UTSA',
        'Virginia': 'UVA',
        'Virginia Tech': 'VT',
        'Western Kentucky': 'W Kentucky',
        'Western Michigan': 'W Michigan',
        'Washington State': 'Washington St',
    }


def get_espn_standings_data(year):
    url = ESPN_STANDINGS_URL.format(year=year)
    html = requests.get(url)

    htmldoc = lxml.html.document_fromstring(html.text)

    conferences = htmldoc.find_class('long-caption')

    teams_by_conference = htmldoc.xpath('//table')

    if len(conferences) != len(teams_by_conference):
        print("Teams and conference number not equal! {0} vs {1}".format(len(conferences), len(teams_by_conference)))
        exit(1)

    conference_names = [conference.text for conference in conferences]

    team_dict_by_conf = []

    team_data = []
    for conf_index, conf in enumerate(teams_by_conference):
        team_names = [name.text for name in conf.xpath('.//tr//span[@class="team-names"]')]
        team_names = [team if team not in ESPN_STANDINGS_TEAM_CONVERSION.keys()
                        else ESPN_STANDINGS_TEAM_CONVERSION[team] for team in team_names]
        raw_team_data = [data[1:] for data in conf.xpath('.//tr')[1:]]
        for team_index, data in enumerate([data for data in raw_team_data if len(data) != 3]):
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
            raw_data += [team_names[team_index], conference_names[conf_index]]
            team_data.append(raw_data)

    team_data = pd.DataFrame(team_data, columns=TEAM_REC_HEADERS).set_index('team')
    return team_data


def __get_espn_win_loss(win_loss_element):
    win_loss_text = win_loss_element.text
    wins = losses = 0
    if win_loss_text != '--':
        wins, losses = win_loss_text.split('-')
    return wins, losses


ESPN_PI_URL = "http://www.espn.com/college-football/statistics/teamratings/_/year/{year}/key/{week}"
ESPN_PI = {2017:
                [
                    '20170826040000',
                    '20170904040000',
                    '20170911040000',
                    '20170918040000',
                    '20170925040000',
                    '20171002040000',
                    '20171009040000',
                    '20171015040000',
                ],
}


def get_espn_power_index_data(year, week_number):
    week = ESPN_PI[year][week_number]
    url = ESPN_PI_URL.format(year=year, week=week)

    table = pd.read_html(url)[0]

    # Drop header rows
    table = table.drop(table.index[[0, 1]])

    # Create true header names
    table.columns = ['rank', 'team_conf', 'win_loss', 'projected_win_loss', 'win_out_pct', 'conf_win_pct',
                     'remaining_SOS_rank', 'FPI']

    # Split team name from conference name
    team_and_conference = table['team_conf'].str.split(',', 1, expand=True)
    team_and_conference.columns = ['team', 'conference']

    # Split Win Loss
    win_and_loss = table['win_loss'].str.split('-', 1, expand=True)
    win_and_loss.columns = ['wins', 'losses']

    # Split Projected Win Loss
    proj_win_and_loss = table['projected_win_loss'].str.split(' - ', 1, expand=True)
    proj_win_and_loss.columns = ['projected_wins', 'projected_losses']

    # Combine
    new_table = pd.concat([table, team_and_conference['team'], win_and_loss, proj_win_and_loss], axis=1).set_index('team', drop=False)

    # Drop more header rows
    new_table = new_table.drop('TEAM')

    # Make numeric where possible
    new_table = new_table.apply(pd.to_numeric, errors='ignore')

    return new_table


def get_cfb_data(year, week):
    standings = get_espn_standings_data(year-1)
    power = get_espn_power_index_data(year, week)
    return pd.concat([standings, power], axis=1, join='inner')

