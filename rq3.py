# %%
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def fix_city(city_string):
  final_string = city_string
  split_string = city_string.split(': ')

  if len(split_string) == 2:
    split_string[0], split_string[len(split_string) - 1] = split_string[len(split_string) - 1], split_string[0]
    final_string = split_string[0] + ", " + split_string[1]

  return final_string

def fix_city_for_protests(city_string):
  split_string = city_string.split(', ')
  final_string = city_string
  if len(split_string) == 3:
    split_string.pop(0)
    final_string = split_string[0] + ", " + split_string[1]

  return final_string

protests = pd.read_csv('part three dataset/protests.csv')
pd.to_datetime(protests['Date'])

start_date = '2020-05-25'
end_date = '2020-07-31'

after_start_date = protests['Date'] >= start_date
before_end_date = protests['Date'] <= end_date
between_two_dates = after_start_date & before_end_date
filtered_dates = protests.loc[between_two_dates].reset_index()

df = filtered_dates.Location.value_counts().rename_axis('locations').reset_index(name='counts')
df.locations = df.apply(lambda x: fix_city_for_protests(x['locations']), axis=1)
df
# %%

budgets = pd.read_csv('part two dataset/police_info/budgets.csv')

budgets.columns

pd.to_numeric(budgets['year'])

budgets_2017 = budgets[budgets['year'] == 2017].reset_index()

police_cols = [col for col in budgets.columns if 'police' in col]

correction_cols = [col for col in budgets.columns if 'correction' in col]

budgets_2017 = budgets_2017[police_cols + ['city_name']]

budgets_2017.city_name = budgets_2017.apply(lambda x: fix_city(x['city_name']), axis=1)

budgets_2017.fillna(0)

# %%
result = budgets_2017.merge(df, how='right', left_on='city_name', right_on='locations').fillna(0)

result.drop(result[result['city_name'] == 0.0].index, inplace=True)
result.drop(result[result['counts'] == 0.0].index, inplace=True)

result = result.reset_index(drop=True)

result
# %%
sns.scatterplot(x=result.counts, y=result.police)
plt.title("Protests vs Police Expenditures")
plt.show()

# %%
correlation = result.corr()
print(correlation)

# %%
sns.heatmap(correlation)
plt.show()