import math
import pandas as pd
import numpy as np

def calculate_risk(data):
    if not isinstance(data, dict) or "Close" not in data:
        raise ValueError("Invalid data: 'Close' key not found")
    if not isinstance(data["Close"], (list, pd.Series, np.ndarray)):
        raise ValueError("Invalid data: 'Close' value must be a list, pandas Series, or numpy array")
    if len(data["Close"]) < 2:
        raise ValueError("Invalid data: 'Close' must have at least two values to calculate risk")
    if not all(isinstance(x, (int, float)) for x in data["Close"]):
        raise ValueError("Invalid data: 'Close' values must be numeric")

    if isinstance(data["Close"], list):
        data["Close"] = pd.Series(data["Close"])
    returns = data["Close"].pct_change().dropna()

    volatility = returns.std() * (252 ** 0.5)

    if math.isnan(volatility) or volatility == 0:
        return "Unknown"

    if volatility < 0.20:
        return "Low"

    elif volatility < 0.35:
        return "Medium"

    return "High"