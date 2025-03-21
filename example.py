from simulator import FundSimulator
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def run_all_probabilities():
    years = 30
    starting_fund = 100_000
    inflation_mean = 2.5
    inflation_std = 3.0
    growth_mean = 7.0
    growth_std = 10.0
    growth_range = (-30, 30)
    inflation_range = (-1.5, 15)

    simulator = FundSimulator(
        years=years,
        initial_fund=starting_fund,
        growth_mean=growth_mean,
        growth_std=growth_std,
        inflation_mean=inflation_mean,
        inflation_std=inflation_std,
    )

    for withdrawal in range(2000, 5001, 100):
        for num_crashes in [2, 3, 4]:
            for crash_percent in [-5, -10, -15]:
                probability = simulator.simulate(
                    initial_withdrawal=withdrawal,
                    growth_rate_range=growth_range,
                    inflation_rate_range=inflation_range,
                    simulations=1000,
                    num_crashes=num_crashes,
                    crash_percent=crash_percent,
                )
                print(
                    f"Withdrawal: ${withdrawal}, Crashes: {num_crashes}, Crash: {crash_percent}%, "
                    f"Depletion Probability: {probability:.2%}"
                )


def plot_depletion_vs_withdrawal():
    simulator = FundSimulator(
        years=30,
        initial_fund=100_000,
        growth_mean=7.0,
        growth_std=10.0,
        inflation_mean=2.5,
        inflation_std=3.0,
    )

    withdrawals = np.arange(2000, 5001, 100)
    growth_range = (-20, 20)
    inflation_range = (0, 10)

    probabilities_with_recovery = []
    probabilities_without_recovery = []

    for withdrawal in withdrawals:
        prob_with = simulator.simulate(
            initial_withdrawal=withdrawal,
            growth_rate_range=growth_range,
            inflation_rate_range=inflation_range,
            simulations=1000,
            num_crashes=3,
            crash_percent=-15,
            enforce_recovery=True,
        )
        prob_without = simulator.simulate(
            initial_withdrawal=withdrawal,
            growth_rate_range=growth_range,
            inflation_rate_range=inflation_range,
            simulations=1000,
            num_crashes=3,
            crash_percent=-15,
            enforce_recovery=False,
        )
        probabilities_with_recovery.append(prob_with * 100)
        probabilities_without_recovery.append(prob_without * 100)

    plt.figure(figsize=(10, 6))
    plt.plot(
        withdrawals, probabilities_with_recovery, marker="o", label="With Recovery"
    )
    plt.plot(
        withdrawals,
        probabilities_without_recovery,
        marker="x",
        label="Without Recovery",
    )
    plt.axhline(y=5, color="red", linestyle="--", label="5% Threshold")
    plt.gca().yaxis.set_major_locator(MultipleLocator(10))
    plt.gca().yaxis.set_minor_locator(MultipleLocator(5))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter("%d%%"))
    plt.title("Probability of Depletion vs Withdrawal Amount\n(3 Crashes at -15%)")
    plt.xlabel("Annual Withdrawal ($)")
    plt.ylabel("Probability of Depletion (%)")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


# run_all_probabilities()
plot_depletion_vs_withdrawal()
