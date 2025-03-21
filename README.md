# FundSimulator

A Python-based Monte Carlo simulation tool to evaluate whether an investment fund will be depleted over a specified time horizon, considering:
- Random growth and inflation rates (skewed distributions),
- Inflation-adjusted withdrawals,
- Randomly distributed market crash events with recovery periods.

## Requirements

- Python 3.12+
- Poetry (for `numpy` and `scipy`)

Installation:

``` bash
pipx install poetry
poetry install
poetry run example.py
```


## Usage

```python
from fund_simulator import FundSimulator

simulator = FundSimulator(
    years=30,
    initial_fund=100_000,
    growth_mean=7.0,
    growth_std=10.0,
    inflation_mean=2.5,
    inflation_std=3.0
)

probability_of_depletion = simulator.simulate(
    initial_withdrawal=4000,
    growth_rate_range=(-20, 20),
    inflation_rate_range=(0, 10),
    simulations=1000,
    num_crashes=3,
    crash_percent=-15
)

print(f"Probability of fund depletion: {probability_of_depletion:.2%}")
```

## Parameters

### FundSimulator (constructor)
| Parameter        | Type   | Description                             |
|------------------|--------|-----------------------------------------|
| `years`          | int    | Number of years to simulate             |
| `initial_fund`   | float  | Starting value of the investment fund   |
| `growth_mean`    | float  | Mean annual growth rate (in %)          |
| `growth_std`     | float  | Standard deviation of growth (in %)     |
| `inflation_mean` | float  | Mean annual inflation rate (in %)       |
| `inflation_std`  | float  | Standard deviation of inflation (in %)  |

### simulate() method
| Parameter            | Type   | Description                                                      |
|----------------------|--------|------------------------------------------------------------------|
| `initial_withdrawal` | float  | First year’s withdrawal (will increase with inflation yearly)     |
| `growth_rate_range`  | tuple  | Min/max possible growth rates (in %)                             |
| `inflation_rate_range`| tuple | Min/max possible inflation rates (in %)                          |
| `simulations`        | int    | Number of Monte Carlo simulation runs                            |
| `num_crashes`        | int    | Number of crash events per simulation                            |
| `crash_percent`      | float  | Crash severity (negative %, e.g. `-20` for -20%)                 |

## Output

The `simulate()` method returns the proportion (0–1) of simulations where the fund was depleted before the end of the simulation period.

## Attribution

This simulation approach was inspired in part by:

> O'Donoghue, Conor (2024). [Simulation-based decumulation modelling](https://sciendo.com/article/10.2478/fprj-2024-0001?tab=article). *Financial Planning Research Journal*, 2024(1). Licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## License

MIT License
