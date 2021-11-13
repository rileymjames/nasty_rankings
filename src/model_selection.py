import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from hyperopt import STATUS_OK, fmin, hp, tpe


def prepare_data(path):
    data = pd.read_feather(path)

    # create a swing flag
    swing_map = {
        'ball': 0,
        'foul': 1,
        'called_strike': 0,
        'swinging_strike': 1,
        'hit_into_play': 1,
        'missed_bunt': 1,
        'blocked_ball': 0,
        'foul_tip': 1,
        'swinging_strike_blocked': 1,
        'foul_bunt': 1,
        'intent_ball': 0,
        'hit_by_pitch': 0,
        'bunt_foul_tip': 1,
        'pitchout': 0,
        'swinging_pitchout': 1}

    data['swing'] = data.description.map(swing_map)

    # create a swing and miss flag
    data['swinging_strike'] = data.description.map(
        {'swinging_strike': 1, 'swinging_strike_blocked': 1})

    data.swinging_strike = data.swinging_strike.fillna(0)

    # create a called strike flag
    data['strike'] = data.description.str.contains('called_strike').astype(int)

    data = data.fillna(-9999)

    return data.copy()


def tune_hyperparameters(X_train, y_train, X_test, y_test):
    param_space = {'max_depth': hp.quniform("max_depth", 3, 10, 1),
                   'gamma': hp.uniform('gamma', 0, 14),
                   'learning_rate': hp.uniform('learning_rate', 0, 1),
                   'reg_alpha': hp.uniform('reg_alpha', 0, 1),
                   'reg_lambda': hp.quniform('reg_lambda', 0, 10, 1),
                   'colsample_bytree': hp.uniform('colsample_bytree', 0.3, 1),
                   'min_child_weight':
                   hp.quniform('min_child_weight', 0, 10, 1),
                   'n_estimators': hp.quniform('n_estimators', 100, 1000, 10)
                   }

    evaluation = [(X_train, y_train), (X_test, y_test)]

    def objective(space):
        model = xgb.XGBRegressor(objective='binary:logistic',
                                 eval_metric='auc',
                                 n_estimators=int(space['n_estimators']),
                                 learning_rate=space['learning_rate'],
                                 max_depth=int(space['max_depth']),
                                 gamma=space['gamma'],
                                 reg_lambda=space['reg_lambda'],
                                 reg_alpha=space['reg_alpha'],
                                 min_child_weight=int(
                                     space['min_child_weight']),
                                 colsample_bytree=space['colsample_bytree']
                                 )

        model.fit(X_train, y_train, eval_set=evaluation, eval_metric='auc',
                  early_stopping_rounds=10, verbose=False)

        pred = model.predict(X_test,
                             iteration_range=(0, model.best_iteration + 1))
        score = roc_auc_score(y_test, pred)

        return {'loss': -score, 'status': STATUS_OK}

    best_hyperparams = fmin(fn=objective,
                            space=param_space,
                            algo=tpe.suggest,
                            max_evals=100)

    return best_hyperparams


def strikezone_model(data):
    # filter to only events with no swing
    data = data[data.swing == 0].reset_index(drop=True)

    # define label and features
    label_col = 'strike'
    x_cols = ['effective_speed', 'pfx_x', 'pfx_z', 'vx0', 'vz0', 'ax',
              'az', 'release_pos_x', 'release_pos_z']

    # prepare X and y
    y = np.array(data[label_col])
    X = np.array(data[x_cols])

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # tune hyperparameters
    best_hyperparams = tune_hyperparameters(X_train, y_train, X_test, y_test)

    model = xgb.XGBRegressor(objective='binary:logistic',
                             use_label_encoder=False,
                             eval_metric='auc',
                             n_estimators=int(
                                 best_hyperparams['n_estimators']),
                             learning_rate=best_hyperparams['learning_rate'],
                             max_depth=int(best_hyperparams['max_depth']),
                             gamma=best_hyperparams['gamma'],
                             reg_lambda=best_hyperparams['reg_lambda'],
                             reg_alpha=best_hyperparams['reg_alpha'],
                             min_child_weight=int(
                                 best_hyperparams['min_child_weight']),
                             colsample_bytree=best_hyperparams[
                                 'colsample_bytree'])

    evaluation = [(X_train, y_train), (X_test, y_test)]
    model.fit(X_train, y_train, eval_set=evaluation, eval_metric='auc',
              verbose=False)

    return model


