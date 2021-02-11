import pandas as pd
import os

languages_path = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "language.csv")
languages_wals_data = pd.read_csv(languages_path)

countries_path = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "country.csv")
countries_wals_data = pd.read_csv(countries_path)

countries_languages_path = os.path.join("data", "cldf-datasets-wals-014143f", "raw", "countrylanguage.csv")
countries_languages_wals_data = pd.read_csv(countries_languages_path)

temp = pd.merge(countries_wals_data[['pk','name','continent']], countries_languages_wals_data[['country_pk','language_pk']], how='outer', left_on=['pk'], right_on=['country_pk'])
temp.drop('pk', axis=1, inplace=True)
temp.rename(columns = {'name':'country_name'}, inplace = True)
languages_countries_joined = pd.merge(temp, languages_wals_data, how='left', left_on=['language_pk'], right_on=['pk'])

languages_countries_joined.to_csv('data/cldf-datasets-wals-014143f/created/lang_country_info.csv', index=False)
