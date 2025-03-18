import json
import pandas as pd
import random
import numpy as np

def modify_base_df(df, w_distance=0.7, w_noise=0.3):
    # Step 1: Add a column with random noise (comparable to min_distance_to_grid_km)
    noise = np.random.normal(loc=0, scale=df['min_distance_to_grid_km'].mean(), size=len(df))
    df['noise'] = noise

    # Step 2: Compute the final_value as a linear combination of min_distance_to_grid_km and noise
    df['final_value'] = w_distance * df['min_distance_to_grid_km'] + w_noise * df['noise']

    # Step 3: Print the first few rows to verify the changes
    print(df.head())

    return df