import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def run_model(cells: pd.DataFrame) -> None:
    X = cells[["other_requests"]]
    y = cells["sancompcount"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    baseline = DummyRegressor(strategy="mean")
    baseline.fit(X_train, y_train)
    baseline_predictions = baseline.predict(X_test)

    print("Baseline MAE:", mean_absolute_error(y_test, baseline_predictions))
    print("Target mean:", y.mean(), "std:", y.std())
    print("MAE:", mean_absolute_error(y_test, predictions))
    print("R^2:", r2_score(y_test, predictions))
    print("Coefficient:", model.coef_, "Intercept:", model.intercept_)
