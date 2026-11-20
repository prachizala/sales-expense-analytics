"""Operating cash burn rate and treasury runway duration calculator."""


class BurnRateCalculator:
    """Evaluates corporate monthly cash burn and runway survival ceiling."""

    @staticmethod
    def compute_net_burn(operating_expenses: float, gross_revenues: float) -> float:
        """Returns net monthly cash burn (positive indicates cash deficit)."""
        return max(0.0, round(operating_expenses - gross_revenues, 2))

    @staticmethod
    def compute_runway_months(total_cash_reserves: float, net_monthly_burn: float) -> float:
        """Computes runway in months until zero cash balance."""
        if net_monthly_burn <= 0:
            return float('inf')
        return round(total_cash_reserves / net_monthly_burn, 1)
