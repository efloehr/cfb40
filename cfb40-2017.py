import lxml.html
import requests
import itertools
import collections

BASE_URL = 'http://www.espn.com/college-football/standings/_/season/'
STANDINGS_2016_URL = BASE_URL + '2016'
TEAM_REC_HEADERS = ['ovr_win', 'ovr_loss', 'pf', 'pa', 'home_win', 'home_loss', 'away_win', 'away_loss', 'ap_win',
                    'ap_loss', 'usa_win', 'usa_loss']
POWER_FIVE_CONFS = ['Atlantic Coast Conference', 'Big 12 Conference', 'Big Ten Conference', 'Pac-12 Conference',
                    'Southeastern Conference']

# From 
POWER_REPORT_WINS = [
[1,'Alabama',22.7,10.1],
[6,'Auburn',14.3,8.2],
[10,'LSU',13.0,7.8],
[18,'Georgia',9.7,7.2],
[19,'Florida',9.6,7.3],
[20,'Texas A&M',9.4,7.2],
[21,'Tennessee',9.2,7.4],
[27,'Ole Miss',7.9,7.0],
[35,'Vanderbilt',6.3,6.6],
[38,'Mississippi State',6.0,6.2],
[41,'Arkansas',5.2,6.3],
[42,'Kentucky',5.0,6.6],
[49,'South Carolina',3.5,5.4],
[58,'Missouri',1.9,6.1],
[4,'Ohio State',16.9,9.8],
[8,'Wisconsin',13.6,9.6],
[9,'Michigan',13.1,8.8],
[12,'Penn State',12.0,8.7],
[29,'Iowa',7.2,7.5],
[32,'Northwestern',6.9,7.9],
[40,'Minnesota',5.2,7.5],
[52,'Nebraska',2.4,6.0],
[53,'Indiana',2.4,6.5],
[72,'Michigan State',-0.6,4.6],
[77,'Maryland',-2.0,4.2],
[104,'Purdue',-8.1,2.9],
[105,'Rutgers',-8.1,4.0],
[114,'Illinois',-9.3,3.0],
[5,'Oklahoma',16.1,9.5],
[23,'TCU',8.6,7.8],
[30,'Baylor',7.2,7.6],
[31,'Oklahoma State',7.0,7.2],
[33,'Kansas State',6.8,7.5],
[37,'Texas',6.1,6.9],
[44,'Texas Tech',4.2,6.2],
[63,'West Virginia',1.0,5.7],
[80,'Iowa State',-3.1,4.1],
[120,'Kansas',-11.2,2.6],
[2,'Clemson',18.4,9.5],
[3,'Florida State',18.2,9.1],
[13,'Miami',11.6,8.2],
[14,'Louisville',11.6,8.3],
[15,'Georgia Tech',9.9,7.3],
[17,'Virginia Tech',9.7,8.0],
[25,'NC State',8.3,6.9],
[26,'North Carolina',8.3,7.3],
[36,'Pittsburgh',6.2,6.5],
[45,'Duke',3.9,5.6],
[51,'Syracuse',2.6,5.4],
[59,'Wake Forest',1.7,5.0],
[65,'Boston College',0.4,4.8],
[76,'Virginia',-1.6,4.6],
[7,'Stanford',13.6,8.9],
[11,'Washington',12.4,9.1],
[16,'USC',9.7,7.8],
[22,'Washington State',9.0,8.0],
[34,'Oregon',6.4,7.2],
[39,'UCLA',5.5,6.3],
[46,'Utah',3.9,6.1],
[50,'Colorado',3.3,6.5],
[60,'Arizona State',1.5,5.4],
[66,'Oregon State',0.2,4.7],
[69,'Arizona',-0.3,5.4],
[71,'California',-0.6,4.3],
]

