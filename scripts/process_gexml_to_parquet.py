import geopandas
import pandas as pd
import os

if __name__=="__main__":
    path = "./data/topograficzne"
    output_path = "./data/clean_topo"
    list_of_dir = os.listdir(path)
    
    dataframes = []
    
    for dir in list_of_dir:
        inner_path = os.path.join(path, dir, "GOTOWE")
        for file in os.listdir(inner_path):
            file_path = os.path.join(inner_path, file)
            
            if file_path.find("BUWT_P") != -1 and file_path.find(".gfs") == -1:
                df = geopandas.read_file(file_path)
                filename = os.path.splitext(os.path.basename(file))[0] + ".parquet"
                df.to_parquet(os.path.join(output_path, filename))
    
    
    