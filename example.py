from simulator import FundSimulator

years = 30
starting_fund = 100_000
inflation_mean = 2.5
inflation_std = 3.0
growth_mean = 7.0
growth_std = 10.0
growth_range = (-20, 20)
inflation_range = (0, 10)

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
