"""EDA: understand structure, coverage, and quality of ipl.csv before analysis."""
import pandas as pd

df = pd.read_csv('ipl.csv')
df['match_date'] = pd.to_datetime(df['match_date'])

print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nDate range:", df.match_date.min().date(), "->", df.match_date.max().date())

print("\nMatches per season:")
print(df.groupby('season').size().to_string())

print("\nNull counts:")
print(df.isnull().sum().to_string())

print("\nMatch types:", df['match_type'].value_counts().to_dict())
print("Results:", df['result'].value_counts().to_dict())
print("Super overs:", df['super_over'].value_counts().to_dict())
print("Toss decisions:", df['toss_decision'].value_counts().to_dict())
print("\nDistinct venues:", df['venue'].nunique(), "| cities:", df['city'].nunique(),
      "| teams(t1):", df['team1'].nunique())

num_cols = ['result_margin', 'target_runs', 'target_overs']
print("\nNumeric summaries:")
print(df[num_cols].describe().round(2).to_string())

# how many rows in 2008-2018 window?
mask = (df['match_date'] >= '2008-01-01') & (df['match_date'] <= '2018-12-31')
print("\nMatches in 2008-2018 window:", mask.sum())
