from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import regression

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FIGURES_DIR = Path(__file__).resolve().parent.parent / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

def linear_regression(df:pd.DataFrame) -> None:
    print("Wallfacer.")




def inital_analysis(df:pd.DataFrame) -> None:
    print("\n=== Initial analysis ===")
    print("Shape (rows, columns):", df.shape)
    print("Number of samples (rows, one per 311 request):", df.shape[0])
    #feature nums
    print("Number of features (columns):", len(df.columns))

    #feature names
    print("Feature names:")
    print(df.columns.tolist())
    print("Feature data types:")
    print(df.dtypes)

    #target variable is sancomplaintcoutn
    print("Target variable: sancompcount (smell-type 311 requests per grid cell)")
    print("It is not a raw column; it is derived per grid cell in build_cell_table()")
    #classification or regression task
    print("Task: regression (the target is a count, not a category)")

    #Regression


def load_data() -> pd.DataFrame: #loading compressed dataset as uncompressed doesn't fit in github
    return pd.read_csv(DATA_DIR / "311_City_Service_Requests_in_2025.csv.gz")

def explore_data(df:pd.DataFrame) -> None:
    print("\n=== Data exploration ===")
    #exploratory
    print("Shape (rows, columns):", df.shape)
    #descriptive stats
    print("\nDescriptive statistics (numeric columns):")
    print(df.describe())

    #min and max
    print("\nMinimum of each numeric column:")
    print(df.min(axis=0, numeric_only=True))
    print("\nMaximum of each numeric column:")
    print(df.max(axis=0, numeric_only=True))

    #averages
    print("\nMean of each numeric column:")
    print(df.mean(axis=0, numeric_only=True))
    dates = pd.to_datetime(df["ADDDATE"], utc=True, errors="coerce")
    print("\nRequest date range (ADDDATE):", dates.min(), "to", dates.max())

    #class counts
    print("\nClass counts")
    print("SERVICECODEDESCRIPTION:", df["SERVICECODEDESCRIPTION"].nunique(), "distinct values")
    print(df["SERVICECODEDESCRIPTION"].value_counts())
    print("\nWARD:", df["WARD"].nunique(), "distinct values")
    print(df["WARD"].value_counts())
    #missing value checks
    print("\nMissing value check")
    print(df.isna().sum())
    print("\nPercent missing per column:")
    print((df.isna().mean() * 100).round(2))
    print("\nColumns that are entirely empty:", df.columns[df.isna().all()].tolist())

def delve(df: pd.DataFrame,cg) -> None:
    # category ("class") counts for columns tied to the research questions
    print("\n=== Category counts for research-question columns ===")
    for col in cg:
        print(f"\n{col}: {df[col].nunique()} distinct values")
        counts = df[col].value_counts(dropna=False).head(15)
        percent = (counts / len(df) * 100).round(2)
        print(pd.DataFrame({"count": counts, "percent": percent}))

def visualization_filter(df: pd.DataFrame) -> list[str]:
    #generates charts.
    mask = df["SERVICETYPECODEDESCRIPTION"].str.contains("SWMA", na=False)
    san = df.loc[mask]
    print("\n=== Solid-waste (SWMA) requests ===")
    print("SWMA rows:", len(san), f"({len(san) / len(df) * 100:.1f}% of all requests)")
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
    ] #narrow list that should proxy for the types of mess we find near bars, May also include abandonded bicycles

    san = df.loc[df["SERVICECODEDESCRIPTION"].isin(SMELL_TYPES)]
    print("\n=== Smell-type requests (narrow list) ===")
    print("Smell-type rows:", len(san), f"({len(san) / len(df) * 100:.1f}% of all requests)")
    print(san["SERVICECODEDESCRIPTION"].value_counts())
    present = set(df["SERVICECODEDESCRIPTION"].unique())
    not_found = [t for t in SMELL_TYPES if t not in present]
    if not_found:
        print("WARNING: these smell types do not appear in the data:", not_found)

    #print(type(san))
    #same dataframe type
    scatter_plot(san)
    plot_top_request_types(san)

    return SMELL_TYPES


def scatter_plot(df: pd.DataFrame) -> None:
    SHAW_BOX = {"lon_min": -77.034, "lon_max": -77.019,
                "lat_min": 38.907, "lat_max": 38.916}


    fig, ax = plt.subplots(figsize=(8,8))
    ax.scatter(df["LONGITUDE"],df["LATITUDE"],s=2,alpha=0.3)

    b = SHAW_BOX
    in_shaw = df[
        df["LONGITUDE"].between(b["lon_min"], b["lon_max"])
        & df["LATITUDE"].between(b["lat_min"], b["lat_max"])
    ]
    print("\n=== Scatter plot ===")
    print("Points plotted:", len(df))
    print(
        "Points inside the Shaw box:", len(in_shaw),
        f"({len(in_shaw) / max(len(df), 1) * 100:.1f}% of points)",
    )
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
    print("Saved:", FIGURES_DIR / "01_sanitation_map.png")

def plot_top_request_types(df: pd.DataFrame) -> None:
    counts = df["SERVICECODEDESCRIPTION"].value_counts().head(10)
    print("\n=== Bar chart: top request types plotted ===")
    print(counts)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(counts.index.tolist(), counts.to_numpy())
    ax.invert_yaxis()  # largest bar on top

    ax.set_title("Top 10 311 request types, 2025")
    ax.set_xlabel("Number of requests")
    ax.set_ylabel("Request type")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "02_top_request_types.png", dpi=160)
    plt.close(fig)
    print("Saved:", FIGURES_DIR / "02_top_request_types.png")

def build_cell_table(df: pd.DataFrame,smell_types: list[str]) -> pd.DataFrame:
    cell_x = (df["LONGITUDE"] // 0.003).astype(int)
    cell_y = (df["LATITUDE"] // 0.003).astype(int)
    is_smell = df["SERVICECODEDESCRIPTION"].isin(smell_types)

    cells = (
        pd.DataFrame({"cell_x": cell_x, "cell_y": cell_y, "is_smell": is_smell})
        .groupby(["cell_x", "cell_y"])["is_smell"]
        .agg(["sum", "size"])
        .reset_index()
    )
    cells["sancompcount"] = cells["sum"]
    cells["other_requests"] = cells["size"] - cells["sum"]

    print("\n=== Cell table (one row per grid cell) ===")
    print("Grid cells (samples for the model):", len(cells))
    print("Smell-type requests across all cells:", cells["sancompcount"].sum())
    print("Cells with zero smell-type requests:", (cells["sancompcount"] == 0).sum())
    print("\nTarget (sancompcount) distribution:")
    print(cells["sancompcount"].describe())
    print("\nFeature (other_requests) distribution:")
    print(cells["other_requests"].describe())
    return cells


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
    filtlist = visualization_filter(df) #bar chart and scatter plot
    cells = build_cell_table(df,filtlist)  # one row per cell, has sancompcount
    print("\nFirst rows of the cell table:")
    print(cells.head())
    print("Cell table shape (cells, columns):", cells.shape)
    print("\n=== Regression ===")
    regression.run_model(cells)




if __name__ == "__main__":
    main()
