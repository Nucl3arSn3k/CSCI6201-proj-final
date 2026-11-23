from pathlib import Path

import pandas as pd

CELL = 0.003  # degrees; MUST match build_cell_table() in analysis.py

# Not physical places where people drink or buy alcohol, so bye bye
EXCLUDE_TYPES = {"Third-Party Delivery"}



def show_license_types(lic: pd.DataFrame) -> None:
    """Run this first and look at it before touching GROUPS in bars.py."""
    print("\n=== License TYPE counts ===")
    print(lic["TYPE"].value_counts(dropna=False))
    print("\n=== CLASS counts ===")
    print(lic["CLASS"].value_counts(dropna=False))
    print("\n=== STATUS counts ===")
    print(lic["STATUS"].value_counts(dropna=False))


def clean_licenses(raw: pd.DataFrame) -> pd.DataFrame:
    n0 = len(raw)
    lic = raw.copy()
    lic["TYPE"] = lic["TYPE"].astype("string").str.strip()

    # Using .loc[mask] (not lic[mask]) keeps the type checker happy: it is
    # typed as returning a DataFrame, whereas lic[...] is Series | DataFrame.
    lic = lic.loc[lic["STATUS"].eq("ACTIVE")]
    print(f"Active licenses: {len(lic)} of {n0}")

    lic = lic.loc[~lic["TYPE"].isin(EXCLUDE_TYPES)]
    print(f"After dropping delivery-only etc.: {len(lic)}")

    lic = lic.dropna(subset=["LONGITUDE", "LATITUDE"])
    has_coords = (lic["LONGITUDE"] != 0) & (lic["LATITUDE"] != 0)
    lic = lic.loc[has_coords]
    print(f"After dropping missing coordinates: {len(lic)}")

    lic = lic.drop_duplicates(subset="LICENSE")
    print(f"After dropping duplicate LICENSE ids: {len(lic)}")

    lic = lic.copy()  # detach from the slices above before adding columns
    # Same cell formula as analysis.build_cell_table
    lic["cell_x"] = (lic["LONGITUDE"] // CELL).astype(int)
    lic["cell_y"] = (lic["LATITUDE"] // CELL).astype(int)
    return lic
