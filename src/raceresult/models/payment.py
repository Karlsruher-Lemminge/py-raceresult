"""Payment models for Raceresult API.

Based on go-model/pay/model.go and go-model/model.go.
"""

from __future__ import annotations

from decimal import Decimal
from enum import IntEnum

from pydantic import BaseModel, Field

from raceresult.models.types import RRDateTime, RRDecimal


class VoucherType(IntEnum):
    """Type of voucher.

    Based on go-model/model.go:523-530.
    """

    AMOUNT = 0
    PERCENT = 1
    FIRST_REG = 2
    PREV_REG = 3


class PaymentConstants:
    """Payment method constants.

    Based on go-model/pay/model.go:11-45.
    """

    # Payment methods
    PM_NO_PAYMENT = 0
    PM_CC_EUR = 2
    PM_CC_CHF = 3
    PM_UEB_D = 4
    PM_BAR = 5
    PM_SPF = 6
    PM_PPAL_EUR = 7
    PM_UEB_CH = 8
    PM_EINZ_CH = 10
    PM_UEB_SOF = 12
    PM_PPAL_GBP = 14
    PM_PPAL_USD = 15
    PM_SEPA = 16
    PM_CC_GBP = 17
    PM_SEPA_DATA = 19
    PM_OWN_EPAY = 20
    PM_OWN_PPAL = 21
    PM_OWN_WIRE_T = 22
    PM_OWN_PAYTRAIL = 25
    PM_OWN_ONE_PAY = 26
    PM_TELR = 27
    PM_OWN_ONE_PAY_DOM = 28
    PM_FATORA = 29
    PM_TWINT = 30
    PM_STRIPE_CARD = 31
    PM_OWN_PAYTRAIL_V2 = 32
    PM_TELR_SALE = 33
    PM_RED_SYS = 34
    PM_MOLLIE_BANCONTACT = 35
    PM_PAY_TABS = 36
    PM_ASIA_PAY = 37
    PM_MERCADO_PAGO = 38
    PM_CB = 99

    # Payment states
    PAY_STATE_UNDEFINED = 0
    PAY_STATE_PENDING = 1
    PAY_STATE_UNDERPAID = 2
    PAY_STATE_PAID = 3
    PAY_STATE_OVERPAID = 4
    PAY_STATE_NO_PAYOUT = 5


class Voucher(BaseModel):
    """Voucher/discount code definition.

    Based on go-model/model.go:533-547.
    """

    id: int = Field(default=0, alias="ID")
    code: str = Field(default="", alias="Code")
    type: VoucherType = Field(default=VoucherType.AMOUNT, alias="Type")
    amount: RRDecimal = Field(default=Decimal(0), alias="Amount")
    tax: RRDecimal = Field(default=Decimal(0), alias="Tax")
    contest: int = Field(default=0, alias="Contest")
    category: str = Field(default="", alias="Category")
    valid_until: RRDateTime = Field(default=None, alias="ValidUntil")
    valid_from: RRDateTime = Field(default=None, alias="ValidFrom")
    reusable: int = Field(default=0, alias="Reusable")
    use_counter: int = Field(default=0, alias="UseCounter")
    remark: str = Field(default="", alias="Remark")
    order_pos: float = Field(default=0.0, alias="OrderPos")

    model_config = {"populate_by_name": True}

    def is_valid(self) -> bool:
        """Check if voucher is currently valid based on date range and usage."""
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)

        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        if self.reusable > 0 and self.use_counter >= self.reusable:
            return False

        return True


# EntryFee is defined in event.py - re-export for backwards compatibility
from raceresult.models.event import EntryFee  # noqa: E402, F401


