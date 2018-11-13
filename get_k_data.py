from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import io
import os

path_files = '/var/www/llfantasy.com/public_html/'


def get_k_data(year, week):
    '''Gathers the stats for every pplayer at a position for a given
    year and week'''

    # Creates the url to scrape
    url = 'https://www.footballdb.com/fantasy-football/index.html?pos=K&yr='
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
                team = stat.find('b').text
                player_stats.append(team)
                home_and_away = stat.text.replace("@", "")
                opponent = home_and_away.replace(team, "")
                player_stats.append(opponent)
                h_or_a = 0 if home_and_away.startswith(team) else 1
                player_stats.append(h_or_a)
            # For the other items, it just adds it to the player_stats
            # list normally
            else:
                player_stats.append(stat.text)
        # calculates the fantasy points that player would have put up
        # using my league's scoring system

        points = int(player_stats[6]) + (3 * int(player_stats[8]))
        data_file = 'data/k_data.csv'
        # writes the stats to that position's csv file
        with io.open(os.path.join(path_files, data_file), 'a', newline='') as stat_file:
            stat_writer = csv.writer(stat_file)
            stat_writer.writerow([year, week, player_stats[0],
                                  player_stats[1], player_stats[2],
                                  player_stats[3], player_stats[6],
                                  player_stats[8], str(round(points, 2))])
        stat_file.close()
