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
        "Air Force Falcons": "Air Force",
        "Akron Zips": "Akron",
        "Alabama Crimson Tide": "Alabama",
        "Appalachian State Mountaineers": "Appalachian St",
        "Arizona State Sun Devils": "Arizona State",
        "Arizona Wildcats": "Arizona",
        "Arkansas Razorbacks": "Arkansas",
        "Arkansas State Red Wolves": "Arkansas State",
        "Army Black Knights": "Army",
        "Auburn Tigers": "Auburn",
        "BYU Cougars": "BYU",
        "Ball State Cardinals": "Ball State",
        "Baylor Bears": "Baylor",
        "Boise State Broncos": "Boise State",
        "Boston College Eagles": "Boston College",
        "Bowling Green Falcons": "Bowling Green",
        "Buffalo Bulls": "Buffalo",
        "California Golden Bears": "Cal",
        "Central Michigan Chippewas": "Cent Michigan",
        "Charlotte 49ers": "Charlotte",
        "Cincinnati Bearcats": "Cincinnati",
        "Clemson Tigers": "Clemson",
        "Coastal Carolina Chanticleers": "C. Carolina",
        "Colorado Buffaloes": "Colorado",
        "Colorado State Rams": "Colorado State",
        "Duke Blue Devils": "Duke",
        "East Carolina Pirates": "ECU",
        "Eastern Michigan Eagles": "E Michigan",
        "Florida Atlantic Owls": "FAU",
        "Florida Gators": "Florida",
        "Florida Intl Golden Panthers": "FIU",
        "Florida State Seminoles": "FSU",
        "Fresno State Bulldogs": "Fresno State",
        "Georgia Bulldogs": "Georgia",
        "Georgia Southern Eagles": "Ga Southern",
        "Georgia State Panthers": "Georgia State",
        "Georgia Tech Yellow Jackets": "Georgia Tech",
        "Hawai'i Rainbow Warriors": "Hawai'i",
        "Houston Cougars": "Houston",
        "Idaho Vandals": "Idaho",
        "Liberty Flames": "Liberty",
        "Illinois Fighting Illini": "Illinois",
        "Indiana Hoosiers": "Indiana",
        "Iowa Hawkeyes": "Iowa",
        "Iowa State Cyclones": "Iowa State",
        "Kansas Jayhawks": "Kansas",
        "Kansas State Wildcats": "Kansas State",
        "Kent State Golden Flashes": "Kent State",
        "Kentucky Wildcats": "Kentucky",
        "LSU Tigers": "LSU",
        "Louisiana Monroe Warhawks": "UL Monroe",
        "Louisiana Ragin' Cajuns": "Louisiana",
        "Louisiana Tech Bulldogs": "LA Tech",
        "Louisville Cardinals": "Louisville",
        "Marshall Thundering Herd": "Marshall",
        "Maryland Terrapins": "Maryland",
        "Memphis Tigers": "Memphis",
        "Miami (OH) RedHawks": "Miami (OH)",
        "Miami Hurricanes": "Miami",
        "Michigan State Spartans": "Mich. St.",
        "Michigan Wolverines": "Michigan",
        "Middle Tennessee Blue Raiders": "Mid Tennessee",
        "Minnesota Golden Gophers": "Minnesota",
        "Mississippi State Bulldogs": "Miss St",
        "Missouri Tigers": "Missouri",
        "NC State Wolfpack": "NC State",
        "Navy Midshipmen": "Navy",
        "Nebraska Cornhuskers": "Nebraska",
        "Nevada Wolf Pack": "Nevada",
        "New Mexico Lobos": "New Mexico",
        "New Mexico State Aggies": "New Mexico St",
        "North Carolina Tar Heels": "UNC",
        "North Texas Mean Green": "North Texas",
        "Northern Illinois Huskies": "N Illinois",
        "Northwestern Wildcats": "Northwestern",
        "Notre Dame Fighting Irish": "Notre Dame",
        "Ohio Bobcats": "Ohio",
        "Ohio State Buckeyes": "Ohio State",
        "Oklahoma Sooners": "Oklahoma",
        "Oklahoma State Cowboys": "Oklahoma State",
        "Old Dominion Monarchs": "Old Dominion",
        "Ole Miss Rebels": "Ole Miss",
        "Oregon Ducks": "Oregon",
        "Oregon State Beavers": "Oregon St",
        "Penn State Nittany Lions": "Penn State",
        "Pittsburgh Panthers": "Pitt",
        "Purdue Boilermakers": "Purdue",
        "Rice Owls": "Rice",
        "Rutgers Scarlet Knights": "Rutgers",
        "SMU Mustangs": "SMU",
        "San Diego State Aztecs": "San Diego State",
        "San Jose State Spartans": "San Jose State",
        "South Alabama Jaguars": "South Alabama",
        "South Carolina Gamecocks": "S Carolina",
        "South Florida Bulls": "USF",
        "Southern Mississippi Golden Eagles": "Southern Miss",
        "Stanford Cardinal": "Stanford",
        "Syracuse Orange": "Syracuse",
        "TCU Horned Frogs": "TCU",
        "Temple Owls": "Temple",
        "Tennessee Volunteers": "Tennessee",
        "Texas A&M Aggies": "Texas A&M",
        "Texas Longhorns": "Texas",
        "Texas State Bobcats": "Texas State",
        "Texas Tech Red Raiders": "Texas Tech",
        "Toledo Rockets": "Toledo",
        "Troy Trojans": "Troy",
        "Tulane Green Wave": "Tulane",
        "Tulsa Golden Hurricane": "Tulsa",
        "UAB Blazers": "UAB",
        "UCF Knights": "UCF",
        "UCLA Bruins": "UCLA",
        "UConn Huskies": "UConn",
        "UMass Minutemen": "UMass",
        "UNLV Rebels": "UNLV",
        "USC Trojans": "USC",
        "UT San Antonio Roadrunners": "UTSA",
        "UTEP Miners": "UTEP",
        "Utah State Aggies": "Utah State",
        "Utah Utes": "Utah",
        "Vanderbilt Commodores": "Vanderbilt",
        "Virginia Cavaliers": "UVA",
        "Virginia Tech Hokies": "VT",
        "Wake Forest Demon Deacons": "Wake Forest",
        "Washington Huskies": "Washington",
        "Washington State Cougars": "Washington St",
        "West Virginia Mountaineers": "West Virginia",
        "Western Kentucky Hilltoppers": "W Kentucky",
        "Western Michigan Broncos": "W Michigan",
        "Wisconsin Badgers": "Wisconsin",
        "Wyoming Cowboys": "Wyoming",
    }


