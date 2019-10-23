from time import time, strftime
import pickle
import ml.evaluate as evaluate
import ml.util as util
import ml.train as train
from helpers.processing import *
from helpers.analysis import *
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.utils import resample
import pandas as pd
import scipy as sc
import numpy as np
import time
import gc
import os
from os.path import join
import sys
sys.path.insert(0, '..')


RANDOM_STATE = 42


features_directory = '../features/processed'

suffix = '_one-per-user'
models_directory = './models{}'.format(suffix)
saves_directory = './saves{}'.format(suffix)
for d in [models_directory, saves_directory]:
    if not os.path.exists(d):
        os.makedirs(d)

feature_set_lookup_file_name = 'feature_names_by_type.pkl'
num_datapoints = 10  # None # None if you want all


# this script runs the same tasks as in the VizML Results paper

# dataset indices for each task, each task subsequently adding
# (dimensions, types, values, names)
dataset_indices = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    [0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16,
     17,
     18,
     19,
     20,
     21,
     22,
     23,
     24,
     25,
     26,
     27,
     28,
     29,
     30,
     31,
     32,
     33,
     34,
     35,
     36,
     37,
     38,
     39,
     40,
     41,
     42,
     43,
     44,
     45,
     46,
     47,
     48,
     49,
     655,
     656],
    [0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16,
     17,
     18,
     19,
     20,
     21,
     22,
     23,
     24,
     25,
     26,
     27,
     28,
     29,
     30,
     31,
     32,
     33,
     34,
     35,
     36,
     37,
     38,
     39,
     40,
     41,
     42,
     43,
     44,
     45,
     46,
     47,
     48,
     49,
     655,
     656,
     50,
     51,
     52,
     53,
     54,
     55,
     56,
     57,
     58,
     59,
     60,
     61,
     62,
     63,
     64,
     65,
     66,
     67,
     68,
     69,
     70,
     71,
     72,
     73,
     74,
     75,
     76,
     77,
     78,
     79,
     80,
     81,
     82,
     83,
     84,
     85,
     86,
     87,
     88,
     89,
     90,
     91,
     92,
     93,
     94,
     95,
     96,
     97,
     98,
     99,
     100,
     101,
     102,
     103,
     104,
     105,
     106,
     107,
     108,
     109,
     110,
     111,
     112,
     113,
     114,
     115,
     116,
     117,
     118,
     119,
     120,
     121,
     122,
     123,
     124,
     125,
     126,
     127,
     128,
     129,
     130,
     131,
     132,
     133,
     134,
     135,
     136,
     137,
     138,
     139,
     140,
     141,
     142,
     143,
     144,
     145,
     146,
     147,
     148,
     149,
     150,
     151,
     152,
     153,
     154,
     155,
     156,
     157,
     158,
     159,
     160,
     161,
     162,
     163,
     164,
     165,
     166,
     167,
     168,
     169,
     170,
     171,
     172,
     173,
     174,
     175,
     176,
     177,
     178,
     179,
     180,
     181,
     182,
     183,
     184,
     185,
     186,
     187,
     188,
     189,
     190,
     191,
     192,
     193,
     194,
     195,
     196,
     197,
     198,
     199,
     200,
     201,
     202,
     203,
     204,
     205,
     206,
     207,
     208,
     209,
     210,
     211,
     212,
     213,
     214,
     215,
     216,
     217,
     218,
     219,
     220,
     221,
     222,
     223,
     224,
     225,
     226,
     227,
     228,
     229,
     230,
     231,
     232,
     233,
     234,
     235,
     236,
     237,
     238,
     239,
     240,
     241,
     242,
     243,
     244,
     245,
     246,
     247,
     248,
     249,
     250,
     251,
     252,
     253,
     254,
     255,
     256,
     257,
     258,
     259,
     260,
     261,
     262,
     263,
     264,
     265,
     266,
     267,
     268,
     269,
     270,
     271,
     272,
     273,
     274,
     275,
     276,
     277,
     278,
     279,
     280,
     281,
     282,
     283,
     284,
     285,
     286,
     287,
     288,
     289,
     290,
     291,
     292,
     293,
     294,
     295,
     296,
     297,
     298,
     299,
     300,
     301,
     302,
     303,
     304,
     305,
     306,
     307,
     308,
     309,
     310,
     311,
     312,
     313,
     314,
     315,
     316,
     317,
     318,
     319,
     320,
     321,
     322,
     323,
     324,
     325,
     326,
     327,
     328,
     329,
     330,
     331,
     332,
     333,
     334,
     335,
     336,
     337,
     338,
     339,
     340,
     341,
     342,
     343,
     344,
     345,
     346,
     347,
     348,
     349,
     350,
     351,
     352,
     353,
     354,
     355,
     356,
     357,
     358,
     359,
     360,
     361,
     362,
     363,
     364,
     365,
     366,
     367,
     368,
     369,
     370,
     371,
     372,
     373,
     374,
     375,
     376,
     377,
     378,
     379,
     380,
     381,
     382,
     383,
     384,
     385,
     386,
     387,
     388,
     389,
     390,
     391,
     392,
     393,
     394,
     395,
     396,
     397,
     398,
     399,
     400,
     401,
     402,
     403,
     404,
     405,
     406,
     407,
     408,
     409,
     410,
     411,
     412,
     413,
     414,
     415,
     416,
     417,
     418,
     419,
     420,
     421,
     422,
     423,
     424,
     425,
     426,
     427,
     428,
     429,
     430,
     431,
     432,
     433,
     434,
     435,
     436,
     437,
     438,
     439,
     440,
     441,
     442,
     443,
     444,
     445,
     446,
     447,
     448,
     449,
     450,
     451,
     452,
     453,
     454,
     455,
     456,
     457,
     458,
     459,
     460,
     461,
     462,
     463,
     464,
     465,
     466,
     467,
     468,
     469,
     470,
     471,
     472,
     473,
     474,
     475,
     476,
     477,
     478,
     479,
     480,
     481,
     482,
     483,
     484,
     485,
     486,
     487,
     488,
     489,
     490,
     491,
     492,
     493,
     494,
     495,
     496,
     497,
     498,
     499,
     500,
     501,
     502,
     503,
     504,
     505,
     506,
     507,
     508,
     509,
     510,
     511,
     512,
     513,
     514,
     515,
     516,
     517,
     518,
     519,
     605,
     606,
     607,
     608,
     609,
     610,
     611,
     612,
     613,
     614,
     615,
     616,
     617,
     618,
     619,
     620,
     621,
     622,
     623,
     624,
     625,
     626,
     627,
     628,
     629,
     630,
     631,
     632,
     633,
     634,
     635,
     636,
     637,
     638,
     639,
     640,
     641,
     642,
     643,
     644,
     645,
     646,
     647,
     648,
     649,
     650,
     651,
     652,
     653,
     654,
     662,
     663,
     664,
     665,
     666,
     667,
     668,
     669,
     670,
     671,
     672,
     673,
     674,
     675,
     676,
     677,
     678,
     679,
     680,
     681,
     682,
     683,
     684,
     685,
     686,
     687,
     688,
     689,
     690,
     691,
     692,
     693,
     694,
     695,
     696,
     697,
     698,
     699,
     700,
     701,
     702,
     703,
     704,
     705,
     706,
     707,
     708,
     709,
     710,
     711,
     712,
     713,
     714,
     715,
     716,
     717,
     718,
     719,
     720,
     721,
     722,
     723,
     724,
     725,
     726,
     727,
     728,
     729,
     730,
     731,
     732,
     733,
     734,
     735,
     736,
     737,
     738,
     739,
     740,
     741,
     742,
     743,
     744,
     745,
     746,
     747,
     748,
     749,
     750,
     751,
     752,
     753,
     754,
     755,
     756,
     757,
     758,
     759,
     760,
     761,
     762,
     763,
     764,
     765,
     766,
     767,
     768,
     769,
     770,
     771,
     772,
     773,
     774,
     775,
     776,
     777,
     778,
     779,
     780,
     781,
     782,
     783,
     784,
     785,
     786,
     787,
     788,
     789,
     790,
     791,
     792,
     793,
     794,
     795,
     796,
     797,
     798,
     799,
     800,
     801,
     802,
     803,
     804,
     805,
     806],
    [0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16,
     17,
     18,
     19,
     20,
     21,
     22,
     23,
     24,
     25,
     26,
     27,
     28,
     29,
     30,
     31,
     32,
     33,
     34,
     35,
     36,
     37,
     38,
     39,
     40,
     41,
     42,
     43,
     44,
     45,
     46,
     47,
     48,
     49,
     655,
     656,
     50,
     51,
     52,
     53,
     54,
     55,
     56,
     57,
     58,
     59,
     60,
     61,
     62,
     63,
     64,
     65,
     66,
     67,
     68,
     69,
     70,
     71,
     72,
     73,
     74,
     75,
     76,
     77,
     78,
     79,
     80,
     81,
     82,
     83,
     84,
     85,
     86,
     87,
     88,
     89,
     90,
     91,
     92,
     93,
     94,
     95,
     96,
     97,
     98,
     99,
     100,
     101,
     102,
     103,
     104,
     105,
     106,
     107,
     108,
     109,
     110,
     111,
     112,
     113,
     114,
     115,
     116,
     117,
     118,
     119,
     120,
     121,
     122,
     123,
     124,
     125,
     126,
     127,
     128,
     129,
     130,
     131,
     132,
     133,
     134,
     135,
     136,
     137,
     138,
     139,
     140,
     141,
     142,
     143,
     144,
     145,
     146,
     147,
     148,
     149,
     150,
     151,
     152,
     153,
     154,
     155,
     156,
     157,
     158,
     159,
     160,
     161,
     162,
     163,
     164,
     165,
     166,
     167,
     168,
     169,
     170,
     171,
     172,
     173,
     174,
     175,
     176,
     177,
     178,
     179,
     180,
     181,
     182,
     183,
     184,
     185,
     186,
     187,
     188,
     189,
     190,
     191,
     192,
     193,
     194,
     195,
     196,
     197,
     198,
     199,
     200,
     201,
     202,
     203,
     204,
     205,
     206,
     207,
     208,
     209,
     210,
     211,
     212,
     213,
     214,
     215,
     216,
     217,
     218,
     219,
     220,
     221,
     222,
     223,
     224,
     225,
     226,
     227,
     228,
     229,
     230,
     231,
     232,
     233,
     234,
     235,
     236,
     237,
     238,
     239,
     240,
     241,
     242,
     243,
     244,
     245,
     246,
     247,
     248,
     249,
     250,
     251,
     252,
     253,
     254,
     255,
     256,
     257,
     258,
     259,
     260,
     261,
     262,
     263,
     264,
     265,
     266,
     267,
     268,
     269,
     270,
     271,
     272,
     273,
     274,
     275,
     276,
     277,
     278,
     279,
     280,
     281,
     282,
     283,
     284,
     285,
     286,
     287,
     288,
     289,
     290,
     291,
     292,
     293,
     294,
     295,
     296,
     297,
     298,
     299,
     300,
     301,
     302,
     303,
     304,
     305,
     306,
     307,
     308,
     309,
     310,
     311,
     312,
     313,
     314,
     315,
     316,
     317,
     318,
     319,
     320,
     321,
     322,
     323,
     324,
     325,
     326,
     327,
     328,
     329,
     330,
     331,
     332,
     333,
     334,
     335,
     336,
     337,
     338,
     339,
     340,
     341,
     342,
     343,
     344,
     345,
     346,
     347,
     348,
     349,
     350,
     351,
     352,
     353,
     354,
     355,
     356,
     357,
     358,
     359,
     360,
     361,
     362,
     363,
     364,
     365,
     366,
     367,
     368,
     369,
     370,
     371,
     372,
     373,
     374,
     375,
     376,
     377,
     378,
     379,
     380,
     381,
     382,
     383,
     384,
     385,
     386,
     387,
     388,
     389,
     390,
     391,
     392,
     393,
     394,
     395,
     396,
     397,
     398,
     399,
     400,
     401,
     402,
     403,
     404,
     405,
     406,
     407,
     408,
     409,
     410,
     411,
     412,
     413,
     414,
     415,
     416,
     417,
     418,
     419,
     420,
     421,
     422,
     423,
     424,
     425,
     426,
     427,
     428,
     429,
     430,
     431,
     432,
     433,
     434,
     435,
     436,
     437,
     438,
     439,
     440,
     441,
     442,
     443,
     444,
     445,
     446,
     447,
     448,
     449,
     450,
     451,
     452,
     453,
     454,
     455,
     456,
     457,
     458,
     459,
     460,
     461,
     462,
     463,
     464,
     465,
     466,
     467,
     468,
     469,
     470,
     471,
     472,
     473,
     474,
     475,
     476,
     477,
     478,
     479,
     480,
     481,
     482,
     483,
     484,
     485,
     486,
     487,
     488,
     489,
     490,
     491,
     492,
     493,
     494,
     495,
     496,
     497,
     498,
     499,
     500,
     501,
     502,
     503,
     504,
     505,
     506,
     507,
     508,
     509,
     510,
     511,
     512,
     513,
     514,
     515,
     516,
     517,
     518,
     519,
     605,
     606,
     607,
     608,
     609,
     610,
     611,
     612,
     613,
     614,
     615,
     616,
     617,
     618,
     619,
     620,
     621,
     622,
     623,
     624,
     625,
     626,
     627,
     628,
     629,
     630,
     631,
     632,
     633,
     634,
     635,
     636,
     637,
     638,
     639,
     640,
     641,
     642,
     643,
     644,
     645,
     646,
     647,
     648,
     649,
     650,
     651,
     652,
     653,
     654,
     662,
     663,
     664,
     665,
     666,
     667,
     668,
     669,
     670,
     671,
     672,
     673,
     674,
     675,
     676,
     677,
     678,
     679,
     680,
     681,
     682,
     683,
     684,
     685,
     686,
     687,
     688,
     689,
     690,
     691,
     692,
     693,
     694,
     695,
     696,
     697,
     698,
     699,
     700,
     701,
     702,
     703,
     704,
     705,
     706,
     707,
     708,
     709,
     710,
     711,
     712,
     713,
     714,
     715,
     716,
     717,
     718,
     719,
     720,
     721,
     722,
     723,
     724,
     725,
     726,
     727,
     728,
     729,
     730,
     731,
     732,
     733,
     734,
     735,
     736,
     737,
     738,
     739,
     740,
     741,
     742,
     743,
     744,
     745,
     746,
     747,
     748,
     749,
     750,
     751,
     752,
     753,
     754,
     755,
     756,
     757,
     758,
     759,
     760,
     761,
     762,
     763,
     764,
     765,
     766,
     767,
     768,
     769,
     770,
     771,
     772,
     773,
     774,
     775,
     776,
     777,
     778,
     779,
     780,
     781,
     782,
     783,
     784,
     785,
     786,
     787,
     788,
     789,
     790,
     791,
     792,
     793,
     794,
     795,
     796,
     797,
     798,
     799,
     800,
     801,
     802,
     803,
     804,
     805,
     806,
     520,
     521,
     522,
     523,
     524,
     525,
     526,
     527,
     528,
     529,
     530,
     531,
     532,
     533,
     534,
     535,
     536,
     537,
     538,
     539,
     540,
     541,
     542,
     543,
     544,
     545,
     546,
     547,
     548,
     549,
     550,
     551,
     552,
     553,
     554,
     555,
     556,
     557,
     558,
     559,
     560,
     561,
     562,
     563,
     564,
     565,
     566,
     567,
     568,
     569,
     570,
     571,
     572,
     573,
     574,
     575,
     576,
     577,
     578,
     579,
     580,
     581,
     582,
     583,
     584,
     585,
     586,
     587,
     588,
     589,
     590,
     591,
     592,
     593,
     594,
     595,
     596,
     597,
     598,
     599,
     600,
     601,
     602,
     603,
     604,
     807,
     808,
     809,
     810,
     811,
     812,
     813,
     814,
     815,
     816,
     817,
     818,
     819,
     820,
     821,
     822,
     823,
     824,
     825,
     826,
     827,
     828,
     829,
     830,
     831,
     832,
     833,
     834,
     835,
     836,
     837,
     838,
     839,
     840,
     841,
     842,
     843,
     844,
     845]
]

