#translates country and region column from scraped data
from googletrans import Translator
import pandas as pd
from tqdm import tqdm
import time
tqdm.pandas()

translator = Translator()
def translate_google(text):
    if pd.isna(text) or text == '':
        return text
    try:
        time.sleep(0.5)
        return translator.translate(text, src='zh-cn', dest='en').text
    except:
        return text

targetfile = 'mfa_2025-11-26.csv'

df = pd.read_csv(targetfile)
unique_regions = df['region'].dropna().unique()
region_map = {region: translate_google(region) for region in tqdm(unique_regions)}
df['region'] = df['region'].map(region_map).fillna(df['region'])

unique_countries = df['country'].dropna().unique()
country_map = {country: translate_google(country) for country in tqdm(unique_countries)}
df['country'] = df['country'].map(country_map).fillna(df['country'])

df['region'] = df['region'].str.upper()
df['country'] = df['country'].str.upper()

df.to_csv(f'EN_{targetfile}', index=False)