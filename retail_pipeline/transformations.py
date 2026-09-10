from decimal import Decimal


def calculate_order_revenue(
    quantity: int,
    unit_price: Decimal,
    discount: Decimal = Decimal("0.00"),
) -> Decimal:
    """Calculate revenue with a total discount for the order."""
    if quantity <= 0:
        raise ValueError("Quantity must be positive")

    if unit_price < 0 or discount < 0:
        raise ValueError("Price and discount cannot be negative")

    gross_revenue = quantity * unit_price

    if discount > gross_revenue:
        raise ValueError("Discount cannot exceed gross revenue")

    return gross_revenue - discount