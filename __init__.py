from flask import Flask
from flask import jsonify
from flask import render_template
import pickle
import numpy as np
import os
import sys
import inspect
import csv
import requests
from bs4 import BeautifulSoup
from get_all_data import get_all_data, get_limits
from analyzers.analyze_qbs import analyze_qbs
from analyzers.analyze_rbs import analyze_rbs
from analyzers.analyze_wrs import analyze_wrs
from analyzers.analyze_tes import analyze_tes
from analyzers.analyze_dsts import analyze_dsts
from analyzers.analyze_ks import analyze_ks
from predict import predict_qb_stats, predict_wr_stats, predict_rb_stats, predict_te_stats, predict_k_stats, predict_dst_stats

app = Flask(__name__)

week = get_limits()
reevaluate = get_all_data()

if reevaluate:
    analyze_qbs()
    analyze_rbs()
    analyze_wrs()
    analyze_tes()
    analyze_dsts()
    analyze_ks()

# getting the trained qb models from the files created by analyze_qbs()
qb_models = {'fumbles': pickle.load(open("models/qb_fumb.pkl", "rb")),
             'pass_2pts': pickle.load(open("models/qb_pa_2pts.pkl", "rb")),
             'pass_int': pickle.load(open("models/qb_pa_int.pkl", "rb")),
             'pass_tds': pickle.load(open("models/qb_pa_tds.pkl", "rb")),
             'pass_yds': pickle.load(open("models/qb_pa_yds.pkl", "rb")),
             'recieving_2pts': pickle.load(open("models/qb_rec_2pts.pkl", "rb")),
             'recieving_receptions': pickle.load(open("models/qb_rec_receptions.pkl", "rb")),
             'recieving_tds': pickle.load(open("models/qb_rec_tds.pkl", "rb")),
             'recieving_yds': pickle.load(open("models/qb_rec_yds.pkl", "rb")),
             'rushing_2pts': pickle.load(open("models/qb_ru_2pts.pkl", "rb")),
             'rushing_tds': pickle.load(open("models/qb_ru_tds.pkl", "rb")),
             'rushing_yds': pickle.load(open("models/qb_ru_yds.pkl", "rb"))}

# getting the trained wr models from the files created by analyze_wrs()
wr_models = {'fumbles': pickle.load(open("models/wr_fumb.pkl", "rb")),
             'pass_2pts': pickle.load(open("models/wr_pa_2pts.pkl", "rb")),
             'pass_int': pickle.load(open("models/wr_pa_int.pkl", "rb")),
             'pass_tds': pickle.load(open("models/wr_pa_tds.pkl", "rb")),
             'pass_yds': pickle.load(open("models/wr_pa_yds.pkl", "rb")),
             'recieving_2pts': pickle.load(open("models/wr_rec_2pts.pkl", "rb")),
             'recieving_receptions': pickle.load(open("models/wr_rec_receptions.pkl", "rb")),
             'recieving_tds': pickle.load(open("models/wr_rec_tds.pkl", "rb")),
             'recieving_yds': pickle.load(open("models/wr_rec_yds.pkl", "rb")),
             'rushing_2pts': pickle.load(open("models/wr_ru_2pts.pkl", "rb")),
             'rushing_tds': pickle.load(open("models/wr_ru_tds.pkl", "rb")),
             'rushing_yds': pickle.load(open("models/wr_ru_yds.pkl", "rb"))}

# getting the trained rb models from the files created by analyze_rbs()
rb_models = {'fumbles': pickle.load(open("models/rb_fumb.pkl", "rb")),
             'pass_2pts': pickle.load(open("models/rb_pa_2pts.pkl", "rb")),
             'pass_int': pickle.load(open("models/rb_pa_int.pkl", "rb")),
             'pass_tds': pickle.load(open("models/rb_pa_tds.pkl", "rb")),
             'pass_yds': pickle.load(open("models/rb_pa_yds.pkl", "rb")),
             'recieving_2pts': pickle.load(open("models/rb_rec_2pts.pkl", "rb")),
             'recieving_receptions': pickle.load(open("models/rb_rec_receptions.pkl", "rb")),
             'recieving_tds': pickle.load(open("models/rb_rec_tds.pkl", "rb")),
             'recieving_yds': pickle.load(open("models/rb_rec_yds.pkl", "rb")),
             'rushing_2pts': pickle.load(open("models/rb_ru_2pts.pkl", "rb")),
             'rushing_tds': pickle.load(open("models/rb_ru_tds.pkl", "rb")),
             'rushing_yds': pickle.load(open("models/rb_ru_yds.pkl", "rb"))}

