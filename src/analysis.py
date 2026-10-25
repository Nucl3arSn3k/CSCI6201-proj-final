from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

def linear_regression(df:pd.DataFrame) -> None:
    print("Wallfacer.")




def inital_analysis(df:pd.DataFrame) -> None:
    print(df.shape)
    #feature nums
    print(len(df.columns))

    #feature names
    print(df.columns)

    #target variable is sancomplaintcoutn
    #classification or regression task

    #Regression


def load_data() -> pd.DataFrame: #loading compressed dataset as uncompressed doesn't fit in github
    return pd.read_csv(DATA_DIR / "311_City_Service_Requests_in_2025.csv.gz")

def explore_data(df:pd.DataFrame) -> None:
    print("Data exploration")
    #exploratory
    print(df.shape)
    #descriptive stats

    #min and max
    print(df.min(axis=0))
    print(df.max(axis=0))

    #averages

    #class counts
    print("Class countse")
    print(df["SERVICECODEDESCRIPTION"].value_counts())
    print(df["WARD"].value_counts())
    #missing value checks
    print("Missing value check")
    print(df.isna().sum())

def delve(df: pd.DataFrame,cg) -> None:
    # category ("class") counts for columns tied to the research questions
    for col in cg:
        print(f"\n{col}: {df[col].nunique()} distinct values")
        print(df[col].value_counts(dropna=False).head(15))

def visualization(df: pd.DataFrame) -> None:
    #generates charts.
    mask = df["SERVICETYPECODEDESCRIPTION"].str.contains("SWMA", na=False)
    san = df.loc[mask]
    print(san["SERVICECODEDESCRIPTION"].value_counts())
    SMELL_TYPES = [
        "Trash Collection - Missed",
        "Illegal Dumping",
        "Sanitation Enforcement",
        "Dead Animal Collection",
        "Alley Cleaning",
        "Street Cleaning",
        "Rat Replacement Containers",
        "Public Space Litter Can-Collection",
    ]

    san = df.loc[df["SERVICECODEDESCRIPTION"].isin(SMELL_TYPES)]

def main():
    df = load_data()
    """

    #inital_analysis(df)
    explore_data(df)

    CATEGORY_COLUMNS = [
        "SERVICECODEDESCRIPTION",
        "SERVICETYPECODEDESCRIPTION",
        "WARD",
        "SERVICEORDERSTATUS",
        "PRIORITY",
        "ORGANIZATIONACRONYM",
    ]
    delve(df,CATEGORY_COLUMNS)
    """
    visualization(df)





if __name__ == "__main__":
    main()
