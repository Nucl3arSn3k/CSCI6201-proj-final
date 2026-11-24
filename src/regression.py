import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import  train_test_split

TARGET = "sancompcount"
SEED = 42
BASE_FEATURES = ["other_requests"]
BAR_FEATURES = ["bars_total", "bars_total_nbr"]  # bars in the cell, bars in the 8 surrounding cells


def run_model(cells: pd.DataFrame, features: list[str] = BASE_FEATURES, label: str = "Model") -> None:
    """Linear regression on `features`: 5-fold CV on the training data, then one test-set score."""
    X = cells.loc[:, features]
    y = cells.loc[:, TARGET]

    # Same 80/20 split every time (random_state=42), so models are comparable
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED
    )



    # Fit on all training data, score once on the held-out test data
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    baseline = DummyRegressor(strategy="mean")
    baseline.fit(X_train, y_train)
    baseline_predictions = baseline.predict(X_test)

    print(f"\n--- {label}: features = {features} ---")
    print("Test baseline MAE:", mean_absolute_error(y_test, baseline_predictions))
    print("Test MAE:", mean_absolute_error(y_test, predictions))
    print("Test R^2:", r2_score(y_test, predictions))
    print("Intercept:", model.intercept_)
    for name, coef in zip(features, model.coef_):
        print(f"Coefficient {name}: {coef:.4f}")
