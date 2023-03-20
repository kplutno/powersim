import pandas as pd

def add_net_coordinates(config):
    res_sources = pd.read_csv(
        config.data.clean_res_list.path
    )
    
    res_sources["net_um_x"] = res_sources.apply( ,axis=1)