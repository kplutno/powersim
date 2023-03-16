import pandas as pd
import geopandas
from pyproj import Proj, Transformer

if __name__ == "__main__":
    parquet_directory = "./data/clean_topo"
    output_parquet_directory = "./data/wind_turbines.parquet"
    df = pd.read_parquet(parquet_directory)
    df = df.loc[df["rodzaj"] == "Twt"]
    df = df[["x", "y", "wysokosc"]]

    transformer = Transformer.from_crs("ESRI:102173", "epsg:4326")

    df["lon"] = df.apply(lambda row: transformer.transform(row["x"], row["y"])[0], axis=1)
    df["lat"] = df.apply(lambda row: transformer.transform(row["x"], row["y"])[1], axis=1)

    df.to_parquet(output_parquet_directory)