# ESPN Win Predictions from http://www.espn.com/college-football/statistics/teamratings/_/year/2017/key/20170826040000
ESPN_WINS = [
[1,'Ohio State',11.9,1,34.8,69.5,49,29.3],
[2,'Alabama',10.8,1.8,10.5,48.9,12,26.2],
[3,'Florida State',10.2,2.3,5.1,38.5,13,23.2],
[4,'Oklahoma',10.8,2.1,4.5,71.7,35,23],
[5,'Auburn',9.7,2.7,2.6,23.5,18,21.8],
[6,'Clemson',9.6,2.7,2.8,26.1,20,19.9],
[7,'Washington',10.3,2.3,4.8,30.6,46,19],
[8,'Penn State',9.8,2.3,1.4,6.3,60,18.2],
[9,'Wisconsin',10.6,2.2,4.1,20.1,63,17.7],
[10,'Stanford',9.2,3.1,1.3,18.9,7,17],
[11,'USC',9.3,3.4,1,34.9,6,16.6],
[12,'LSU',8.3,3.8,0.2,3.6,5,16.4],
[13,'Georgia',8.5,3.9,0.2,11.7,2,15.9],
[14,'Michigan',8.4,3.6,0.1,2,55,14.1],
[15,'Louisville',8.6,3.5,0.4,5.4,59,13.8],
[16,'TCU',8.7,3.7,0.3,11.9,39,13.8],
[17,'Florida',7.8,4.5,0.1,6.8,4,13.8],
[18,'Miami',8.9,3.6,0.2,17.3,43,13.5],
[19,'Notre Dame',8.1,3.9,0.3,0,21,13.2],
[20,'NC State',7.8,4.3,0.1,4.3,14,12.6],
[21,'UCLA',7.7,4.5,0,6.9,9,12.4],
[22,'Tennessee',7.8,4.4,0,2.9,31,12.3],
[23,'Washington State',8.2,3.9,0.2,4.2,40,12],
[24,'Oregon',8,4.1,0.1,3,44,11.2],
[25,'Texas',7.6,4.6,0,5.4,29,11],
[26,'Oklahoma State',7.9,4.3,0,5.9,28,10.9],
[27,'Texas A&M',6.6,5.4,0,0.4,16,9.8],
[28,'North Carolina',7.6,4.6,0,3.1,41,9.2],
[29,'Northwestern',8.4,3.8,0.1,1.6,65,9],
[30,'Kansas State',7.5,4.6,0,2.8,50,8.8],
[31,'Virginia Tech',8,4.2,0.1,3.3,57,8.6],
[32,'South Carolina',6.2,5.8,0,0.9,3,8.3],
[33,'Mississippi State',6.2,5.8,0,0.1,15,7.9],
[34,'Baylor',7.1,5,0,1.7,47,7.8],
[35,'Kentucky',6.5,5.5,0,0.7,32,6.6],
[36,'Ole Miss',6.4,5.6,0,0.1,37,6.1],
[37,'Arkansas',5.9,6.1,0,0.1,30,6],
[38,'Georgia Tech',6,6.1,0,1.2,10,5.9],
[39,'Missouri',6.7,5.4,0,0.4,52,5.9],
[40,'Iowa',6.8,5.2,0,0.2,56,5.6],
[41,'Colorado',6.6,5.5,0,0.8,51,5.2],
[43,'Vanderbilt',5.5,6.5,0,0.1,17,4.5],
[45,'BYU',8.6,4.4,0.1,0,71,4.1],
[46,'Arizona State',5.3,6.7,0,0.4,8,3.8],
[47,'Pittsburgh',5.6,6.4,0,0.4,27,3.6],
[48,'Syracuse',5.5,6.5,0,0,34,3.5],
[49,'Nebraska',6.1,5.9,0,0.2,53,3.4],
[51,'Texas Tech',5.3,6.7,0,0.3,23,2.7],
[52,'West Virginia',5.6,6.4,0,0.3,38,2.7],
[53,'Duke',5.4,6.6,0,0.3,26,2.7],
[54,'Oregon State',5.1,7,0,0.1,19,2.3],
[55,'Arizona',5.7,6.3,0,0.2,48,1.9],
[57,'Utah',4.7,7.3,0,0.1,11,1.6],
[58,'Wake Forest',4.8,7.2,0,0,22,1.3],
[59,'Indiana',6,6,0,0,62,1.2],
[60,'Michigan State',5.1,6.9,0,0,36,0.8],
[65,'Iowa State',4.4,7.6,0,0,25,1],
[66,'Minnesota',5.6,6.4,0,0,64,1.2],
[67,'Boston College',4.4,7.6,0,0,33,1.6],
[68,'California',3.4,8.6,0,0,1,1.8],
[71,'Maryland',4.1,7.9,0,0,24,2.3],
[73,'Virginia',4.7,7.3,0,0,54,2.7],
[74,'Army',7.6,4.4,0.0,0,102,-2.8],
[86,'Illinois',3.8,8.2,0,0,61,7.1],
[90,'Rutgers',3.8,8.2,0,0,58,8.2],
[96,'Purdue',2.7,9.3,0,0,42,9.4],
[99,'Kansas',2.9,9.1,0,0,45,9.8],
[111,'UMass',4.3,7.7,0.0,0,76,-12.2],
]


