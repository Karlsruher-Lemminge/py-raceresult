#!/usr/bin/env python3
"""Output all registration forms of an event with full details."""

import argparse
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from raceresult import RaceResultAPI


def print_section(title: str, level: int = 1):
    """Print a section header."""
    if level == 1:
        print(f"\n{'=' * 70}")
        print(f" {title}")
        print(f"{'=' * 70}")
    elif level == 2:
        print(f"\n  {'-' * 50}")
        print(f"  {title}")
        print(f"  {'-' * 50}")
    else:
        print(f"\n    {title}")
        print(f"    {'-' * len(title)}")


def print_field(name: str, value, indent: int = 2):
    """Print a field with indentation."""
    prefix = "  " * indent
    if value is not None and value != "" and value != [] and value != {}:
        print(f"{prefix}{name}: {value}")


def print_element(elem, indent: int = 4):
    """Recursively print an element and its children."""
    prefix = "  " * indent

    # Element header
    elem_type = elem.type or "unknown"
    elem_label = f" - {elem.label}" if elem.label else ""
    print(f"{prefix}[{elem_type}]{elem_label}")

    # Element details
    if elem.id:
        print(f"{prefix}  ID: {elem.id}")
    if not elem.enabled:
        print(f"{prefix}  Enabled: False")
    if elem.enabled_from:
        print(f"{prefix}  Enabled From: {elem.enabled_from}")
    if elem.enabled_to:
        print(f"{prefix}  Enabled To: {elem.enabled_to}")
    if elem.show_if:
        print(f"{prefix}  ShowIf: {elem.show_if}")
    if elem.show_if_curr:
        print(f"{prefix}  ShowIfCurr: {elem.show_if_curr}")
    if elem.class_name:
        print(f"{prefix}  ClassName: {elem.class_name}")
    if elem.common:
        print(f"{prefix}  Common: {elem.common}")

    # Styles
    if elem.styles:
        styles_str = ", ".join(f"{s.attribute}={s.value}" for s in elem.styles)
        print(f"{prefix}  Styles: {styles_str}")

    # Field (singular)
    if elem.field:
        f = elem.field
        print(f"{prefix}  Field: {f.name}")
        if f.control_type:
            print(f"{prefix}    ControlType: {f.control_type}")
        if f.mandatory:
            print(f"{prefix}    Mandatory: {f.mandatory}")
        if f.default_value:
            print(f"{prefix}    Default: {f.default_value}")
        if f.placeholder:
            print(f"{prefix}    Placeholder: {f.placeholder}")
        if f.unique:
            print(f"{prefix}    Unique: {f.unique}")
        if f.special:
            print(f"{prefix}    Special: {f.special}")
        if f.special_details:
            print(f"{prefix}    SpecialDetails: {f.special_details}")
        if f.force_update:
            print(f"{prefix}    ForceUpdate: True")
        if f.flags:
            print(f"{prefix}    Flags: {f.flags}")
        if f.additional_options:
            print(f"{prefix}    AdditionalOptions: {f.additional_options}")

        # Field values (dropdown options)
        if f.values:
            print(f"{prefix}    Values ({len(f.values)}):")
            for v in f.values[:10]:  # Limit to first 10
                v_str = f"{prefix}      - {v.value}"
                if v.label and v.label != str(v.value):
                    v_str += f" ({v.label})"
                if not v.enabled:
                    v_str += " [disabled]"
                if v.max_capacity:
                    v_str += f" [max: {v.max_capacity}]"
                if v.show_if:
                    v_str += f" [showIf: {v.show_if}]"
                print(v_str)
            if len(f.values) > 10:
                print(f"{prefix}      ... and {len(f.values) - 10} more")

    # Validation rules
    if elem.validation_rules:
        print(f"{prefix}  ValidationRules:")
        for vr in elem.validation_rules:
            print(f"{prefix}    - Rule: {vr.rule}")
            if vr.msg:
                print(f"{prefix}      Msg: {vr.msg}")

    # Children (recursive)
    if elem.children:
        print(f"{prefix}  Children ({len(elem.children)}):")
        for child in elem.children:
            print_element(child, indent + 2)


