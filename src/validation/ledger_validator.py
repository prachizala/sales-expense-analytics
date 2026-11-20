"""Financial accounting ledger double-entry debit and credit integrity validator."""


class LedgerValidator:
    """Verifies GAAP/IFRS double-entry equilibrium across transaction records."""

    @staticmethod
    def validate_trial_balance(debits: list[float], credits: list[float], tolerance: float = 0.01) -> dict:
        """Checks if sum(debits) matches sum(credits) within floating point tolerance."""
        total_debits = sum(debits)
        total_credits = sum(credits)
        variance = abs(total_debits - total_credits)
        is_balanced = variance <= tolerance

        return {
            "total_debits": round(total_debits, 2),
            "total_credits": round(total_credits, 2),
            "variance": round(variance, 4),
            "is_balanced": is_balanced,
        }
