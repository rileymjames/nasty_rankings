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

The models are trained in the ``model_selection.py`` code.

## Results
After training, the model is used to rank each pitch from the 2021 season. Results can also be found in the ``Rank 2021 pitchers.ipynb`` notebook.

Table 1. Top 10 nastiest pitches* throughout the 2021 season, 100 pitch minumum
| player_name        | pitch_type   |   avg_release_speed |   avg_release_spin_rate |   pitch_count |   nasty_score |
|:-------------------|:-------------|--------------------:|------------------------:|--------------:|--------------:|
| Martin, Chris      | SL           |             83.4826 |                 2496.34 |           109 |       42.1304 |
| Gallen, Zac        | SL           |             86.1486 |                 2467.82 |           179 |       41.9826 |
| Treinen, Blake     | SL           |             86.5086 |                 2396.77 |           429 |       41.686  |
| Jackson, Luke      | SL           |             87.6188 |                 2313.28 |           650 |       41.6773 |
| Pineda, Michael    | SL           |             81.2269 |                 1890.67 |           494 |       41.2578 |
| Melancon, Mark     | KC           |             82.2452 |                 2599.08 |           363 |       41.0571 |
| Gallegos, Giovanny | SL           |             85.6004 |                 2482.92 |           534 |       40.6533 |
| Glasnow, Tyler     | CU           |             83.5049 |                 2995.28 |           183 |       40.6457 |
| Ginkel, Kevin      | SL           |             83.8469 |                 1892.06 |           224 |       39.9241 |
| Gibson, Kyle       | SL           |             83.4665 |                 2513.55 |           462 |       39.5484 |
* Values are averages over all pitches thrown of each type 

Table 2. Top 10 nastiest pitchers throughout the 2021 season, 400 pitch minimum
| player_name     |   nasty_score |   pitch_count |
|:----------------|--------------:|--------------:|
| Jackson, Luke   |       30.8664 |          1204 |
| Glasnow, Tyler  |       29.5164 |          1339 |
| deGrom, Jacob   |       28.6884 |          1226 |
| Scott, Tanner   |       28.4809 |          1032 |
| Anderson, Shaun |       27.6063 |           437 |
| Musgrove, Joe   |       27.5701 |          2938 |
| Clase, Emmanuel |       27.3388 |          1057 |
| Doval, Camilo   |       26.9649 |           499 |
| McGowin, Kyle   |       26.7913 |           517 |
| Pagán, Emilio   |       26.4082 |          1098 |

Table 3. Top 10 nastiest games throughout the 2021 season, 50 pitch minimum
| player_name     | game_date           |   nasty_score |   pitch_count |
|:----------------|:--------------------|--------------:|--------------:|
| Musgrove, Joe   | 2021-05-08 00:00:00 |       34.0255 |            90 |
| Musgrove, Joe   | 2021-09-10 00:00:00 |       33.5874 |           106 |
| deGrom, Jacob   | 2021-06-16 00:00:00 |       33.5733 |            51 |
| deGrom, Jacob   | 2021-05-31 00:00:00 |       33.3269 |            70 |
| Musgrove, Joe   | 2021-04-19 00:00:00 |       33.2768 |            96 |
| Rasmussen, Drew | 2021-08-06 00:00:00 |       33.2465 |            53 |
| Glasnow, Tyler  | 2021-05-26 00:00:00 |       32.3265 |           102 |
| Glasnow, Tyler  | 2021-04-01 00:00:00 |       32.3097 |            77 |
| deGrom, Jacob   | 2021-06-11 00:00:00 |       32.1563 |            80 |
| Musgrove, Joe   | 2021-07-29 00:00:00 |       32.1233 |            91 |

## Sticky-stuff
The biggest controversy of the 2021 baseball season was the widespread use and then banning of a substance called "sticky-stuff" or "spidertack". This extremely sticky substance allowed pitchers to get more grip on the ball, increasing spin rate and movement. After recieving negative player and media attention on the subject throughout late May and early June, MLB put rules in place to ban the use of sticky stuff on June 21. This analysis is also available in the ``Sticky-stuff analysis.ipynb`` notebook.

The banning of sticky-stuff effected teams and players across baseball, leading to more offense overall throughout the league. Without sticky-stuff, "stuff" and "nastiest" went down significantly.

Table 5. Percent of pitchers pre-sticky-stuff
| Top n pitches | % of pitches pre-sticky-stuff ban |
| 50 | 74.0% |
| 100 | 63.0% |
| 500 | 56.6% |
| 2500 | 50.6% |
| 10000 | 46.5% |
| 50000 | 45.2% |
| 500000 | 43.4% |

Of the 100 nastiest pitches thrown in 2021, over 60% were before the ban, while under 50% of the top 10,000 pitches were pre-ban. Of the elite pitches thrown this season, the overwhelming majority benefited from the use of sticky-stuff.

Figure 1. Nasty score over time
![alt text](https://github.com/rileymjames/nasty_rankings/blob/images/nasty_plot.jpg?raw=true)


