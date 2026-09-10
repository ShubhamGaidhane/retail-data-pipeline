import unittest
from decimal import Decimal

from retail_pipeline.transformations import calculate_order_revenue


class TestOrderRevenue(unittest.TestCase):
    def test_discount_applies_once_per_order(self):
        result = calculate_order_revenue(
            2, Decimal("100.00"), Decimal("20.00")
        )
        self.assertEqual(result, Decimal("180.00"))

    def test_discount_defaults_to_zero(self):
        result = calculate_order_revenue(3, Decimal("0.10"))
        self.assertEqual(result, Decimal("0.30"))

    def test_full_discount_produces_zero_revenue(self):
        result = calculate_order_revenue(
            2, Decimal("100.00"), Decimal("200.00")
        )
        self.assertEqual(result, Decimal("0.00"))

    def test_zero_price_is_allowed(self):
        result = calculate_order_revenue(1, Decimal("0.00"))
        self.assertEqual(result, Decimal("0.00"))

    def test_invalid_orders_are_rejected(self):
        cases = [
            (0, Decimal("100.00"), Decimal("0.00")),
            (-1, Decimal("100.00"), Decimal("0.00")),
            (1, Decimal("-1.00"), Decimal("0.00")),
            (1, Decimal("100.00"), Decimal("-1.00")),
            (1, Decimal("100.00"), Decimal("101.00")),
        ]

        for quantity, price, discount in cases:
            with self.subTest(
                quantity=quantity, price=price, discount=discount
            ):
                with self.assertRaises(ValueError):
                    calculate_order_revenue(quantity, price, discount)