POWER_REPORT_WIN_DICT = {}
for power_team in POWER_REPORT_WINS:
    POWER_REPORT_WIN_DICT[power_team[1]] = power_team[3]

ESPN_WIN_DICT = {}
for espn_team in ESPN_WINS:
    ESPN_WIN_DICT[espn_team[1]] = espn_team[2]
    
def get_win_loss(win_loss_element):
    win_loss_text = win_loss_element.text
    wins = losses = 0
    if win_loss_text != '--':
        wins, losses = win_loss_text.split('-')
    return wins, losses

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
            ovr_win, ovr_loss = get_win_loss(data[3])
            pf = data[4].text
            pa = data[5].text
            home_win, home_loss = get_win_loss(data[6])
            away_win, away_loss = get_win_loss(data[7])
            ap_win, ap_loss = get_win_loss(data[9])
            usa_win, usa_loss = get_win_loss(data[10])
            raw_data = [int(x) for x in
                        [ovr_win, ovr_loss, pf, pa, home_win, home_loss, away_win, away_loss, ap_win, ap_loss, usa_win,
                         usa_loss]]
            team_data.append(dict(zip(TEAM_REC_HEADERS, raw_data)))

        team_dict_by_conf.append(dict(zip(team_names, team_data)))

    conference_dict = dict(zip(conference_names, team_dict_by_conf))

    return conference_dict

def get_power5_data(url, include_ind = False):
    conference_data = get_cfb_data(url)
    conferences = POWER_FIVE_CONFS
    if include_ind:
        conferences += ['FBS Independents']
    power_five_teams = {team: data for conf_team in [conference_data[conf] for conf in conferences] for team, data in conf_team.items()}
    return power_five_teams

def print_selection(teams, data):
    for team in teams:
        w2016 = power5_2016[team]['ovr_win']
        w2017 = ESPN_WIN_DICT[team]
        print("{0:<16} {1:>2d} -> {2:>2.1f}".format(team, w2016, w2017))

    print("{0:<16} {1:>2d} -> {2:>2.1f}".format("TOTAL:", data['2016'], data['2017_raw']))


# Get power 5 win loss last year
power5_2016 = get_power5_data(STANDINGS_2016_URL, True)

# Verify team names are the same
for team_name in power5_2016.keys():
    if team_name not in POWER_REPORT_WIN_DICT.keys():
        print("{0} not in POWER win data".format(team_name))
for team_name in power5_2016.keys():
    if team_name not in ESPN_WIN_DICT.keys():
        print("{0} not in ESPN win data".format(team_name))

# Get all combinations of 5 teams
all_five_teams = itertools.combinations(power5_2016.keys(), 5)

# Get all combinations of 5 teams with 40 wins or less
forty_or_less_five_teams = {}
forty_or_more_five_teams = {}
cfb40max_selection = None
cfb40max_data = None
cfb40max_predicted_wins = 0
cfb40min_selection = None
cfb40min_data = None
cfb40min_predicted_wins = 999999

for five_team in all_five_teams:
    wins_2016 = [power5_2016[team]['ovr_win'] for team in five_team]
    wins_2017 = [ESPN_WIN_DICT[team] for team in five_team]
    total_wins_2016 = sum(wins_2016)
    total_wins_2017 = sum(wins_2017)
    total_wins_2017_int = int(round(total_wins_2017))
    data = {'2016': total_wins_2016, '2017_raw': total_wins_2017, '2017': total_wins_2017_int}
    if total_wins_2016 <= 40:
        forty_or_less_five_teams[five_team] = data
        if total_wins_2017 > cfb40max_predicted_wins:
            cfb40max_selection = five_team
            cfb40max_data = data
            cfb40max_predicted_wins = total_wins_2017
    if total_wins_2016 >= 40:
        forty_or_more_five_teams[five_team] = data
        if total_wins_2017 < cfb40min_predicted_wins:
            cfb40min_selection = five_team
            cfb40min_data = data
            cfb40min_predicted_wins = total_wins_2017
    #if total_wins_2017 >= 48:
        #print_selection(five_team, data)
        #print()
            
        
print("Total of {} combinations of 5 teams with 40 wins or less last year".format(len(forty_or_less_five_teams)))
print("Total of {} combinations of 5 teams with 40 wins or more last year".format(len(forty_or_more_five_teams)))

print()
print("My CFB40 Max selection:")
print_selection(cfb40max_selection, cfb40max_data)

print()
print("My CFB40 Min selection:")
print_selection(cfb40min_selection, cfb40min_data)