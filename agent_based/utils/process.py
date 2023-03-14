import pandas as pd
from box import Box
import yaml
from yaml.loader import FullLoader

def process_ure_rse_source(config: Box):
    res = pd.read_excel(
        config.data.res_list.path,
    )
    res = res.rename(mapper=config.data.res_list.columns_rename, axis=1)
    res.drop(["lp"], axis=1)
    wind = res.loc[res['rodzaj'] == "WIL"]
    pv = res.loc[res['rodzaj'] == "PVA"]
    return res, wind, pv
    
def load_config(config_path: str):
    with open(config_path) as f:
        config = yaml.load(f, Loader=FullLoader)
    config = Box(config)
    
    return config
