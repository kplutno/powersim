import pandas as pd
import geopandas
from pyproj import Proj, Transformer
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # parquet_directory = "./data/wind_turbines.parquet"
    # df = geopandas.read_parquet(parquet_directory)
    # #df = df.loc[df["rodzaj"] == "Twt"]
    # print(df)
    # df.plot(column="wysokosc", marker="*", markersize=1)
    # plt.savefig('books_read.png')
    
    poland_shapefile_directory = "./data/pl_10km.shp"
    df_poland = geopandas.read_file(poland_shapefile_directory)
    df_poland.plot()
    plt.savefig("/data/poland.png")