from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def inital_analysis() -> None:
    print("Wallfacer")

def load_data() -> pd.DataFrame: #loading compressed dataset as uncompressed doesn't fit in github
    return pd.read_csv(DATA_DIR / "311_City_Service_Requests_in_2025.csv.gz")

def explore_data(df:pd.DataFrame) -> None:
    #exploratory
    print(df.shape)
    #descriptive stats

    #min and max
    print(df.min(axis=0))
    print(df.max(axis=0))

    #averages

    #class counts

    #missing value checks


def main():
    df = load_data()
    explore_data(df)



if __name__ == "__main__":
    main()
