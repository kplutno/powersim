import pandas as pd

if __name__ == "__main__":
    df = pd.read_parquet("./data/output")
    
    df.info(verbose=True)