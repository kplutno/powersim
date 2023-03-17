import os
import geopandas

def process_topo(config):
    path = config.data.topo_data.input_path
    output_path = config.data.topo_data.output_path
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
