import pandas as pd
from box import Box
import yaml
from yaml.loader import FullLoader
import requests
from urllib.parse import quote
import time


def process_ure_rse_source(config: Box):
    res = pd.read_excel(
        config.data.res_list.path,
    )
    res = res.rename(mapper=config.data.res_list.columns_rename, axis=1)
    res["powiat"] = res.apply(lambda row: row["powiat"].replace("m. ", ""), axis=1)
    res["powiat"] = res.apply(lambda row: row["powiat"].replace("m.st. ", ""), axis=1)
    res.drop(["lp"], axis=1)

    locs = dict()
    country = config.data.res_list.geo.country
    for index, row in res.iterrows():
        state = row["woje"]
        county = row["powiat"]
        query_string = f"country={quote(country)}&state={quote(state)}&county={quote(county)}&format=json"
        find_in_dict = locs.get(query_string, None)

        if find_in_dict is None:
            url = f"https://nominatim.openstreetmap.org/search?{query_string}"
            response = requests.get(url).json()
            locs[query_string] = response
            time.sleep(0.3)

    def get_lat(row):
        state = row["woje"]
        county = row["powiat"]
        query_string = f"country={quote(country)}&state={quote(state)}&county={quote(county)}&format=json"
        if len(locs[query_string]) > 0:
            value = locs[query_string][0]["lat"]
        else:
            value = ""
        return value

    def get_lon(row):
        state = row["woje"]
        county = row["powiat"]
        query_string = f"country={quote(country)}&state={quote(state)}&county={quote(county)}&format=json"
        if len(locs[query_string]) > 0:
            value = locs[query_string][0]["lon"]
        else:
            value = ""
        return value

    res["lat"] = res.apply(get_lat, axis=1)
    res["lon"] = res.apply(get_lon, axis=1)

    res.to_csv(config.data.clean_res_list.path)
    return res

def load_clean_res_data(config: Box):
    res = pd.read_csv(
        config.data.clean_res_list.path,
    )
    
    wind = res.loc[res["rodzaj"] == "WIL"]
    pv = res.loc[res["rodzaj"] == "WIL"]
    
    return wind, pv, res

def load_config(config_path: str):
    with open(config_path) as f:
        config = yaml.load(f, Loader=FullLoader)
    config = Box(config)

    return config
