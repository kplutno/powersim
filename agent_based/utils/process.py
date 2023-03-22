import pandas as pd
from box import Box
import yaml
from yaml.loader import FullLoader
import requests
from urllib.parse import quote
import time
from unidecode import unidecode
from logging.config import dictConfig
import logging
import glob


def process_ure_rse_source(config: Box):
    logger = logging.getLogger(__name__)

    logger.info("Processing RSE data source.")
    logger.info(f"Loading {config.data.res_list.path} file.")

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
            value = 51.9189046
        return value

    def get_lon(row):
        state = row["woje"]
        county = row["powiat"]
        query_string = f"country={quote(country)}&state={quote(state)}&county={quote(county)}&format=json"
        if len(locs[query_string]) > 0:
            value = locs[query_string][0]["lon"]
        else:
            value = 19.1343786
        return value

    res["lat"] = res.apply(get_lat, axis=1)
    res["lon"] = res.apply(get_lon, axis=1)
    res["woje"] = res.apply(lambda x: unidecode(x["woje"]), axis=1)
    res["powiat"] = res.apply(lambda x: unidecode(x["powiat"]), axis=1)

    logger.info(f"Saving to {config.data.clean_res_list.path} file.")
    res.to_csv(config.data.clean_res_list.path)
    return res


def load_clean_res_data(config: Box):
    logger = logging.getLogger(__name__)

    logger.info(f"Loading dataset {config.data.ure_res_list_rowcol.path}")
    res = pd.read_csv(
        config.data.ure_res_list_rowcol.path,
    )

    wind = res.loc[res["rodzaj"] == "WIL"]
    pv = res.loc[res["rodzaj"] == "PVA"]

    return wind, pv, res


def load_config(config_path: str):
    logger = logging.getLogger(__name__)
    logger.info(f"Loading config from folder {config_path}")
    config = dict()
    files = glob.glob(config_path)
    
    
    for file in files:
        config.update(read_yaml_file(file))

    dictConfig(config)
    config = Box(config)

    return config


def read_yaml_file(filename):
    with open(filename, "r") as f:
        try:
            yml = yaml.load(f, Loader=FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    return yml