class MethodOption(BaseModel):
    """Payment method option offered to user.

    Based on go-model/pay/model.go:57-70.
    """

    id: int = Field(default=0, alias="ID")
    name_short: str = Field(default="", alias="NameShort")
    name: str = Field(default="", alias="Name")
    entry_fee: RRDecimal = Field(default=Decimal(0), alias="EntryFee")
    payment_fee: RRDecimal = Field(default=Decimal(0), alias="PaymentFee")
    user_fee: RRDecimal = Field(default=Decimal(0), alias="UserFee")
    kickback: RRDecimal = Field(default=Decimal(0), alias="KB")
    currency: str = Field(default="", alias="Currency")
    exchange_rate: float = Field(default=0.0, alias="ExchangeRate")
    sepa_not_before: str | None = Field(default=None, alias="SEPANotBefore")
    no_test_mode: bool = Field(default=False, alias="NoTestMode")
    token: str = Field(default="", alias="Token")

    model_config = {"populate_by_name": True}


class Method(BaseModel):
    """Payment method configuration.

    Based on go-model/pay/model.go:140-161.
    """

    id: int = Field(default=0, alias="ID")
    name_short: str = Field(default="", alias="NameShort")
    name: str = Field(default="", alias="Name")
    currency: str = Field(default="", alias="Currency")
    transaction_fee: RRDecimal = Field(default=Decimal(0), alias="TransactionFee")
    disagio: RRDecimal = Field(default=Decimal(0), alias="Disagio")
    reg_fee: RRDecimal = Field(default=Decimal(0), alias="RegFee")
    refund_fee: RRDecimal = Field(default=Decimal(0), alias="RefundFee")
    transaction_costs: RRDecimal = Field(default=Decimal(0), alias="TransactionCosts")
    disagio_costs: RRDecimal = Field(default=Decimal(0), alias="DisagioCosts")
    transfer_delay: int = Field(default=0, alias="TransferDelay")
    transfer_delay_december: int = Field(default=0, alias="TransferDelayDecember")
    activated: bool = Field(default=False, alias="Activated")
    no_payout: bool = Field(default=False, alias="NoPayout")
    bank_account_id: int = Field(default=0, alias="BankAccountID")
    capture_amount_account_id: int = Field(default=0, alias="CaptureAmountAccountID")
    no_payout_receival: bool = Field(default=False, alias="NoPayoutReceival")
    no_test_mode: bool = Field(default=False, alias="NoTestMode")
    rounding: RRDecimal = Field(default=Decimal(0), alias="Rounding")
    dont_show_fee: bool = Field(default=False, alias="DontShowFee")

    model_config = {"populate_by_name": True}


class Payment(BaseModel):
    """Payment record.

    Based on go-model/pay/model.go:91-114.
    """

    id: int = Field(default=0, alias="ID")
    cust_no: int = Field(default=0, alias="CustNo")
    event: int = Field(default=0, alias="Event")
    method: int = Field(default=0, alias="Method")
    currency: str = Field(default="", alias="Currency")
    amount_new: RRDecimal = Field(default=Decimal(0), alias="AmountNew")
    fees: RRDecimal = Field(default=Decimal(0), alias="Fees")
    user_fees: RRDecimal = Field(default=Decimal(0), alias="UserFees")
    kickback: RRDecimal = Field(default=Decimal(0), alias="Kickback")
    exchange_rate: float = Field(default=0.0, alias="ExchangeRate")
    created: RRDateTime = Field(default=None, alias="Created")
    pay_state: int = Field(default=0, alias="PayState")
    event_currency: str = Field(default="", alias="EventCurrency")
    reference: str = Field(default="", alias="Reference")
    email: str = Field(default="", alias="Email")
    bill_no: int = Field(default=0, alias="BillNo")
    retry_of: int = Field(default=0, alias="RetryOf")
    lang: str = Field(default="", alias="Lang")
    ignore_payment: bool = Field(default=False, alias="IgnorePayment")
    ignore_reason: str = Field(default="", alias="IgnoreReason")
    request_id: int = Field(default=0, alias="RequestID")
    kickback_inv_id: int = Field(default=0, alias="KickbackInvID")

    model_config = {"populate_by_name": True}
