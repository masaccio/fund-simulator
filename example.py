from simulator import FundSimulator
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


# The mean of the S&P 500, Dow Jones, NASDAQ and FTSE 100 from 1970-2024
GROWTH_MEAN = 9.74

# The standard deviation of the S&P 500, Dow Jones, NASDAQ and FTSE 100 from 1970-2024
GROWTH_STD_DEV = 21.0

# Mean UK inflation from 1980-2024
INFLATION_MEAN = 3.75

# Standard deviation of UK inflation from 1980-2024
INFLATION_STD_DEV = 3.25

# UK Inflation from 1980-2024 10th and 90th percentile
INFLATION_RANGE = (0, 7.74)

# S&P 500, Dow Jones, NASDAQ and FTSE 100 from 1970-2024 10th and 90th percentile
GROWTH_RANGE = (-24.4, 35.0)

# 100,000 simulations is what Tamimi et al used in their paper and generates a smooth enough
# probability curve, though 1000 is sufficient for a quick simulation
NUM_SIMULATIONS = 1000

# Expected duration of returement
NUM_YEARS = 30

# Initial fund value is arbitrary since we are only interested in the probability of depletion
INITIAL_FUND_VALUE = 100_000

# Withdrawal range from 2% to 5% of the initial fund value in steps of 100
WITHDRAWAL_RANGE = (
    int(INITIAL_FUND_VALUE * 0.02),
    int(INITIAL_FUND_VALUE * 0.05 + 1),
    100,
)

# What crashes to simulate. We chose 2, 3 and 4 crashes at -5%, -10% and -15% respectively
CRASH_COUNTS = [2, 3, 4]
CRASH_PERCENTS = [-5, -10, -15]

simulator = FundSimulator(
    years=NUM_YEARS,
    initial_fund=INITIAL_FUND_VALUE,
    growth_mean=GROWTH_MEAN,
    growth_std=GROWTH_STD_DEV,
    inflation_mean=INFLATION_MEAN,
    inflation_std=INFLATION_STD_DEV,
)

withdrawals = np.arange(*WITHDRAWAL_RANGE)

plt.figure(figsize=(10, 6))

probabilities = {}
for num_crashes in CRASH_COUNTS:
    probabilities[num_crashes] = {}
    for crash_percent in CRASH_PERCENTS:
        probabilities[num_crashes][crash_percent] = []
        for withdrawal in withdrawals:
            probability = simulator.simulate(
                initial_withdrawal=withdrawal,
                growth_rate_range=GROWTH_RANGE,
                inflation_rate_range=INFLATION_RANGE,
                simulations=NUM_SIMULATIONS,
                num_crashes=num_crashes,
                crash_percent=crash_percent,
                enforce_recovery=True,
            )
            probabilities[num_crashes][crash_percent].append(probability * 100)

        plt.plot(
            withdrawals,
            probabilities[num_crashes][crash_percent],
            label=f"{num_crashes} Crashes at {crash_percent}%",
        )

plt.axhline(y=5, color="red", linestyle="--", label="5% Threshold")
plt.gca().yaxis.set_major_locator(MultipleLocator(10))
plt.gca().yaxis.set_minor_locator(MultipleLocator(5))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%d%%"))
plt.title("Probability of Depletion vs Withdrawal Amount")
plt.xlabel("Annual Withdrawal ($)")
plt.ylabel("Probability of Depletion (%)")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.show()
