import csv


def evaluate_qb(name, team, opponent, home, week, model, stat, qb_stats):
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
    qb_stats[stat] = float(prediction)
    return qb_stats


def evaluate_wr(name, team, opponent, home, week, model, stat, wr_stats):
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
    wr_stats[stat] = float(prediction)
    return wr_stats


def evaluate_rb(name, team, opponent, home, week, model, stat, rb_stats):
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
    rb_stats[stat] = float(prediction)
    return rb_stats


def evaluate_te(name, team, opponent, home, week, model, stat, te_stats):
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
    te_stats[stat] = float(prediction)
    return te_stats


def evaluate_k(name, team, opponent, home, week, model, stat, k_stats):
    '''Creates a prediction, based on the ivs provided and a model.'''
    players = {}
    teams = {}
    opponents = {}
    with open('data/k_data.csv') as f:
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
    k_stats[stat] = float(prediction)
    return k_stats


def evaluate_dst(team, opponent, home, week, model, stat, dst_stats):
    '''Creates a prediction, based on the ivs provided and a model.'''
    teams = {}
    opponents = {}
    with open('data/dst_data.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            teams[row['team']] = 0
            opponents[row['opponent']] = 0
    f.close()

    ivs = [int(week)]
    teams[team] = 1
    opponents[opponent] = 1
    for k, v in teams.items():
        ivs.append(v)
    for k, v in opponents.items():
        ivs.append(v)
    ivs.append(int(home))
    # the model generates a predicted performance
    # ivs = np.array(ivs)
    prediction = model.predict([ivs])
    # preparing a response object and storing the model's predictions
    dst_stats[stat] = float(prediction)
    return dst_stats


def predict_qb_stats(name, team, opponent, home, week, models):
    qb_stats = {}
    for stat, model in models.items():
        qb_stats = evaluate_qb(name, team, opponent, home, week, model, stat, qb_stats)

    points = (qb_stats['pass_yds'] / 25) + (6 * qb_stats['pass_tds'])
    points += (2 * qb_stats['pass_2pts']) - (2 * qb_stats['pass_int'])
    points += (qb_stats['recieving_yds'] / 10) + (qb_stats['recieving_tds'] * 6)
    points += (2 * qb_stats['recieving_2pts']) + (qb_stats['recieving_receptions'] / 2)
    points += (qb_stats['rushing_yds'] / 10) + (qb_stats['rushing_tds'] * 6)
    points += (2 * qb_stats['rushing_2pts']) - (qb_stats['fumbles'] * 2)

    qb_stats['name'] = name
    qb_stats['team'] = team
    qb_stats['opponent'] = opponent
    qb_stats['home'] = 'home' if home > 0 else 'away'
    qb_stats['fantasy points'] = points
    # sending our response object back as json
    return qb_stats


def predict_wr_stats(name, team, opponent, home, week, models):
    wr_stats = {}
    for stat, model in models.items():
        wr_stats = evaluate_wr(name, team, opponent, home, week, model, stat, wr_stats)

    points = (wr_stats['pass_yds'] / 25) + (6 * wr_stats['pass_tds'])
    points += (2 * wr_stats['pass_2pts']) - (2 * wr_stats['pass_int'])
    points += (wr_stats['recieving_yds'] / 10) + (wr_stats['recieving_tds'] * 6)
    points += (2 * wr_stats['recieving_2pts']) + (wr_stats['recieving_receptions'] / 2)
    points += (wr_stats['rushing_yds'] / 10) + (wr_stats['rushing_tds'] * 6)
    points += (2 * wr_stats['rushing_2pts']) - (wr_stats['fumbles'] * 2)

    wr_stats['name'] = name
    wr_stats['team'] = team
    wr_stats['opponent'] = opponent
    wr_stats['home'] = 'home' if home > 0 else 'away'
    wr_stats['fantasy points'] = points
    # sending our response object back as json
    return wr_stats


def predict_rb_stats(name, team, opponent, home, week, models):
    rb_stats = {}
    for stat, model in models.items():
        rb_stats = evaluate_rb(name, team, opponent, home, week, model, stat, rb_stats)

    points = (rb_stats['pass_yds'] / 25) + (6 * rb_stats['pass_tds'])
    points += (2 * rb_stats['pass_2pts']) - (2 * rb_stats['pass_int'])
    points += (rb_stats['recieving_yds'] / 10) + (rb_stats['recieving_tds'] * 6)
    points += (2 * rb_stats['recieving_2pts']) + (rb_stats['recieving_receptions'] / 2)
    points += (rb_stats['rushing_yds'] / 10) + (rb_stats['rushing_tds'] * 6)
    points += (2 * rb_stats['rushing_2pts']) - (rb_stats['fumbles'] * 2)

    rb_stats['name'] = name
    rb_stats['team'] = team
    rb_stats['opponent'] = opponent
    rb_stats['home'] = 'home' if home > 0 else 'away'
    rb_stats['fantasy points'] = points
    # sending our response object back as json
    return rb_stats


def predict_te_stats(name, team, opponent, home, week, models):
    te_stats = {}
    for stat, model in models.items():
        te_stats = evaluate_te(name, team, opponent, home, week, model, stat, te_stats)

    points = (te_stats['pass_yds'] / 25) + (6 * te_stats['pass_tds'])
    points += (2 * te_stats['pass_2pts']) - (2 * te_stats['pass_int'])
    points += (te_stats['recieving_yds'] / 10) + (te_stats['recieving_tds'] * 6)
    points += (2 * te_stats['recieving_2pts']) + (te_stats['recieving_receptions'] / 2)
    points += (te_stats['rushing_yds'] / 10) + (te_stats['rushing_tds'] * 6)
    points += (2 * te_stats['rushing_2pts']) - (te_stats['fumbles'] * 2)

    te_stats['name'] = name
    te_stats['team'] = team
    te_stats['opponent'] = opponent
    te_stats['home'] = 'home' if home > 0 else 'away'
    te_stats['fantasy points'] = points
    # sending our response object back as json
    return te_stats


def predict_k_stats(name, team, opponent, home, week, models):
    k_stats = {}
    for stat, model in models.items():
        k_stats = evaluate_k(name, team, opponent, home, week, model, stat, k_stats)

    points = k_stats['xps'] + (3 * k_stats['fgs'])

    k_stats['name'] = name
    k_stats['team'] = team
    k_stats['opponent'] = opponent
    k_stats['home'] = 'home' if home > 0 else 'away'
    k_stats['fantasy points'] = points
    # sending our response object back as json
    return k_stats


def predict_dst_stats(team, opponent, home, week, models):
    dst_stats = {}
    for stat, model in models.items():
        dst_stats = evaluate_dst(team, opponent, home, week, model, stat, dst_stats)

    if int(dst_stats['points_allowed']) > 34:
        pa = -4
    elif int(dst_stats['points_allowed']) > 27:
        pa = -1
    elif int(dst_stats['points_allowed']) > 20:
        pa = 0
    elif int(dst_stats['points_allowed']) > 13:
        pa = 1
    elif int(dst_stats['points_allowed']) > 6:
        pa = 4
    elif int(dst_stats['points_allowed']) > 0:
        pa = 7
    else:
        pa = 10
    if int(dst_stats['yards_allowed']) > 499:
        payds = -3
    elif int(dst_stats['yards_allowed']) > 99:
        payds = 0
    else:
        payds = 3

    points = dst_stats['sack'] + (2 * dst_stats['int'])
    points += (2 * dst_stats['safeties']) + (2 * dst_stats['fum_rec'])
    points += (dst_stats['block'] * 2) + (dst_stats['tds'] * 6)
    points += pa + payds

    dst_stats['team'] = team
    dst_stats['opponent'] = opponent
    dst_stats['home'] = 'home' if home > 0 else 'away'
    dst_stats['fantasy points'] = points
    # sending our response object back as json
    return dst_stats