field_indices = [
    [1],
    [1, 2, 3, 4, 5, 6, 7, 8],
    [1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16,
     17,
     18,
     19,
     20,
     21,
     22,
     23,
     24,
     25,
     26,
     27,
     28,
     29,
     30,
     31,
     32,
     33,
     34,
     35,
     36,
     37,
     38,
     39,
     40,
     41,
     42,
     43,
     44,
     45,
     46,
     47,
     48,
     49,
     50,
     51,
     52,
     53,
     54,
     55,
     56,
     57,
     58,
     59,
     74,
     75,
     76,
     77,
     78,
     79,
     80],
    [1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     10,
     11,
     12,
     13,
     14,
     15,
     16,
     17,
     18,
     19,
     20,
     21,
     22,
     23,
     24,
     25,
     26,
     27,
     28,
     29,
     30,
     31,
     32,
     33,
     34,
     35,
     36,
     37,
     38,
     39,
     40,
     41,
     42,
     43,
     44,
     45,
     46,
     47,
     48,
     49,
     50,
     51,
     52,
     53,
     54,
     55,
     56,
     57,
     58,
     59,
     74,
     75,
     76,
     77,
     78,
     79,
     80,
     60,
     61,
     62,
     63,
     64,
     65,
     66,
     67,
     68,
     69,
     70,
     71,
     72,
     73]
]