async def main():
    parser = argparse.ArgumentParser(
        description="Output all registration forms of an event"
    )
    parser.add_argument("event_id", help="Event ID")
    parser.add_argument("--api-key", help="API key (or set API_KEY env var)")
    parser.add_argument("--name", help="Only show registration with this name")
    parser.add_argument("--compact", "-c", action="store_true", help="Compact output (less details)")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("API_KEY", "").strip('"')
    event_id = args.event_id

    if not api_key:
        print("Error: API key required. Set API_KEY env var or use --api-key")
        return

    async with RaceResultAPI() as api:
        await api.login(api_key=api_key)
        event = api.event(event_id)

        # Get event name
        settings = await event.settings.get("EventName")
        event_name = settings.get("EventName", event_id)

        print(f"\nRegistration Forms for: {event_name}")
        print(f"Event ID: {event_id}")

        # Get registration names
        reg_names = await event.registrations.names()

        if args.name:
            if args.name in reg_names:
                reg_names = [args.name]
            else:
                print(f"\nError: Registration '{args.name}' not found.")
                print(f"Available: {reg_names}")
                return

        print(f"Found {len(reg_names)} registration form(s): {reg_names}")

        for reg_name in reg_names:
            reg = await event.registrations.get(reg_name)

            print_section(f"REGISTRATION: {reg.name}")

            # Basic settings
            print_section("Basic Settings", 2)
            print_field("Name", reg.name)
            print_field("Key", reg.key)
            print_field("Title", reg.title)
            print_field("Enabled", reg.enabled)
            print_field("Enabled From", reg.enabled_from)
            print_field("Enabled To", reg.enabled_to)
            print_field("Type", reg.type)
            print_field("Contest", reg.contest)
            print_field("Limit", reg.limit)
            print_field("Test Mode Key", reg.test_mode_key)

            # Group settings
            if reg.group_min or reg.group_max:
                print_section("Group Settings", 2)
                print_field("Group Min", reg.group_min)
                print_field("Group Max", reg.group_max)
                print_field("Group Default", reg.group_default)
                print_field("Group Increment", reg.group_inc)

            # Change settings
            if reg.change_identity_field or reg.change_identity_filter:
                print_section("Change Settings", 2)
                print_field("Change Key Salt", reg.change_key_salt)
                print_field("Change Identity Field", reg.change_identity_field)
                print_field("Change Identity Filter", reg.change_identity_filter)

            # Validation options
            print_section("Validation Options", 2)
            print_field("Check Sex", reg.check_sex)
            print_field("Check Duplicate", reg.check_duplicate)
            print_field("Don't Propose Gender", reg.dont_propose_gender)

            # CSS
            if reg.css:
                print_section("Custom CSS", 2)
                css_preview = reg.css[:200] + "..." if len(reg.css) > 200 else reg.css
                print(f"    {css_preview}")

            # Steps
            if reg.steps:
                print_section(f"Steps ({len(reg.steps)})", 2)
                for i, step in enumerate(reg.steps, 1):
                    print_section(f"Step {i}: {step.title or '(untitled)'}", 3)
                    print_field("ID", step.id, 4)
                    print_field("Title", step.title, 4)
                    print_field("Enabled", step.enabled if not step.enabled else None, 4)
                    print_field("Enabled From", step.enabled_from, 4)
                    print_field("Enabled To", step.enabled_to, 4)
                    print_field("Button Text", step.button_text, 4)

                    if step.elements:
                        print(f"        Elements ({len(step.elements)}):")
                        if args.compact:
                            for elem in step.elements:
                                elem_type = elem.type or "unknown"
                                elem_label = elem.label or ""
                                field_name = elem.field.name if elem.field else ""
                                print(f"          - [{elem_type}] {elem_label} {field_name}".strip())
                        else:
                            for elem in step.elements:
                                print_element(elem, indent=5)

            # Additional Values
            if reg.additional_values:
                print_section(f"Additional Values ({len(reg.additional_values)})", 2)
                for av in reg.additional_values:
                    print(f"    - {av.field_name}")
                    print_field("Source", av.source, 3)
                    print_field("Value", av.value, 3)
                    print_field("Filter", av.filter, 3)
                    print_field("Filter Initial", av.filter_initial, 3)

            # Payment settings
            print_section("Payment Settings", 2)
            print_field("Online Payment", reg.online_payment)
            print_field("Online Payment Button", reg.online_payment_button_text)
            print_field("Online Refund", reg.online_refund)

            # Payment Methods
            if reg.payment_methods:
                print_section(f"Payment Methods ({len(reg.payment_methods)})", 2)
                for pm in reg.payment_methods:
                    pm_info = f"    - ID {pm.id}: {pm.label}"
                    if not pm.enabled:
                        pm_info += " [disabled]"
                    print(pm_info)
                    if pm.filter:
                        print(f"        Filter: {pm.filter}")
                    if pm.enabled_from:
                        print(f"        Enabled From: {pm.enabled_from}")
                    if pm.enabled_to:
                        print(f"        Enabled To: {pm.enabled_to}")

            # Refund Methods
            if reg.refund_methods:
                print_section(f"Refund Methods ({len(reg.refund_methods)})", 2)
                for rm in reg.refund_methods:
                    rm_info = f"    - ID {rm.id}: {rm.label}"
                    if not rm.enabled:
                        rm_info += " [disabled]"
                    print(rm_info)

            # Confirmation
            if reg.confirmation and (reg.confirmation.title or reg.confirmation.expression):
                print_section("Confirmation Page", 2)
                print_field("Title", reg.confirmation.title, 3)
                print_field("Expression", reg.confirmation.expression, 3)

            # After Save
            if reg.after_save:
                print_section(f"After Save Actions ({len(reg.after_save)})", 2)
                for action in reg.after_save:
                    print(f"    - Type: {action.type}")
                    print_field("Value", action.value, 3)
                    print_field("Destination", action.destination, 3)
                    print_field("Filter", action.filter, 3)
                    print_field("Flags", action.flags, 3)

            # Error Messages
            if reg.error_messages:
                em = reg.error_messages
                if em.befor_reg_start or em.after_reg_end:
                    print_section("Custom Error Messages", 2)
                    print_field("Before Reg Start", em.befor_reg_start, 3)
                    print_field("After Reg End", em.after_reg_end, 3)

        print(f"\n{'=' * 70}")
        print(f" COMPLETE - {len(reg_names)} registration form(s) displayed")
        print(f"{'=' * 70}\n")


if __name__ == "__main__":
    asyncio.run(main())
