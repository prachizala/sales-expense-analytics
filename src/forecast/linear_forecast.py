"""Linear trendline and revenue forecasting calculation engine."""


class LinearForecastEngine:
    """Computes ordinary least squares (OLS) linear trendline and future projection."""

    @staticmethod
    def fit_and_predict(historical_values: list[float], forecast_periods: int = 3) -> tuple[float, float, list[float]]:
        """Fits y = mx + c and projects future periods. Returns (slope, intercept, forecasts)."""
        n = len(historical_values)
        if n < 2:
            return 0.0, historical_values[0] if historical_values else 0.0, []

        x = list(range(n))
        y = historical_values

        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi * xi for xi in x)

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n

        forecasts = [round(slope * (n + p) + intercept, 2) for p in range(forecast_periods)]
        return round(slope, 4), round(intercept, 2), forecasts
