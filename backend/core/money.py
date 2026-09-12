from decimal import Decimal, ROUND_HALF_UP
from typing import Union

TWO_PLACES = Decimal("0.01")
FOUR_PLACES = Decimal("0.0001")

def to_decimal(val: Union[int, float, str, Decimal]) -> Decimal:
    """Safely convert any numeric representation to Decimal without float imprecision."""
    if isinstance(val, Decimal):
        return val
    return Decimal(str(val))

def round_currency(amount: Union[int, float, str, Decimal]) -> Decimal:
    """Rounds financial amounts to 2 decimal places using standard half-up rounding."""
    d = to_decimal(amount)
    return d.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

def round_quantity(qty: Union[int, float, str, Decimal]) -> Decimal:
    """Rounds quantities to 4 decimal places where applicable."""
    d = to_decimal(qty)
    return d.quantize(FOUR_PLACES, rounding=ROUND_HALF_UP)

def format_currency(amount: Union[int, float, str, Decimal]) -> str:
    """Format PKR currency with commas and 2 decimals."""
    d = round_currency(amount)
    return f"PKR {d:,.2f}"

def format_quantity(qty: Union[int, float, str, Decimal]) -> str:
    """Format quantity without trailing redundant zeroes where clean."""
    d = to_decimal(qty)
    if d == d.to_integral():
        return f"{d:,.0f}"
    return f"{d:,.2f}"