def swing_model(data, sz_model):
    # create probabalistic strikezone
    sz_model_cols = ['effective_speed', 'pfx_x', 'pfx_z', 'vx0', 'vz0', 'ax',
                     'az', 'release_pos_x', 'release_pos_z']

    X_sz = np.array(data[sz_model_cols])
    data['strikezone_prob'] = sz_model.predict(X_sz)

    # define label and features
    label_col = 'swing'
    x_cols = ['release_spin_rate', 'effective_speed', 'pfx_x', 'pfx_z', 'vx0',
              'vy0', 'vz0', 'ax', 'ay', 'az', 'spin_axis', 'strikezone_prob']

    # prepare X and y
    y = np.array(data[label_col])
    X = np.array(data[x_cols])

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # tune hyperparameters
    best_hyperparams = tune_hyperparameters(X_train, y_train, X_test, y_test)

    model = xgb.XGBRegressor(objective='binary:logistic',
                             use_label_encoder=False,
                             eval_metric='auc',
                             n_estimators=int(
                                 best_hyperparams['n_estimators']),
                             learning_rate=best_hyperparams['learning_rate'],
                             max_depth=int(best_hyperparams['max_depth']),
                             gamma=best_hyperparams['gamma'],
                             reg_lambda=best_hyperparams['reg_lambda'],
                             reg_alpha=best_hyperparams['reg_alpha'],
                             min_child_weight=int(
                                 best_hyperparams['min_child_weight']),
                             colsample_bytree=best_hyperparams[
                                 'colsample_bytree'])

    evaluation = [(X_train, y_train), (X_test, y_test)]
    model.fit(X_train, y_train, eval_set=evaluation, eval_metric='auc',
              verbose=False)

    return model


def swingmiss_model(data, sz_model):
    # subset to pitches that are swings
    data = data.loc[data.swing == 1].reset_index(drop=True)

    # create probabalistic strikezone
    sz_model_cols = ['effective_speed', 'pfx_x', 'pfx_z', 'vx0', 'vz0', 'ax',
                     'az', 'release_pos_x', 'release_pos_z']

    X_sz = np.array(data[sz_model_cols])
    data['strikezone_prob'] = sz_model.predict(X_sz)

    # define label and features
    label_col = 'swinging_strike'
    x_cols = ['release_spin_rate', 'effective_speed', 'pfx_x', 'pfx_z', 'vx0',
              'vy0', 'vz0', 'ax', 'ay', 'az', 'spin_axis', 'strikezone_prob']

    # prepare X and y
    y = np.array(data[label_col])
    X = np.array(data[x_cols])

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # tune hyperparameters
    best_hyperparams = tune_hyperparameters(X_train, y_train, X_test, y_test)

    model = xgb.XGBRegressor(objective='binary:logistic',
                             use_label_encoder=False,
                             eval_metric='auc',
                             n_estimators=int(
                                 best_hyperparams['n_estimators']),
                             learning_rate=best_hyperparams['learning_rate'],
                             max_depth=int(best_hyperparams['max_depth']),
                             gamma=best_hyperparams['gamma'],
                             reg_lambda=best_hyperparams['reg_lambda'],
                             reg_alpha=best_hyperparams['reg_alpha'],
                             min_child_weight=int(
                                 best_hyperparams['min_child_weight']),
                             colsample_bytree=best_hyperparams[
                                 'colsample_bytree'])

    evaluation = [(X_train, y_train), (X_test, y_test)]
    model.fit(X_train, y_train, eval_set=evaluation, eval_metric='auc',
              verbose=False)

    return model
