from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import io


def get_dst_data(year, week):
    '''Gathers the stats for every pplayer at a position for a given
    year and week'''

    # Creates the url to scrape
    url = 'https://www.footballdb.com/fantasy-football/index.html?pos=DST&yr='
    url += str(year) + '&wk=' + str(week) + '&rules=2'

    # Opens the url
    req = Request(url)
    page = urlopen(req).read()
    week_data = BeautifulSoup(page, "html.parser")
    # Grabs the data rows by isolating the <tr>s and saves them in an
    # list called players
    player_rows = week_data.find_all('tr', 'right')
    # Removes the header row that names the columns
    player_rows.pop(0)

    # loops through players to grab their individual stats
    for player in player_rows:
        player_stats = list()
        stat = None
        stats = player.find_all('td')
        for stat in stats:
            # Checks if its the first item, if it is, it further digs
            # into the <a> element, so that it gets just the name
            if len(player_stats) == 0:
                player_stats.append(stat.find('a').text)
            # Next it checks if its the second item, which is the home
            # and away item in the form: team1@team2
            elif len(player_stats) == 1:
                opponent = stat.text.split('@ ')
                home = 0
                if len(opponent) < 2:
                    opponent = stat.text.split('vs. ')
                    home = 1
                player_stats.append(opponent[1])
                player_stats.append(home)
            # For the other items, it just adds it to the player_stats
            # list normally
            else:
                player_stats.append(stat.text)
        # calculates the fantasy points that player would have put up
        # using my league's scoring system

        if int(player_stats[10]) > 34:
            pa = -4
        elif int(player_stats[10]) > 27:
            pa = -1
        elif int(player_stats[10]) > 20:
            pa = 0
        elif int(player_stats[10]) > 13:
            pa = 1
        elif int(player_stats[10]) > 6:
            pa = 4
        elif int(player_stats[10]) > 0:
            pa = 7
        else:
            pa = 10
        if int(player_stats[13]) > 499:
            payds = -3
        elif int(player_stats[13]) > 99:
            payds = 0
        else:
            payds = 3

        points = float(player_stats[4]) + (2 * float(player_stats[5]))
        points += (2 * float(player_stats[6])) + (2 * float(player_stats[7]))
        points += (float(player_stats[8]) * 2) + (float(player_stats[9]) * 6)
        points += pa + payds
        data_file = 'data/dst_data.csv'
        # writes the stats to that position's csv file
        with io.open(data_file, 'a', newline='') as stat_file:
            stat_writer = csv.writer(stat_file)
            # team  opp home pts Sack	Int	Saf	FR	Blk	TD	PA	PassYds
            # RushYds	TotYds
            stat_writer.writerow([year, week, player_stats[0],
                                  player_stats[1], player_stats[2],
                                  player_stats[4], player_stats[5],
                                  player_stats[6], player_stats[7],
                                  player_stats[8], player_stats[9],
                                  player_stats[10], player_stats[13],
                                  str(round(points, 2))])
        stat_file.close()
