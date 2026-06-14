def calculate_cagr(start_price, end_price, years):

    if start_price <= 0 or years <= 0:
        return 0.0

    return ((end_price / start_price) ** (1 / years)) - 1


def forecast_values(investment, cagr, years):

    conservative = cagr - 0.05
    expected = cagr
    optimistic = cagr + 0.05

    return {
        "conservative":
            investment * ((1 + conservative) ** years),

        "expected":
            investment * ((1 + expected) ** years),

        "optimistic":
            investment * ((1 + optimistic) ** years)
    }