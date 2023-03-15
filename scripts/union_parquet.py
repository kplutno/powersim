import pandas as pd

if __name__=="__main__":
    parquet_directory = "./data/clean_topo"
    df = pd.read_parquet(parquet_directory)
    df = df.loc[df["rodzaj"] == "Twt"]
    
    df_2 = pd.read_csv("./data/clean_res_list.csv")
    df_2 = df_2.loc[df_2["rodzaj"] == "WIL"]
    
    print(df_2)