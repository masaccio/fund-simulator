import numpy as np
from scipy.stats import truncnorm
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class FundSimulator:
    years: int
    initial_fund: float
    growth_mean: float
    growth_std: float
    inflation_mean: float
    inflation_std: float

    def _generate_skewed_distribution(self, min_val, max_val, mean, std, size):
        """Generates skewed values using a truncated normal distribution."""
        a, b = (min_val - mean) / std, (max_val - mean) / std
        return truncnorm.rvs(a, b, loc=mean, scale=std, size=size) / 100

    def _apply_crashes_and_recovery(
        self, growth_rates, simulations, num_crashes, crash_percent, enforce_recovery
    ):
        """Injects crash events and optionally enforces recovery over 3 years."""
        for sim in range(simulations):
            crash_years = np.random.choice(
                self.years, size=min(num_crashes, self.years), replace=False
            )
            for year in crash_years:
                growth_rates[sim, year] = crash_percent / 100
                if enforce_recovery:
                    recovery_years = range(year + 1, min(year + 4, self.years))
                    for ry in recovery_years:
                        growth_rates[sim, ry] = max(
                            growth_rates[sim, ry], abs(crash_percent) / 100
                        )

    def _run_simulation_loop(
        self, growth_rates, inflation_rates, initial_withdrawal, simulations
    ):
        """Simulates fund depletion over time and returns boolean array of depleted funds."""
        funds = np.full(simulations, self.initial_fund, dtype=float)
        withdrawals = np.full(simulations, initial_withdrawal, dtype=float)
        depleted = np.zeros(simulations, dtype=bool)

        for year in range(self.years):
            funds *= 1 + growth_rates[:, year]
            funds -= withdrawals
            depleted |= funds <= 0
            withdrawals *= 1 + inflation_rates[:, year]

        return depleted

    def simulate(
        self,
        initial_withdrawal: float,
        growth_rate_range: tuple,
        inflation_rate_range: tuple,
        simulations: int = 1000,
        num_crashes: int = 0,
        crash_percent: float = -20.0,
        enforce_recovery: bool = True,
    ) -> float:
        """
        Runs simulations and returns the proportion of runs where the fund was depleted.

        Parameters:
        - initial_withdrawal: First year's withdrawal amount.
        - growth_rate_range: Tuple (min_growth, max_growth) as percentages.
        - inflation_rate_range: Tuple (min_inflation, max_inflation) as percentages.
        - simulations: Number of simulation runs.
        - num_crashes: Number of market crashes per simulation.
        - crash_percent: Crash severity as percentage.
        - enforce_recovery: Whether to enforce recovery growth after crashes.

        Returns:
        - Proportion of simulations where the fund was depleted.
        """
        growth_rates = self._generate_skewed_distribution(
            growth_rate_range[0],
            growth_rate_range[1],
            mean=self.growth_mean,
            std=self.growth_std,
            size=(simulations, self.years),
        )

        inflation_rates = self._generate_skewed_distribution(
            inflation_rate_range[0],
            inflation_rate_range[1],
            mean=self.inflation_mean,
            std=self.inflation_std,
            size=(simulations, self.years),
        )

        self._apply_crashes_and_recovery(
            growth_rates, simulations, num_crashes, crash_percent, enforce_recovery
        )
        depleted = self._run_simulation_loop(
            growth_rates, inflation_rates, initial_withdrawal, simulations
        )

        return np.mean(depleted)
