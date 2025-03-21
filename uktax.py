from constants import (
    PERSONAL_ALLOWANCE,
    HIGHER_RATE_THRESHOLD,
    ALLOWANCE_REDUCTION_THRESHOLD,
    ADDITIONAL_RATE_THRESHOLD,
    BASIC_RATE,
    HIGHER_RATE,
    ADDITIONAL_RATE,
)


def uk_income_tax(income: float) -> float:
    """
    Calculate the UK income tax for a given income.

    Parameters:
    income (float): The total taxable income.

    Returns:
    float: The total income tax owed.
    """

    if income > ALLOWANCE_REDUCTION_THRESHOLD:
        reduction = (income - ALLOWANCE_REDUCTION_THRESHOLD) / 2
        personal_allowance = max(0, PERSONAL_ALLOWANCE - reduction)
    else:
        personal_allowance = PERSONAL_ALLOWANCE

    taxable_income = max(0, income - personal_allowance)
    tax = 0

    # Basic rate tax
    if taxable_income > 0:
        basic_taxable = min(taxable_income, HIGHER_RATE_THRESHOLD)
        tax += basic_taxable * BASIC_RATE

    # Higher rate tax
    if taxable_income > HIGHER_RATE_THRESHOLD:
        higher_taxable = min(
            taxable_income - HIGHER_RATE_THRESHOLD,
            ADDITIONAL_RATE_THRESHOLD - HIGHER_RATE_THRESHOLD,
        )
        tax += higher_taxable * HIGHER_RATE

    # Additional rate tax
    if taxable_income > ADDITIONAL_RATE_THRESHOLD:
        additional_taxable = taxable_income - ADDITIONAL_RATE_THRESHOLD
        tax += additional_taxable * ADDITIONAL_RATE

    return tax
