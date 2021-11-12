"""
Script to develop models to be used in the pitch grading.

Execution
---------
python "01 Get pitch models.py"
"""

import pickle
import src.model_selection as ms

"""
Global
"""

# Inputs
input_dir = 'data'

# Outputs
output_dir = 'models'
output_filetype = '.pkl'


def main():
    # get data
    data = ms.prepare_data(input_dir + '/nasty_data.fea')

    print('Developing strikezone model...', '\n')
    sz_model = ms.strikezone_model(data)

    print('Developing swing model...', '\n')
    swing_model = ms.swing_model(data, sz_model)

    print('Developing swing and miss model...', '\n')
    swingmiss_model = ms.swingmiss_model(data, sz_model)

    # save models
    with open(output_dir + '/sz_model' + output_filetype, 'wb') as f:
        pickle.dump(sz_model, f)

    with open(output_dir + '/swing_model' + output_filetype, 'wb') as f:
        pickle.dump(swing_model, f)

    with open(output_dir + '/swingmiss_model' + output_filetype, 'wb') as f:
        pickle.dump(swingmiss_model, f)


if __name__ == '__main__':
    main()