def format_outcomes_df(outcomes_df, outcome_variable_name,
                       outcomes, id_field='fid'):
    outcomes_df[outcome_variable_name].fillna(value=False, inplace=True)
    if outcomes:
        outcomes_df = outcomes_df[outcomes_df[outcome_variable_name].isin(
            outcomes)]
    outcomes_df_subset = outcomes_df[[id_field, outcome_variable_name]]
    return outcomes_df_subset


def load_features(task):
    dataset_prediction_task_to_outcomes = {
        'all_one_trace_type': {
            'two': ['line', 'bar'],
            'three': ['line', 'scatter', 'bar'],
            'six': ['line', 'scatter', 'bar', 'box', 'histogram', 'pie'],
        },
        'has_single_src': {
            'two': [True, False]
        },
        'num_x_axes': {
            'numeric': [i for i in range(5)]
        },
        'num_y_axes': {
            'numeric': [i for i in range(5)]
        }
    }

    field_prediction_task_to_outcomes = {
        'trace_type': {
            'two': ['line', 'bar'],
            'three': ['line', 'scatter', 'bar'],
            'six': ['line', 'scatter', 'bar', 'box', 'histogram', 'heatmap'],
        },
        'is_xsrc': {
            'two': [True, False]
        },
        'is_ysrc': {
            'two': [True, False]
        },
        'is_x_or_y': {
            'two': ['x', 'y']
        },
        'is_single_src': {
            'two': [True, False]
        }
    }

    if task['dataset'] == 'dataset':
        task['features_df_file_name'] = 'features_aggregate_single_pairwise.csv'
        task['outcomes_df_file_name'] = 'chart_outcomes.csv'
        task['id_field'] = 'fid'
        prediction_task_to_outcomes = dataset_prediction_task_to_outcomes
    else:
        assert task['dataset'] == 'field'
        task['features_df_file_name'] = 'field_level_features.csv'
        task['outcomes_df_file_name'] = 'field_level_outcomes.csv'
        task['id_field'] = 'field_id'
        prediction_task_to_outcomes = field_prediction_task_to_outcomes

    features_df = pd.read_csv(
        join(
            features_directory,
            task['features_df_file_name']),
        nrows=num_datapoints)
    outcomes_df = pd.read_csv(
        join(
            features_directory,
            task['outcomes_df_file_name']),
        nrows=num_datapoints)
    feature_names_by_type = pickle.load(
        open(
            join(
                features_directory,
                feature_set_lookup_file_name),
            'rb'))

    print(features_df)
    print('Initial Features:', features_df.shape)
    print('Initial Outcomes:', outcomes_df.shape)

    if task['dataset'] == 'field':
        def is_x_or_y(is_xsrc, is_ysrc):
            if is_xsrc and pd.isnull(is_ysrc):
                return 'x'
            if is_ysrc and pd.isnull(is_xsrc):
                return 'y'
            else:
                return None

        outcomes_df['is_x_or_y'] = np.vectorize(is_x_or_y)(
            outcomes_df['is_xsrc'], outcomes_df['is_ysrc'])
        outcomes_df['is_single_src'] = outcomes_df['is_single_xsrc'] | outcomes_df['is_single_ysrc']

    outcomes_df_subset = format_outcomes_df(outcomes_df, task['outcome_variable_name'],
                                            prediction_task_to_outcomes[task['outcome_variable_name']
                                                                        ][task['prediction_task']],
                                            id_field=task['id_field'])
    final_df = join_features_and_outcomes(
        features_df, outcomes_df_subset, on=task['id_field'])
    last_index = final_df.columns.get_loc(task['outcome_variable_name'])
    X = final_df.iloc[:, :last_index]
    y = final_df.iloc[:, last_index]
    print('Intermediate Outcomes:', y.shape)
    value_counts = y.value_counts()
    print('Value counts:')
    print(value_counts)

    # delete variables to save memory!
    del final_df, outcomes_df

    task_types = ['dimensions', 'types', 'values', 'names']
    for task_name in task_types:
        names = get_feature_set_names_by_type(
            feature_names_by_type,
            task_type=task['dataset'],
            feature_set=task_name)
        indices = [X.columns.get_loc(c) for c in names if c in X.columns]
        print('task is ' + task_name + ' and indices are:')
        #print('names are {}'.format(names) )
        # print(indices)

    y = pd.get_dummies(y).values.argmax(1)

    if task['sampling_mode'] == 'over':
        res = RandomOverSampler(random_state=RANDOM_STATE)
        X, y = res.fit_sample(X, y)
    elif task['sampling_mode'] == 'under':
        res = RandomUnderSampler(random_state=RANDOM_STATE)
        X, y = res.fit_sample(X, y)
    elif isinstance(task['sampling_mode'], int):
        X_resampled_arrays, y_resampled_arrays = [], []
        for outcome in np.unique(y):
            outcome_mask = (y == outcome)
            X_resampled_outcome, y_resampled_outcome = resample(
                X[outcome_mask],
                y[outcome_mask],
                n_samples=task['sampling_mode'],
                random_state=RANDOM_STATE
            )
            X_resampled_arrays.append(X_resampled_outcome)
            y_resampled_arrays.append(y_resampled_outcome)

        X, y = np.concatenate(X_resampled_arrays).astype(
            np.float64), np.concatenate(y_resampled_arrays)
    else:
        X, y = X.values.astype(np.float64), y

    print('Final Features:', X.shape)
    print('Final Outcomes:', y.shape)
    return util.unison_shuffle(X, y)