def get_espn_standings_data(year):
    url = ESPN_STANDINGS_URL.format(year=year)
    html = requests.get(url)

    htmldoc = lxml.html.document_fromstring(html.text)

    conferences = htmldoc.find_class('Table2__Title')

    teams_by_conference = htmldoc.find_class('Table2__table__wrapper')

    if len(conferences) != len(teams_by_conference):
        print("Teams and conference number not equal! {0} vs {1}".format(len(conferences), len(teams_by_conference)))
        exit(1)

    conference_names = [conference.text for conference in conferences]

    team_dict_by_conf = []

    team_data = []
    for conf_index, conf in enumerate(teams_by_conference):
        team_names = [name.text_content() for name in conf.xpath('.//span[@class="hide-mobile"]')]

        team_names = [team if team not in ESPN_STANDINGS_TEAM_CONVERSION.keys()
                        else ESPN_STANDINGS_TEAM_CONVERSION[team] for team in team_names]

        raw_team_data = conf.xpath('.//tbody[@class="Table2__tbody"]')[1].xpath('.//tr')

        # Remove headers
        raw_team_data = [data for data in raw_team_data if data[0].text_content() != 'W-L']

        for team_index, data in enumerate(raw_team_data):
            ovr_win, ovr_loss = __get_espn_win_loss(data[3])
            pf = data[4].text_content()
            pa = data[5].text_content()
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
    win_loss_text = win_loss_element.text_content()
    wins = losses = 0
    if win_loss_text != '--':
        wins, losses = win_loss_text.split('-')
    return wins, losses


ESPN_PI_URL = "http://www.espn.com/college-football/statistics/teamratings/_/year/{year}/key/{week}"
ESPN_PI = {
    2017:
        [
            '20170826040000',
            '20170904040000',
            '20170911040000',
            '20170918040000',
            '20170925040000',
            '20171002040000',
            '20171009040000',
            '20171016040000',
            '20171023040000',
            '20171030040000',
            '20171106040000',
            '20171113040000',
            '20171120040000',
            '20171127040000',
            '20171204040000',
            '20171211040000',
            '20180109040000',
        ],
    2018:
        [
            '20180825040000',
            '20180903040000',
            '20180910040000',
            '20180917040000',
            '20180924040000',
            '20181001040000',
            '20181007040000',
            '20181015040000',
            '20181022040000',
            '20181029040000',
        ]
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