# getting the trained te models from the files created by analyze_tes()
te_models = {'fumbles': pickle.load(open("models/te_fumb.pkl", "rb")),
             'pass_2pts': pickle.load(open("models/te_pa_2pts.pkl", "rb")),
             'pass_int': pickle.load(open("models/te_pa_int.pkl", "rb")),
             'pass_tds': pickle.load(open("models/te_pa_tds.pkl", "rb")),
             'pass_yds': pickle.load(open("models/te_pa_yds.pkl", "rb")),
             'recieving_2pts': pickle.load(open("models/te_rec_2pts.pkl", "rb")),
             'recieving_receptions': pickle.load(open("models/te_rec_receptions.pkl", "rb")),
             'recieving_tds': pickle.load(open("models/te_rec_tds.pkl", "rb")),
             'recieving_yds': pickle.load(open("models/te_rec_yds.pkl", "rb")),
             'rushing_2pts': pickle.load(open("models/te_ru_2pts.pkl", "rb")),
             'rushing_tds': pickle.load(open("models/te_ru_tds.pkl", "rb")),
             'rushing_yds': pickle.load(open("models/te_ru_yds.pkl", "rb"))}

# getting the trained te models from the files created by analyze_tes()
dst_models = {'block': pickle.load(open("models/dst_block.pkl", "rb")),
              'fum_rec': pickle.load(open("models/dst_fum_rec.pkl", "rb")),
              'int': pickle.load(open("models/dst_int.pkl", "rb")),
              'points_allowed': pickle.load(open("models/dst_points_allowed.pkl", "rb")),
              'sack': pickle.load(open("models/dst_sack.pkl", "rb")),
              'safeties': pickle.load(open("models/dst_safeties.pkl", "rb")),
              'tds': pickle.load(open("models/dst_tds.pkl", "rb")),
              'yards_allowed': pickle.load(open("models/dst_yards_allowed.pkl", "rb"))}

# getting the trained te models from the files created by analyze_tes()
k_models = {'fgs': pickle.load(open("models/k_fgs.pkl", "rb")),
            'xps': pickle.load(open("models/k_xps.pkl", "rb"))}

qb_response = {}
wr_response = {}
rb_response = {}
te_response = {}
my_team = []
my_opponent = []
my_players = []
opponent_players = []
my_score = 0
opponent_score = 0