def main():
    tasks = [None,
             {'outcome_variable_name': 'all_one_trace_type',
              'prediction_task': 'two',
              'sampling_mode': 'over',
              'pref_id': 1,
              'dataset': 'dataset'},
             {'outcome_variable_name': 'all_one_trace_type',
              'prediction_task': 'three',
              'sampling_mode': 'over',
              'pref_id': 2,
              'dataset': 'dataset'},
             {'outcome_variable_name': 'all_one_trace_type', 'prediction_task': 'six',
              'sampling_mode': 'over', 'pref_id': 3, 'dataset': 'dataset'},
             {'outcome_variable_name': 'has_single_src', 'prediction_task': 'two',
              'sampling_mode': 'over', 'pref_id': 4, 'dataset': 'dataset'},
             {'outcome_variable_name': 'num_x_axes', 'prediction_task': 'numeric',
              'sampling_mode': 10000, 'pref_id': 5, 'dataset': 'dataset'},
             {'outcome_variable_name': 'num_y_axes', 'prediction_task': 'numeric',
              'sampling_mode': 10000, 'pref_id': 6, 'dataset': 'dataset'},
             {'outcome_variable_name': 'trace_type', 'prediction_task': 'two',
              'sampling_mode': 'over', 'pref_id': 7, 'dataset': 'field'},
             {'outcome_variable_name': 'trace_type', 'prediction_task': 'three',
              'sampling_mode': 'over', 'pref_id': 8, 'dataset': 'field'},
             {'outcome_variable_name': 'trace_type', 'prediction_task': 'six',
              'sampling_mode': 'over', 'pref_id': 9, 'dataset': 'field'},
             {'outcome_variable_name': 'is_single_src', 'prediction_task': 'two',
              'sampling_mode': 'over', 'pref_id': 10, 'dataset': 'field'},
             {'outcome_variable_name': 'is_x_or_y', 'prediction_task': 'two',
              'sampling_mode': 'over', 'pref_id': 11, 'dataset': 'field'},
             ]

    for i in [1, 11]:  # range(7, len(tasks)):
        task = tasks[i]
        model_prefix = 'paper_' + task['dataset'] + '_' + str(task['pref_id'])

        parameters = {
            'batch_size': 200,
            'num_epochs': 100,
            'hidden_sizes': [1000, 1000, 1000],
            'learning_rate': 5e-4,
            'weight_decay': 0,
            'dropout': 0.00,
            'patience': 10,
            'threshold': 1e-3,
            'model_prefix': model_prefix,
            # uncomment this if you want to print test accuracies/save model
            'only_train': False,
            'save_model': True,
            'print_test': True,
            # for constructing learning curves
            'dataset_ratios': [0.01, 0.1, 0.5, 1.0],
            'test_best': True
        }

        for feature_set in [
                0, 1, 2, 3]:  # range(0, 4): # dimensions, types, values, names
            assert len(
                sys.argv) >= 2, 'You must specify a command LOAD, TRAIN, or EVAL'
            assert(parameters['model_prefix']
                   ), 'You must specify a prefix for the model name'
            if 'test_best' in parameters and parameters['test_best']:
                assert parameters['save_model'], 'You must save a model to test the best version!'

            command = sys.argv[1].lower()
            if command == 'load':
                X, y = load_features(task)
                util.save_matrices_to_disk(
                    X, y, [0.2, 0.2], saves_directory, parameters['model_prefix'], num_datapoints)
            else:
                X_train, y_train, X_val, y_val, X_test, y_test = util.load_matrices_from_disk(
                    saves_directory, parameters['model_prefix'], num_datapoints)

                if task['dataset'] == 'dataset':
                    X_train = X_train[:, dataset_indices[feature_set]]
                    X_val = X_val[:, dataset_indices[feature_set]]
                    X_test = X_test[:, dataset_indices[feature_set]]
                else:
                    assert task['dataset'] == 'field'
                    X_train = X_train[:, field_indices[feature_set]]
                    X_val = X_val[:, field_indices[feature_set]]
                    X_test = X_test[:, field_indices[feature_set]]
                print('loaded dimensions are', X_train.shape)
                print('task_num and feature_set:(' +
                      str(task['pref_id']) + ',' + str(feature_set) + ')')

                if command == 'train':
                    train_dataloader, val_dataloader, test_dataloader = train.load_datasets(
                        X_train, y_train, X_val, y_val, parameters, X_test=X_test, y_test=y_test)
                    train.train(
                        train_dataloader,
                        val_dataloader,
                        test_dataloader,
                        parameters,
                        models_directory=models_directory,
                        suffix=suffix)
                elif command == 'eval':
                    assert len(sys.argv) >= 3
                    model_suffix = sys.argv[2]
                    train_dataloader, val_dataloader, test_dataloader = train.load_datasets(
                        X_train, y_train, X_val, y_val, parameters, X_test=X_test, y_test=y_test)
                    evaluate.evaluate(
                        model_suffix, test_dataloader, parameters)
                else:
                    assert False, 'The command must either be LOAD, TRAIN, or EVAL'


if __name__ == '__main__':
    main()
