# Nasty Rankings
## Analysis overview
This analysis uses machine learning to quantify and rank a pitcher's "stuff". "Stuff" and "nastiness" are terms in baseball that are used to describe how inherently difficult it is to hit a pitcher's pitches. This model uses "whiffs", or swings and misses, to determine how nasty a pitch is. The more likely a pitch is to result in a whiff, the nastier the pitch is.

To determine the probability of a whiff on a given pitch, this analysis uses 3 models.
1. Probability a pitch is called a strike (strikezone model)
3. Probability a pitch is swung at, using model 1 as an input (swing model)
4. Given a swing, probability of a whiff, using model 1 as an input (whiff model)

The "nasty-score" is then given by the probability from the swing model multiplied by the probility from the whiff model, scaled to a maximum of 100.

## About the model
This analysis uses XGBoost, a gradient boosting machine learning algorithm, to estimate the probabilities described above. Each model was trained and tested on a split of pitch data from 2010 to present, a total of 8,236,183 pitches from 2,500 different pitchers.

The label and features of each model are shown below:
| Model | Label | Feature |
| --- | --- | --- |
| Strikezone | Called balls and strikes | Effective speed, directional movement, directional velocity, directional acceleration, release position |
| Swing | Swing event | Effective speed, directional movement, directional velocity, directional acceleration, spin rate, strikezone probability |
| Whiff | Whiff event | Effective speed, directional movement, directional velocity, directional acceleration, spin rate, strikezone probability |

The XGBoost model uses a logistic objective funtion and an auc evaluation metric. The hyper paramaters are tuned with hyperopt, a hyperparamater optimization function. More features were tested in the development of this model, including pitcher and batter handedness, and the pitch type, but these did not have an affect on the accuracy of the model so they were ultimately dropped.

## Results

## Sticky-stuff
