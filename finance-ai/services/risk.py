import math

def calculate_risk(data):

    returns = data["Close"].pct_change()

    volatility = returns.std() * (252 ** 0.5)

    if math.isnan(volatility):
        return "Unknown"

    if volatility < 0.20:
        return "Low"

    elif volatility < 0.35:
        return "Medium"

    return "High"