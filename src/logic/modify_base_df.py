import json
import pandas as pd
import random
import numpy as np

def modify_base_df(df, w_distance=0.1, w_noise=0.9):

    noise = np.random.normal(loc=0, scale=df['min_distance_to_grid_km'].mean(), size=len(df))
    df['noise'] = noise

    df['final_value'] = w_distance * df['min_distance_to_grid_km'] + w_noise * df['noise']

    print(df.head())

    return df