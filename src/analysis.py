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

def visualization_filter(df: pd.DataFrame) -> None:
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
    ] #narrow list that should proxy for the types of mess we find near bars

    san = df.loc[df["SERVICECODEDESCRIPTION"].isin(SMELL_TYPES)]

    #print(type(san))
    #same dataframe type
    scatter_plot(san)


def scatter_plot(df: pd.DataFrame) -> None:
    SHAW_BOX = {"lon_min": -77.034, "lon_max": -77.019,
                "lat_min": 38.907, "lat_max": 38.916}


    fig, ax = plt.subplots(figsize=(8,8))
    ax.scatter(df["LONGITUDE"],df["LATITUDE"],s=2,alpha=0.3)

    b = SHAW_BOX
    ax.plot(
        [b["lon_min"], b["lon_max"], b["lon_max"], b["lon_min"], b["lon_min"]],
        [b["lat_min"], b["lat_min"], b["lat_max"], b["lat_max"], b["lat_min"]],
        color="green",
    )

    ax.set_title("Sanitation-type 311 requests, Washington DC, 2025")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal")
    fig.savefig(FIGURES_DIR / "01_sanitation_map.png", dpi=160)
    plt.close(fig)

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
    visualization_filter(df)





if __name__ == "__main__":
    main()
