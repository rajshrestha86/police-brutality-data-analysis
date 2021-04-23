# %%
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

police_killings = pd.read_csv('part one dataset/police_killings_MPV.csv')

del police_killings["Unnamed: 29"]
del police_killings["Unnamed: 30"]
del police_killings["Unnamed: 31"]
del police_killings["Unnamed: 32"] 
del police_killings["Unnamed: 33"] 
del police_killings["Unnamed: 34"]
del police_killings["Unnamed: 35"]
del police_killings["Unnamed: 36"]
del police_killings["Unnamed: 37"]
del police_killings["Unnamed: 38"]
del police_killings["Unnamed: 39"]
del police_killings["Unnamed: 40"]
del police_killings["Unnamed: 41"]
del police_killings["Unnamed: 42"]
del police_killings["Unnamed: 43"]
del police_killings["Unnamed: 44"]
del police_killings["Unnamed: 45"]
del police_killings["Unnamed: 46"]
del police_killings["Unnamed: 47"]
del police_killings["Unnamed: 48"]
del police_killings["Unnamed: 49"]
del police_killings["Unnamed: 50"]
del police_killings["Unnamed: 51"]
del police_killings["Unnamed: 52"]
del police_killings["Unnamed: 53"]
del police_killings["Unnamed: 54"]
del police_killings["Unnamed: 55"]
del police_killings["Unnamed: 56"]
del police_killings["Unnamed: 57"]
del police_killings["Unnamed: 58"]
del police_killings["Unnamed: 59"]
del police_killings["Unnamed: 60"]
del police_killings["Unnamed: 61"]
del police_killings["Unnamed: 62"]
del police_killings["Unnamed: 63"]
del police_killings["Unnamed: 64"]
del police_killings["Unnamed: 65"]
del police_killings["Unnamed: 66"]
del police_killings["Unnamed: 67"]
del police_killings["Fatal Encounters ID"]
del police_killings["MPV ID"]
del police_killings["Geography (via Trulia methodology based on zipcode population density: http://jedkolko.com/wp-content/uploads/2015/05/full-ZCTA-urban-suburban-rural-classification.xlsx )"]
del police_killings["URL of image of victim"]
del police_killings["Street Address of Incident"]
del police_killings["Zipcode"]
del police_killings["County"]
del police_killings["Link to news article or photo of official document"]
del police_killings["ORI Agency Identifier (if available)"]
del police_killings["WaPo ID (If included in WaPo database)"]
del police_killings["Criminal Charges?"]
del police_killings["Agency responsible for death"]
del police_killings["A brief description of the circumstances surrounding the death"]
del police_killings["Alleged Threat Level (Source: WaPo)"]
del police_killings["Body Camera (Source: WaPo)"]
del police_killings["Fleeing (Source: WaPo)"]
del police_killings["Off-Duty Killing?"]
del police_killings["Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)"]
del police_killings["Official disposition of death (justified or other)"]
del police_killings["Symptoms of mental illness?"]

police_killings["Date of Incident (month/day/year)"] = pd.to_datetime(police_killings["Date of Incident (month/day/year)"], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

# %%

start_date = "2020-05-25"
end_date = "2020-07-31"

after_start_date = police_killings["Date of Incident (month/day/year)"] >= start_date
before_end_date = police_killings["Date of Incident (month/day/year)"] <= end_date
between_two_dates = after_start_date & before_end_date
filtered_police_killings = police_killings.loc[between_two_dates].reset_index(drop=True)
filtered_police_killings["Location"] = filtered_police_killings["City"] + ", " + filtered_police_killings["State"]

del filtered_police_killings["City"]
del filtered_police_killings["State"]

filtered_police_killings

# %%
deaths_by_race = filtered_police_killings["Victim's race"].value_counts().rename_axis('race').reset_index(name='counts')
# %%
deaths_by_race = deaths_by_race[deaths_by_race.race != 'Unknown race']
# %%

deaths_by_race['death_perc'] = deaths_by_race['counts'] / deaths_by_race['counts'].sum()

deaths_by_race

# %%
# trying to show a timeline of the deaths

timeline = filtered_police_killings["Date of Incident (month/day/year)"].value_counts().rename_axis('incident_dates').reset_index(name='counts')

pd.to_datetime(timeline.incident_dates)

timeline.sort_values(by=["incident_dates"], inplace=True, ascending=True)

timeline = timeline.reset_index(drop=True)

# %%
sns.lineplot(data=timeline)
plt.show()
# %%

partisan_and_republican = pd.read_csv('part two dataset/demographics/politics_538.csv')

partisan_and_republican
# %%

deaths_by_city = filtered_police_killings["Location"].value_counts().rename_axis('Location').reset_index(name='counts')

deaths_by_city
# %%

result = pd.merge(partisan_and_republican, deaths_by_city, on="Location")
result

# %%

sns.scatterplot(data=result, x="Republican Vote Share", y="Partisan Segregation", hue="counts")
plt.show()
# %%
