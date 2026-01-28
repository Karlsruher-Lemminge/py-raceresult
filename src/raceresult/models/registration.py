"""Registration models for Raceresult API.

Based on go-model/registration/registration.go.
"""

from __future__ import annotations

from typing import Any, Annotated, TypeVar

from pydantic import BaseModel, Field as PydanticField, BeforeValidator, model_validator

from raceresult.models.types import RRDateTime


T = TypeVar("T")


def _null_to_list(v: Any) -> list:
    """Convert None to empty list."""
    if v is None:
        return []
    return v


# Helper type for list fields that may come as null from API
NullableList = Annotated[list, BeforeValidator(_null_to_list)]


class NullSafeModel(BaseModel):
    """Base model that converts null values to empty lists for list fields."""

    @model_validator(mode="before")
    @classmethod
    def _convert_null_lists(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Get all list field names from model annotations
            for field_name, field_info in cls.model_fields.items():
                # Check if field type is a list (simplified check)
                alias = field_info.alias or field_name
                if alias in data and data[alias] is None:
                    # Check if it's expected to be a list by looking at annotation
                    annotation = cls.__annotations__.get(field_name, None)
                    if annotation and "list" in str(annotation).lower():
                        data[alias] = []
        return data

    model_config = {"populate_by_name": True}


class Style(NullSafeModel):
    """CSS style attribute.

    Based on go-model/registration/registration.go:84-87.
    """

    attribute: str = PydanticField(default="", alias="Attribute")
    value: str = PydanticField(default="", alias="Value")

    model_config = {"populate_by_name": True}


class Value(NullSafeModel):
    """Dropdown value option.

    Based on go-model/registration/registration.go:89-97.
    """

    value: Any = PydanticField(default=None, alias="Value")
    label: str = PydanticField(default="", alias="Label")
    enabled: bool = PydanticField(default=True, alias="Enabled")
    enabled_from: RRDateTime = PydanticField(default=None, alias="EnabledFrom")
    enabled_to: RRDateTime = PydanticField(default=None, alias="EnabledTo")
    max_capacity: int = PydanticField(default=0, alias="MaxCapacity")
    show_if: str = PydanticField(default="", alias="ShowIf")

    model_config = {"populate_by_name": True}


class ValidationRule(NullSafeModel):
    """Validation rule for form fields.

    Based on go-model/registration/registration.go:129-132.
    """

    rule: str = PydanticField(default="", alias="Rule")
    msg: str = PydanticField(default="", alias="Msg")

    model_config = {"populate_by_name": True}


class FormField(NullSafeModel):
    """Form field definition.

    Based on go-model/registration/registration.go:68-82.
    """

    name: str = PydanticField(default="", alias="Name")
    control_type: str = PydanticField(default="", alias="ControlType")
    mandatory: int = PydanticField(default=0, alias="Mandatory")
    default_value: str = PydanticField(default="", alias="DefaultValue")
    default_value_type: int = PydanticField(default=0, alias="DefaultValueType")
    placeholder: str = PydanticField(default="", alias="Placeholder")
    unique: str = PydanticField(default="", alias="Unique")
    special: str = PydanticField(default="", alias="Special")
    special_details: str = PydanticField(default="", alias="SpecialDetails")
    force_update: bool = PydanticField(default=False, alias="ForceUpdate")
    values: list[Value] = PydanticField(default_factory=list, alias="Values")
    additional_options: list[str] = PydanticField(default_factory=list, alias="AdditionalOptions")
    flags: list[str] = PydanticField(default_factory=list, alias="Flags")

    model_config = {"populate_by_name": True}


class Element(NullSafeModel):
    """Registration form element.

    Based on go-model/registration/registration.go:48-66.
    """

    type: str = PydanticField(default="", alias="Type")
    label: str = PydanticField(default="", alias="Label")
    enabled: bool = PydanticField(default=True, alias="Enabled")
    enabled_from: RRDateTime = PydanticField(default=None, alias="EnabledFrom")
    enabled_to: RRDateTime = PydanticField(default=None, alias="EnabledTo")
    field: FormField | None = PydanticField(default=None, alias="Field")
    show_if: str = PydanticField(default="", alias="ShowIf")
    show_if_mode: int = PydanticField(default=0, alias="ShowIfMode")
    show_if_curr: str = PydanticField(default="", alias="ShowIfCurr")
    show_if_curr_mode: int = PydanticField(default=0, alias="ShowIfCurrMode")
    show_if_initial: bool = PydanticField(default=False, alias="ShowIfInitial")
    styles: list[Style] = PydanticField(default_factory=list, alias="Styles")
    class_name: str = PydanticField(default="", alias="ClassName")
    id: int = PydanticField(default=0, alias="ID")
    common: int = PydanticField(default=0, alias="Common")
    validation_rules: list[ValidationRule] = PydanticField(default_factory=list, alias="ValidationRules")
    children: list[Element] = PydanticField(default_factory=list, alias="Children")

    model_config = {"populate_by_name": True}


class Step(NullSafeModel):
    """Registration form step.

    Based on go-model/registration/registration.go:38-46.
    """

    id: int = PydanticField(default=0, alias="ID")
    title: str = PydanticField(default="", alias="Title")
    enabled: bool = PydanticField(default=True, alias="Enabled")
    enabled_from: RRDateTime = PydanticField(default=None, alias="EnabledFrom")
    enabled_to: RRDateTime = PydanticField(default=None, alias="EnabledTo")
    elements: list[Element] = PydanticField(default_factory=list, alias="Elements")
    button_text: str = PydanticField(default="", alias="ButtonText")

    model_config = {"populate_by_name": True}


class AdditionalValue(NullSafeModel):
    """Additional value computed during registration.

    Based on go-model/registration/registration.go:99-105.
    """

    field_name: str = PydanticField(default="", alias="FieldName")
    source: str = PydanticField(default="", alias="Source")
    value: str = PydanticField(default="", alias="Value")
    filter: str = PydanticField(default="", alias="Filter")
    filter_initial: str = PydanticField(default="", alias="FilterInitial")

    model_config = {"populate_by_name": True}


class Confirmation(NullSafeModel):
    """Confirmation page settings.

    Based on go-model/registration/registration.go:107-110.
    """

    title: str = PydanticField(default="", alias="Title")
    expression: str = PydanticField(default="", alias="Expression")

    model_config = {"populate_by_name": True}


class AfterSave(NullSafeModel):
    """Action to perform after saving registration.

    Based on go-model/registration/registration.go:112-118.
    """

    type: str = PydanticField(default="", alias="Type")
    value: str = PydanticField(default="", alias="Value")
    destination: str = PydanticField(default="", alias="Destination")
    filter: str = PydanticField(default="", alias="Filter")
    flags: list[str] = PydanticField(default_factory=list, alias="Flags")

    model_config = {"populate_by_name": True}


class PaymentMethod(NullSafeModel):
    """Payment method for registration.

    Based on go-model/registration/registration.go:120-127.
    """

    id: int = PydanticField(default=0, alias="ID")
    label: str = PydanticField(default="", alias="Label")
    enabled: bool = PydanticField(default=True, alias="Enabled")
    enabled_from: RRDateTime = PydanticField(default=None, alias="EnabledFrom")
    enabled_to: RRDateTime = PydanticField(default=None, alias="EnabledTo")
    filter: str = PydanticField(default="", alias="Filter")

    model_config = {"populate_by_name": True}


class ErrorMessages(NullSafeModel):
    """Custom error messages for registration.

    Based on go-model/registration/registration.go:134-137.
    """

    befor_reg_start: str = PydanticField(default="", alias="BeforRegStart")
    after_reg_end: str = PydanticField(default="", alias="AfterRegEnd")

    model_config = {"populate_by_name": True}


class Registration(NullSafeModel):
    """Registration form definition.

    Based on go-model/registration/registration.go:7-36.
    """

    name: str = PydanticField(default="", alias="Name")
    key: str = PydanticField(default="", alias="Key")
    change_key_salt: str = PydanticField(default="", alias="ChangeKeySalt")
    title: str = PydanticField(default="", alias="Title")
    enabled: bool = PydanticField(default=False, alias="Enabled")
    enabled_from: RRDateTime = PydanticField(default=None, alias="EnabledFrom")
    enabled_to: RRDateTime = PydanticField(default=None, alias="EnabledTo")
    test_mode_key: str = PydanticField(default="", alias="TestModeKey")
    type: str = PydanticField(default="", alias="Type")
    group_min: int = PydanticField(default=0, alias="GroupMin")
    group_max: int = PydanticField(default=0, alias="GroupMax")
    group_default: int = PydanticField(default=0, alias="GroupDefault")
    group_inc: int = PydanticField(default=0, alias="GroupInc")
    contest: int = PydanticField(default=0, alias="Contest")
    limit: int = PydanticField(default=0, alias="Limit")
    change_identity_field: str = PydanticField(default="", alias="ChangeIdentityField")
    change_identity_filter: str = PydanticField(default="", alias="ChangeIdentityFilter")
    steps: list[Step] = PydanticField(default_factory=list, alias="Steps")
    additional_values: list[AdditionalValue] = PydanticField(default_factory=list, alias="AdditionalValues")
    check_sex: bool = PydanticField(default=False, alias="CheckSex")
    check_duplicate: bool = PydanticField(default=False, alias="CheckDuplicate")
    dont_propose_gender: bool = PydanticField(default=False, alias="DontProposeGender")
    online_payment: bool = PydanticField(default=False, alias="OnlinePayment")
    online_payment_button_text: str = PydanticField(default="", alias="OnlinePaymentButtonText")
    payment_methods: list[PaymentMethod] = PydanticField(default_factory=list, alias="PaymentMethods")
    online_refund: bool = PydanticField(default=False, alias="OnlineRefund")
    refund_methods: list[PaymentMethod] = PydanticField(default_factory=list, alias="RefundMethods")
    confirmation: Confirmation = PydanticField(default_factory=Confirmation, alias="Confirmation")
    after_save: list[AfterSave] = PydanticField(default_factory=list, alias="AfterSave")
    css: str = PydanticField(default="", alias="CSS")
    error_messages: ErrorMessages = PydanticField(default_factory=ErrorMessages, alias="ErrorMessages")

    model_config = {"populate_by_name": True}

    def is_active(self) -> bool:
        """Check if registration is currently active based on enabled and date range."""
        if not self.enabled:
            return False

        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)

        if self.enabled_from and now < self.enabled_from:
            return False
        if self.enabled_to and now > self.enabled_to:
            return False

        return True
