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

Table 1. Model labels and features
| Model | Label | Features |
| --- | --- | --- |
| Strikezone | Called balls and strikes | Effective speed, directional movement, directional velocity, directional acceleration, release position |
| Swing | Swing event | Effective speed, directional movement, directional velocity, directional acceleration, spin rate, strikezone probability |
| Whiff | Whiff event | Effective speed, directional movement, directional velocity, directional acceleration, spin rate, strikezone probability |

The XGBoost model uses a logistic objective funtion and an auc evaluation metric. The hyper paramaters are tuned with hyperopt, a hyperparamater optimization function. More features were tested in the development of this model, including pitcher and batter handedness, and the pitch type, but these did not have an affect on the accuracy of the model so they were ultimately dropped.

The models are trained in the ``model_selection.py`` code.

## Results
After training, the model is used to rank each pitch from the 2021 season. Results can also be found in the ``Rank 2021 pitchers.ipynb`` notebook.

Table 2. Top 10 nastiest pitches* throughout the 2021 season, 100 pitch minumum
| player_name        | pitch_type   |   avg_release_speed |   avg_release_spin_rate |   pitch_count |   nasty_score |
|:-------------------|:-------------|--------------------:|------------------------:|--------------:|--------------:|
| Treinen, Blake     | SL           |             86.5086 |                 2396.77 |           429 |       45.8778 |
| Gallegos, Giovanny | SL           |             85.6004 |                 2482.92 |           534 |       43.8524 |
| Snell, Blake       | SL           |             86.5274 |                 2394.91 |           572 |       43.7114 |
| Rodón, Carlos      | SL           |             85.7038 |                 2431.17 |           626 |       43.3352 |
| Gallen, Zac        | SL           |             86.1486 |                 2467.82 |           179 |       43.237  |
| Jackson, Luke      | SL           |             87.6188 |                 2313.28 |           650 |       42.0988 |
| Pineda, Michael    | SL           |             81.2269 |                 1890.67 |           494 |       41.436  |
| Kittredge, Andrew  | SL           |             88.923  |                 2720.39 |           453 |       41.2838 |
| Chafin, Andrew     | SL           |             82.4624 |                 2407.47 |           250 |       41.2607 |
| Feyereisen, J.P.   | CH           |             87.6194 |                 1476.11 |           201 |       40.953  |
* Values are averages over all pitches thrown of each type 

Table 3. Top 10 nastiest pitchers throughout the 2021 season, 400 pitch minimum
| player_name     |   nasty_score |   pitch_count |
|:----------------|--------------:|--------------:|
| deGrom, Jacob   |       34.4525 |          1226 |
| Williams, Devin |       31.8472 |           993 |
| Hendriks, Liam  |       31.6064 |          1172 |
| Kimbrel, Craig  |       30.8858 |          1055 |
| Jackson, Luke   |       30.8253 |          1204 |
| Hader, Josh     |       30.7058 |           995 |
| Kopech, Michael |       29.8174 |          1225 |
| Scott, Tanner   |       29.6267 |          1032 |
| Glasnow, Tyler  |       28.3243 |          1339 |
| Pagán, Emilio   |       28.1704 |          1098 |

Table 4. Top 10 nastiest games throughout the 2021 season, 50 pitch minimum
| player_name     | game_date           |   nasty_score |   pitch_count |
|:----------------|:--------------------|--------------:|--------------:|
| deGrom, Jacob   | 2021-06-11 00:00:00 |       40.2499 |            80 |
| deGrom, Jacob   | 2021-05-31 00:00:00 |       39.086  |            70 |
| deGrom, Jacob   | 2021-06-16 00:00:00 |       38.2419 |            51 |
| deGrom, Jacob   | 2021-04-23 00:00:00 |       38.2166 |           109 |
| deGrom, Jacob   | 2021-04-05 00:00:00 |       36.8351 |            77 |
| Kopech, Michael | 2021-10-03 00:00:00 |       36.2085 |            51 |
| deGrom, Jacob   | 2021-05-25 00:00:00 |       35.2737 |            63 |
| deGrom, Jacob   | 2021-04-10 00:00:00 |       35.158  |            95 |
| deGrom, Jacob   | 2021-04-17 00:00:00 |       34.1791 |            99 |
| deGrom, Jacob   | 2021-04-28 00:00:00 |       33.2557 |            93 |

## Sticky-stuff
The biggest controversy of the 2021 baseball season was the widespread use and then banning of a substance called "sticky-stuff" or "spidertack". This extremely sticky substance allowed pitchers to get more grip on the ball, increasing spin rate and movement. After recieving negative player and media attention on the subject throughout late May and early June, MLB put rules in place to ban the use of sticky stuff on June 21. This analysis is also available in the ``Sticky-stuff analysis.ipynb`` notebook.

The banning of sticky-stuff effected teams and players across baseball, leading to more offense overall throughout the league. Without sticky-stuff, "stuff" and "nastiness" went down significantly.

Table 5. Percent of pitchers pre-sticky-stuff
| Top n pitches | % of pitches pre-sticky-stuff ban |
| --- | --: |
| 50 | 62.0% |
| 100 | 60.0% |
| 500 | 47.8% |
| 2500 | 48.2% |
| 10000 | 47.0% |
| 50000 | 44.7% |
| 500000 | 43.4% |

Of the 100 nastiest pitches thrown in 2021, 60% were before the ban, while under 50% of the top 10,000 pitches were pre-ban. Of the elite pitches thrown this season, the  majority benefited from the use of sticky-stuff.

Figure 1. Nasty score over time
![alt text](https://github.com/rileymjames/nasty_rankings/blob/main/images/nasty_plot.jpeg)

There is a clear drop off in pitch nastiness in the beginning of June, when the sticky-stuff controversy was reaching a peak, until June 21 when the ban went into place. Also interesting is the spike in nastiness during the playoffs. After the worst teams, with the worst pitchers, are eliminated, it leaves only elite playoff caliber players, causing a spike in the average nastiness.
