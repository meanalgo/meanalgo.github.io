import pandas as pd
url = 'https://github.com/meanalgo/meanalgo.github.io/raw/main/data/20220203_mean_reversion.csv'
df = pd.read_csv(url,index_col=0)

print(df)