def predict_qb(name, team, opponent, home, week, model, stat):
    '''Creates a prediction, based on the ivs provided and a model.'''
    players = {}
    teams = {}
    opponents = {}
    with open('data/qb_data.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            players[row['name']] = 0
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    ivs = [int(week)]
    players[name] = 1
    teams[team] = 1
    opponents[opponent] = 1
    for k, v in players.items():
        ivs.append(v)
    for k, v in teams.items():
        ivs.append(v)
    for k, v in opponents.items():
        ivs.append(v)
    ivs.append(int(home))
    # the model generates a predicted performance
    # ivs = np.array(ivs)
    prediction = model.predict([ivs])
    # preparing a response object and storing the model's predictions
    global qb_response
    qb_response[stat] = float(prediction)


def predict_wr(name, team, opponent, home, week, model, stat):
    '''Creates a prediction, based on the ivs provided and a model.'''
    players = {}
    teams = {}
    opponents = {}
    with open('data/wr_data.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            players[row['name']] = 0
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    ivs = [int(week)]
    players[name] = 1
    teams[team] = 1
    opponents[opponent] = 1
    for k, v in players.items():
        ivs.append(v)
    for k, v in teams.items():
        ivs.append(v)
    for k, v in opponents.items():
        ivs.append(v)
    ivs.append(int(home))
    # the model generates a predicted performance
    # ivs = np.array(ivs)
    prediction = model.predict([ivs])
    # preparing a response object and storing the model's predictions
    global wr_response
    wr_response[stat] = float(prediction)


def predict_rb(name, team, opponent, home, week, model, stat):
    '''Creates a prediction, based on the ivs provided and a model.'''
    players = {}
    teams = {}
    opponents = {}
    with open('data/rb_data.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            players[row['name']] = 0
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    ivs = [int(week)]
    players[name] = 1
    teams[team] = 1
    opponents[opponent] = 1
    for k, v in players.items():
        ivs.append(v)
    for k, v in teams.items():
        ivs.append(v)
    for k, v in opponents.items():
        ivs.append(v)
    ivs.append(int(home))
    # the model generates a predicted performance
    # ivs = np.array(ivs)
    prediction = model.predict([ivs])
    # preparing a response object and storing the model's predictions
    global rb_response
    rb_response[stat] = float(prediction)


def predict_te(name, team, opponent, home, week, model, stat):
    '''Creates a prediction, based on the ivs provided and a model.'''
    players = {}
    teams = {}
    opponents = {}
    with open('data/te_data.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            players[row['name']] = 0
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    ivs = [int(week)]
    players[name] = 1
    teams[team] = 1
    opponents[opponent] = 1
    for k, v in players.items():
        ivs.append(v)
    for k, v in teams.items():
        ivs.append(v)
    for k, v in opponents.items():
        ivs.append(v)
    ivs.append(int(home))
    # the model generates a predicted performance
    # ivs = np.array(ivs)
    prediction = model.predict([ivs])
    # preparing a response object and storing the model's predictions
    global te_response
    te_response[stat] = float(prediction)


def calculate_points():
    global my_team
    global my_opponent
    global week
    global qb_models
    global wr_models
    global rb_models
    global k_models
    global dst_models
    global te_models
    global my_players
    global opponent_players
    global my_score
    global opponent_score
    for player in my_team:
        if player['position'] == 'QB':
            stats = predict_qb_stats(player['name'], player['team'], player['opponent'], player['home'], week, qb_models)
        elif player['position'] == 'WR':
            stats = predict_wr_stats(player['name'], player['team'], player['opponent'], player['home'], week, wr_models)
        elif player['position'] == 'RB':
            stats = predict_rb_stats(player['name'], player['team'], player['opponent'], player['home'], week, rb_models)
        elif player['position'] == 'TE':
            stats = predict_te_stats(player['name'], player['team'], player['opponent'], player['home'], week, te_models)
        elif player['position'] == 'K':
            stats = predict_k_stats(player['name'], player['team'], player['opponent'], player['home'], week, k_models)
        elif player['position'] == 'DEF':
            stats = predict_dst_stats(player['team'], player['opponent'], player['home'], week, dst_models)
        my_players.append(stats)
        my_score += stats['fantasy points']
    for player in my_opponent:
        if player['position'] == 'QB':
            stats = predict_qb_stats(player['name'], player['team'], player['opponent'], player['home'], week, qb_models)
        elif player['position'] == 'WR':
            stats = predict_wr_stats(player['name'], player['team'], player['opponent'], player['home'], week, wr_models)
        elif player['position'] == 'RB':
            stats = predict_rb_stats(player['name'], player['team'], player['opponent'], player['home'], week, rb_models)
        elif player['position'] == 'TE':
            stats = predict_te_stats(player['name'], player['team'], player['opponent'], player['home'], week, te_models)
        elif player['position'] == 'K':
            stats = predict_k_stats(player['name'], player['team'], player['opponent'], player['home'], week, k_models)
        elif player['position'] == 'DEF':
            stats = predict_dst_stats(player['team'], player['opponent'], player['home'], week, dst_models)
        opponent_players.append(stats)
        opponent_score += stats['fantasy points']


def grab_players(team):
    '''Grabs my players and my opponents and passes them to dictionaries.'''
    url = 'https://fantasy.nfl.com/league/2625883/team/' + str(team)
    url += '/gamecenter?gameCenterTab=track&trackType=fbs'
    req = requests.get(url)
    matchup = BeautifulSoup(req.text, "html.parser")

    global my_team
    global my_players
    global my_opponent
    global opponent_players
    global my_score
    global opponent_score
    my_team = list()
    my_players = list()
    my_opponent = list()
    opponent_players = list()
    my_score = 0
    opponent_score = 0
    players = matchup.find_all('tr', 'player-QB-0')
    players.extend(matchup.find_all('tr', 'player-RB-0'))
    players.extend(matchup.find_all('tr', 'player-RB-1'))
    players.extend(matchup.find_all('tr', 'player-WR-0'))
    players.extend(matchup.find_all('tr', 'player-WR-1'))
    players.extend(matchup.find_all('tr', 'player-TE-0'))
    players.extend(matchup.find_all('tr', 'player-W/R-0'))
    players.extend(matchup.find_all('tr', 'player-R/W/T-0'))
    players.extend(matchup.find_all('tr', 'player-K-0'))
    players.extend(matchup.find_all('tr', 'player-DEF-0'))
    mine = True

    for player in players:
        name = player.find('a', 'playerName').text
        em = player.find_all('em')[0]
        em = em.text.split(' - ')
        if len(em) < 2:
            em = player.find_all('em')[1]
            em = em.text.split(' - ')
        if len(em) < 2:
            position = player.find_all('em')[0].text
            team = name
        else:
            position = em[0]
            team = em[1]
        opponent = player.find('a', 'opp-fpa').text
        home = 1
        if opponent[0] == '@':
            opponent = opponent[1:]
            home = 0
        if mine:
            my_team.append({'name': name, 'position': position, 'team': team,
                            'opponent': opponent, 'home': home})
            mine = False
        else:
            my_opponent.append({'name': name, 'position': position,
                                'team': team, 'opponent': opponent,
                                'home': home})
            mine = True
    calculate_points()

# grab_players(8)


@app.route('/')
@app.route('/index')
def index():
    return '''
<html>
    <head>
        <title>AI - Fantasy Predictor</title>
    </head>
    <body>
        <h1>Fantasy Matchup Predictor</h1>
    </body>
</html>'''


@app.route('/matchup/<team>')
def matchup(team):
    grab_players(team)
    global my_players
    global opponent_players
    global my_score
    global opponent_score
    return render_template('matchup.html', my_players=my_players, opponent_players=opponent_players, my_score=my_score, opponent_score=opponent_score)


@app.route('/api/qb/<name>/<team>/<opponent>/<home>/<week>')
def qb_prediction(name, team, opponent, home, week):
    global qb_response
    qb_response = {}
    for stat, model in qb_models.items():
        predict_qb(name, team, opponent, home, week, model, stat)

    points = (qb_response['pass_yds'] / 25) + (6 * qb_response['pass_tds'])
    points += (2 * qb_response['pass_2pts']) - (2 * qb_response['pass_int'])
    points += (qb_response['recieving_yds'] / 10) + (qb_response['recieving_tds'] * 6)
    points += (2 * qb_response['recieving_2pts']) + (qb_response['recieving_receptions'] / 2)
    points += (qb_response['rushing_yds'] / 10) + (qb_response['rushing_tds'] * 6)
    points += (2 * qb_response['rushing_2pts']) - (qb_response['fumbles'] * 2)

    qb_response['fantasy points'] = points
    # sending our response object back as json
    return jsonify(qb_response)


@app.route('/api/wr/<name>/<team>/<opponent>/<home>/<week>')
def wr_prediction(name, team, opponent, home, week):
    global wr_response
    wr_response = {}
    for stat, model in wr_models.items():
        predict_wr(name, team, opponent, home, week, model, stat)

    points = (wr_response['pass_yds'] / 25) + (6 * wr_response['pass_tds'])
    points += (2 * wr_response['pass_2pts']) - (2 * wr_response['pass_int'])
    points += (wr_response['recieving_yds'] / 10) + (wr_response['recieving_tds'] * 6)
    points += (2 * wr_response['recieving_2pts']) + (wr_response['recieving_receptions'] / 2)
    points += (wr_response['rushing_yds'] / 10) + (wr_response['rushing_tds'] * 6)
    points += (2 * wr_response['rushing_2pts']) - (wr_response['fumbles'] * 2)

    wr_response['fantasy points'] = points
    # sending our response object back as json
    return jsonify(wr_response)


@app.route('/api/rb/<name>/<team>/<opponent>/<home>/<week>')
def rb_prediction(name, team, opponent, home, week):
    global rb_response
    rb_response = {}
    for stat, model in rb_models.items():
        predict_rb(name, team, opponent, home, week, model, stat)

    points = (rb_response['pass_yds'] / 25) + (6 * rb_response['pass_tds'])
    points += (2 * rb_response['pass_2pts']) - (2 * rb_response['pass_int'])
    points += (rb_response['recieving_yds'] / 10) + (rb_response['recieving_tds'] * 6)
    points += (2 * rb_response['recieving_2pts']) + (rb_response['recieving_receptions'] / 2)
    points += (rb_response['rushing_yds'] / 10) + (rb_response['rushing_tds'] * 6)
    points += (2 * rb_response['rushing_2pts']) - (rb_response['fumbles'] * 2)

    rb_response['fantasy points'] = points
    # sending our response object back as json
    return jsonify(rb_response)


@app.route('/api/te/<name>/<team>/<opponent>/<home>/<week>')
def te_prediction(name, team, opponent, home, week):
    global te_response
    te_response = {}
    for stat, model in te_models.items():
        predict_te(name, team, opponent, home, week, model, stat)

    points = (te_response['pass_yds'] / 25) + (6 * te_response['pass_tds'])
    points += (2 * te_response['pass_2pts']) - (2 * te_response['pass_int'])
    points += (te_response['recieving_yds'] / 10) + (te_response['recieving_tds'] * 6)
    points += (2 * te_response['recieving_2pts']) + (te_response['recieving_receptions'] / 2)
    points += (te_response['rushing_yds'] / 10) + (te_response['rushing_tds'] * 6)
    points += (2 * te_response['rushing_2pts']) - (te_response['fumbles'] * 2)

    te_response['fantasy points'] = points
    # sending our response object back as json
    return jsonify(te_response)

if __name__ == "__main__":
    app.run()
