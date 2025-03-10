import pandas as pd

input_path = '../data/raw/wind-data-main.csv'
output_path = '../data/processed/wind-farms.csv'

df = pd.read_csv(input_path, sep=';', decimal=',')

df.rename(columns={df.columns[-1]: 'Capacity (MW_ac)'}, inplace=True)
df = df.drop(df.columns[0], axis=1)

df.to_csv(output_path, sep=',', index=False)

# pd.set_option('display.max_columns', None)
df = pd.read_csv('../data/processed/wind-farms.csv')
print(df.head(68))

