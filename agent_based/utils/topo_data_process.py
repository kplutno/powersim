import os
import geopandas
from pyproj import Transformer

def process_topo(config):
    path = config.data.topo_data.input_path
    output_path = config.data.topo_data.output_path
    output_wind_turbines_path = config.data.wind_turbines.output_path
    
    list_of_dir = os.listdir(path)
    
    for dir in list_of_dir:
        inner_path = os.path.join(path, dir, "GOTOWE")
        for file in os.listdir(inner_path):
            file_path = os.path.join(inner_path, file)
            
            if file_path.find("BUWT_P") != -1 and file_path.find(".gfs") == -1:
                df = geopandas.read_file(file_path)
                df["x"] = df["geometry"].x
                df["y"] = df["geometry"].y
                filename = os.path.splitext(os.path.basename(file))[0] + ".parquet"
                df.to_parquet(os.path.join(output_path, filename))

    parquet_directory = output_path
    df = geopandas.read_parquet(parquet_directory)
    df = df.loc[df["rodzaj"] == "Twt"]
    df = df[["x", "y", "wysokosc", "geometry"]]

    transformer = Transformer.from_crs("ESRI:102173", "epsg:4326")

    df["lon"] = df.apply(lambda row: transformer.transform(row["x"], row["y"])[0], axis=1)
    df["lat"] = df.apply(lambda row: transformer.transform(row["x"], row["y"])[1], axis=1)

    df.to_parquet(output_wind_turbines_path)