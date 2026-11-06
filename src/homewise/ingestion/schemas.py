"""Schemas for purchase data extracted from receipts.

This is the contract between ingestion, database and UI. All money values are
`Decimal` rounded to 2 decimal places (ROUND_HALF_UP). See ADR 0003.
"""

from __future__ import annotations

from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated, Any

from pydantic import AfterValidator, BaseModel, BeforeValidator, Field

CENT = Decimal("0.01")
QUANTITY_STEP = Decimal("0.001")  # weighed items (kg) come with 3 decimals
TOLERANCE = CENT  # receipts round each line, so allow one cent of difference


def _to_decimal(value: Any) -> Any:
    """Convert input to Decimal without going through binary float noise."""
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, str):
        text = value.strip().replace("R$", "").strip()
        if "," in text and "." not in text:  # Brazilian format: "12,90"
            text = text.replace(",", ".")
        return Decimal(text)
    return value


def _round_money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _round_quantity(value: Decimal) -> Decimal:
    return value.quantize(QUANTITY_STEP, rounding=ROUND_HALF_UP)


Money = Annotated[Decimal, BeforeValidator(_to_decimal), AfterValidator(_round_money)]
Quantity = Annotated[Decimal, BeforeValidator(_to_decimal), AfterValidator(_round_quantity)]


class PurchaseItem(BaseModel):
    """One line of a receipt, exactly as extracted."""

    description: str = Field(min_length=1, description="Product text as printed on the receipt")
    quantity: Quantity = Field(gt=0)
    unit: str = Field(default="UN", description="UN, KG, L, ...")
    unit_price: Money = Field(ge=0)
    total_price: Money = Field(ge=0)

    @property
    def total_is_consistent(self) -> bool:
        """True if quantity * unit_price matches total_price within one cent."""
        expected = _round_money(self.quantity * self.unit_price)
        return abs(expected - self.total_price) <= TOLERANCE


class Purchase(BaseModel):
    """A whole receipt: store, date, items and the total declared on the paper."""

    store_name: str = Field(min_length=1)
    purchase_date: date
    items: list[PurchaseItem] = Field(min_length=1)
    discount: Money = Field(default=Decimal("0.00"), ge=0)
    declared_total: Money = Field(ge=0, description="Total printed on the receipt")
    payment_method: str | None = None

    @property
    def items_total(self) -> Decimal:
        """Sum of the item totals (computed by code, never by the LLM)."""
        return _round_money(sum((item.total_price for item in self.items), Decimal("0")))

    @property
    def discrepancy(self) -> Decimal:
        """Items total minus discount minus declared total. Zero means it matches."""
        return _round_money(self.items_total - self.discount - self.declared_total)

    @property
    def total_matches(self) -> bool:
        return abs(self.discrepancy) <= TOLERANCE

    @property
    def needs_review(self) -> bool:
        """Extraction doubtful: total mismatch or an inconsistent line."""
        return not self.total_matches or not all(i.total_is_consistent for i in self.items)
