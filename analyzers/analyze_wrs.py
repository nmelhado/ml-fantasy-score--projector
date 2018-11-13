import pandas
import pickle
import io
import os
import csv
from sklearn import linear_model

path_files = '/var/www/llfantasy.com/public_html/'


def analyze_wrs():
    '''Function that analyzes the WR data and creates a model from it.'''
    players = {}
    teams = {}
    opponents = {}
    with open(os.path.join(path_files, 'data/wr_data.csv')) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            players[row['name']] = 0
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    with io.open(os.path.join(path_files, 'computed/wr_data.csv'), 'w', newline='') as stat_file:
        stat_writer = csv.writer(stat_file)
        cats = ['year', 'week']
        for k, v in players.items():
            cats.append(k)
        for k, v in teams.items():
            cats.append(k)
        for k, v in opponents.items():
            cats.append(k)
        cats.extend(['home', 'pa_att', 'pa_cmp', 'pa_yds', 'pa_tds', 'pa_int',
                     'pa_2pts', 'ru_att', 'ru_yds', 'ru_tds', 'ru_2pts',
                     'rec_receptions', 'rec_yds', 'rec_tds', 'rec_2pts',
                     'fumb', 'fantasy points'])
        stat_writer.writerow(cats)
        with open(os.path.join(path_files, 'data/wr_data.csv')) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                players[row['name']] = 1
                teams[row['team']] = 1
                opponents[row['opponent']] = 1
                stats = [row['year'], row['week']]
                for k, v in players.items():
                    stats.append(v)
                for k, v in teams.items():
                    stats.append(v)
                for k, v in opponents.items():
                    stats.append(v)
                stats.extend([row['home'], row['pa_att'], row['pa_cmp'],
                              row['pa_yds'], row['pa_tds'], row['pa_int'],
                              row['pa_2pts'], row['ru_att'], row['ru_yds'],
                              row['ru_tds'], row['ru_2pts'],
                              row['rec_receptions'], row['rec_yds'],
                              row['rec_tds'], row['rec_2pts'], row['fumb'],
                              row['fantasy points']])
                stat_writer.writerow(stats)
                players[row['name']] = 0
                teams[row['team']] = 0
                opponents[row['opponent']] = 0

        f.close()
    stat_file.close()
    # loading the data as a panda
    df = pandas.read_csv(os.path.join(path_files, 'computed/wr_data.csv'), delimiter=",")

    # getting the dvs
    labels = ['pa_yds', 'pa_tds', 'pa_int', 'pa_2pts', 'ru_yds', 'ru_tds',
              'ru_2pts', 'rec_receptions', 'rec_yds', 'rec_tds', 'rec_2pts',
              'fumb']

    # getting the ivs
    features = df.drop(['year', 'pa_att', 'pa_cmp', 'pa_yds', 'pa_tds',
                        'pa_int', 'pa_2pts', 'ru_att', 'ru_yds', 'ru_tds',
                        'ru_2pts', 'rec_receptions', 'rec_yds', 'rec_tds',
                        'rec_2pts', 'fumb', 'fantasy points'], axis=1)

    for label in labels:
        dv = df[label]
        # defining the linear regression estimator for each iv, and
        # training it with the data
        regr = linear_model.LinearRegression()
        regr.fit(features, dv)

        # serializing the model to a file
        pickle.dump(regr, open(os.path.join(path_files, "models/wr_" + label + ".pkl"), "wb"))
