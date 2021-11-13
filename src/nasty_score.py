import pickle
import numpy as np


def import_model(file_path):
    """
    Import the model from a pickle file.
    """
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model


def add_nasty_score(data, sz_model, swing_model, swingmiss_model):

    data = data.fillna(-9999)
    sz_cols = ['effective_speed', 'pfx_x', 'pfx_z', 'vx0', 'vz0', 'ax',
               'az', 'release_pos_x', 'release_pos_z']

    data['strikezone'] = sz_model.predict(np.array(data[sz_cols]))

    swing_cols = ['release_spin_rate', 'effective_speed', 'pfx_x', 'pfx_z',
                  'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'spin_axis',
                  'strikezone']

    data['swing'] = swing_model.predict(np.array(data[swing_cols]))
    data['swingmiss'] = swingmiss_model.predict(np.array(data[swing_cols]))

    data['nasty_score_raw'] = data.swing * data.swingmiss

    scale = data.nasty_score_raw.max()
    data['nasty_score'] = data.nasty_score_raw / scale * 100

    return data.copy()
