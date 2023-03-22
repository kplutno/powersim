import pandas as pd
import requests
from dotenv import load_dotenv
import os



def add_ure_res_grid_coordinates(config):
    token = os.getenv("METEO_API_KEY")
    headers = {"Authorization": f"Token {token}"}
    res_sources = pd.read_csv(
        config.data.clean_res_list.path
    )
    
    types_of_res = config.data.ure_res_list_rowcol.types_of_res
    res_sources = res_sources.loc[res_sources["rodzaj"].isin(types_of_res)]
    
    models = config.meteo.models
    url_template = config.meteo.api.url_rowcol
    
    fetched = dict()
    
    for model, value in models.items():
        # Get grids
        grids = value.grids
        
        for grid in grids:
            # create processing function
            def rowcol(row):
                lat = row["lat"]
                lon = row["lon"]
                latlon = f"{lat},{lon}"
                
                find_fetched = fetched.get(latlon, None)
                
                if find_fetched is None:
                    url = url_template.format(model=model, grid=grid, latlon=latlon)
                    request = requests.get(url, headers=headers)
                    data = request.json()["points"][0]
                    rowcol = f"{data['row']},{data['col']}"
                    fetched[latlon] = rowcol
                    return rowcol
                
                return find_fetched
                
            res_sources[grid] = res_sources.apply(rowcol, axis=1)

    res_sources.to_csv(
        config.data.ure_res_list_rowcol.path
    )
