from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data(): #loading compressed dataset as uncompressed doesn't fit in github
    return pd.read_csv(DATA_DIR / "311_City_Service_Requests_in_2025.csv.gz")

def main():
    df = load_data()
    print(df.shape)
    print(df.min(axis=0))


if __name__ == "__main__":
    main()
