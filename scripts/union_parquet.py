import pandas as pd

if __name__=="__main__":
    parquet_directory = "./data/clean_topo"
    df = pd.read_parquet(parquet_directory)
    
    print(df.shape)