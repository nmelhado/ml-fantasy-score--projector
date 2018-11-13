import pandas
import pickle
import io
import csv
from sklearn import linear_model


def analyze_dsts():
    '''Function that analyzes the DST data and creates a model from it.'''
    teams = {}
    opponents = {}
    with open('data/dst_data.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    with io.open('computed/dst_data.csv', 'w', newline='') as stat_file:
        stat_writer = csv.writer(stat_file)
        cats = ['year', 'week']
        for k, v in teams.items():
            cats.append(k)
        for k, v in opponents.items():
            cats.append(k)
        cats.extend(['home', 'sack', 'int', 'safeties', 'fum_rec', 'block',
                     'tds', 'points_allowed', 'yards_allowed',
                     'fantasy points'])
        stat_writer.writerow(cats)
        with open('data/dst_data.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                teams[row['team']] = 1
                opponents[row['opponent']] = 1
                stats = [row['year'], row['week']]
                for k, v in teams.items():
                    stats.append(v)
                for k, v in opponents.items():
                    stats.append(v)
                stats.extend([row['home'], row['sack'], row['int'],
                              row['safeties'], row['fum_rec'], row['block'],
                              row['tds'], row['points_allowed'],
                              row['yards_allowed'], row['fantasy points']])
                stat_writer.writerow(stats)
                teams[row['team']] = 0
                opponents[row['opponent']] = 0

        f.close()
    stat_file.close()
    # loading the data as a panda
    df = pandas.read_csv('computed/dst_data.csv', delimiter=",")

    # getting the dvs
    labels = ['sack', 'int', 'safeties', 'fum_rec', 'block', 'tds',
              'points_allowed', 'yards_allowed']

    # getting the ivs
    features = df.drop(['year', 'sack', 'int', 'safeties', 'fum_rec', 'block',
                        'tds', 'points_allowed', 'yards_allowed',
                        'fantasy points'], axis=1)

    for label in labels:
        dv = df[label]
        # defining the linear regression estimator for each iv, and
        # training it with the data
        regr = linear_model.LinearRegression()
        regr.fit(features, dv)

        # serializing the model to a file
        pickle.dump(regr, open("models/dst_" + label + ".pkl", "wb"))
