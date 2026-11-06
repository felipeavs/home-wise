from decimal import Decimal

import pytest
from pydantic import ValidationError

from homewise.ingestion.schemas import Purchase, PurchaseItem


def make_item(**overrides) -> dict:
    data = {
        "description": "LEITE INT 1L",
        "quantity": "2",
        "unit": "UN",
        "unit_price": "4.90",
        "total_price": "9.80",
    }
    return data | overrides


def make_purchase(**overrides) -> dict:
    data = {
        "store_name": "Mercado X",
        "purchase_date": "2026-11-06",
        "items": [make_item(), make_item(description="PAO", quantity="1", unit_price="6.20",
                                         total_price="6.20")],
        "declared_total": "16.00",
    }
    return data | overrides


def test_money_is_rounded_to_two_places_half_up():
    item = PurchaseItem(**make_item(unit_price="1.005", total_price="2.675"))
    assert item.unit_price == Decimal("1.01")
    assert item.total_price == Decimal("2.68")
    assert str(item.total_price) == "2.68"


def test_money_always_has_two_decimals():
    item = PurchaseItem(**make_item(total_price="10"))
    assert str(item.total_price) == "10.00"


def test_brazilian_comma_and_currency_symbol():
    item = PurchaseItem(**make_item(unit_price="R$ 4,90"))
    assert item.unit_price == Decimal("4.90")


def test_float_input_has_no_binary_noise():
    item = PurchaseItem(**make_item(unit_price=0.1, total_price=0.3, quantity=3))
    assert item.unit_price == Decimal("0.10")
    assert item.total_price == Decimal("0.30")


def test_weighed_quantity_keeps_three_decimals():
    item = PurchaseItem(**make_item(quantity="0.345", unit="KG", unit_price="39.90",
                                    total_price="13.77"))
    assert item.quantity == Decimal("0.345")
    assert item.total_is_consistent


def test_negative_price_and_zero_quantity_are_rejected():
    with pytest.raises(ValidationError):
        PurchaseItem(**make_item(total_price="-1"))
    with pytest.raises(ValidationError):
        PurchaseItem(**make_item(quantity="0"))


def test_purchase_total_matches():
    purchase = Purchase(**make_purchase())
    assert purchase.items_total == Decimal("16.00")
    assert purchase.discrepancy == Decimal("0.00")
    assert purchase.total_matches
    assert not purchase.needs_review


def test_purchase_with_discount():
    purchase = Purchase(**make_purchase(discount="1.00", declared_total="15.00"))
    assert purchase.total_matches


def test_total_mismatch_flags_review_instead_of_raising():
    purchase = Purchase(**make_purchase(declared_total="20.00"))
    assert purchase.discrepancy == Decimal("-4.00")
    assert not purchase.total_matches
    assert purchase.needs_review


def test_inconsistent_line_flags_review():
    bad = make_item(total_price="12.00")  # 2 * 4.90 is 9.80, not 12.00
    purchase = Purchase(**make_purchase(items=[bad], declared_total="12.00"))
    assert purchase.total_matches
    assert purchase.needs_review


def test_purchase_requires_at_least_one_item():
    with pytest.raises(ValidationError):
        Purchase(**make_purchase(items=[]))


def test_json_roundtrip_keeps_two_decimals():
    purchase = Purchase(**make_purchase())
    restored = Purchase.model_validate_json(purchase.model_dump_json())
    assert restored == purchase
    assert '"declared_total":"16.00"' in purchase.model_dump_json()
