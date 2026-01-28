#!/usr/bin/env python3
"""Live test against a Raceresult event - tests all API endpoints."""

import argparse
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from raceresult import RaceResultAPI
from raceresult.endpoints.participants import Identifier


async def main():
    parser = argparse.ArgumentParser(description="Live test against a Raceresult event")
    parser.add_argument("event_id", help="Event ID to test against")
    parser.add_argument("--api-key", help="API key (or set API_KEY env var)")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("API_KEY", "").strip('"')
    event_id = args.event_id

    if not api_key:
        print("Error: API key required. Set API_KEY env var or use --api-key")
        return

    print(f"Testing event: {event_id}")
    print("=" * 60)

    async with RaceResultAPI() as api:
        # Login
        print("\n1. LOGIN")
        try:
            await api.login(api_key=api_key)
            print(f"   ✓ Logged in, session_id: {api.session_id[:20]}...")
        except Exception as e:
            print(f"   ✗ Login failed: {e}")
            return

        # User info
        print("\n2. USER INFO")
        try:
            user_info = await api.user_info()
            print(f"   CustNo: {user_info.cust_no}")
            print(f"   UserName: {user_info.user_name}")
        except Exception as e:
            print(f"   ✗ User info failed: {e}")

        # Event list
        print("\n3. EVENT LIST")
        try:
            events = await api.event_list(year=2024)
            print(f"   Found {len(events)} events in 2024")
            for ev in events[:3]:
                print(f"   - {ev.id}: {ev.event_name}")
        except Exception as e:
            print(f"   ✗ Event list failed: {e}")

        event = api.event(event_id)

        # Settings
        print("\n4. SETTINGS")
        try:
            settings = await event.settings.get(
                "EventName", "EventDate", "EventDate2", "BillingMode"
            )
            for name, value in settings.items():
                print(f"   {name}: {value}")
        except Exception as e:
            print(f"   ✗ Settings failed: {e}")

        # Contests
        print("\n5. CONTESTS")
        try:
            contests = await event.contests.get()
            print(f"   Found {len(contests)} contests")
            for c in contests[:5]:
                print(f"   - ID {c.id}: {c.name} ({c.name_short})")
        except Exception as e:
            print(f"   ✗ Contests failed: {e}")

        # Age Groups
        print("\n6. AGE GROUPS")
        try:
            agegroups = await event.agegroups.get()
            print(f"   Found {len(agegroups)} age groups")
            for ag in agegroups[:5]:
                print(f"   - ID {ag.id}: {ag.name} (Contest: {ag.contest}, Set: {ag.ag_set})")
        except Exception as e:
            print(f"   ✗ Age groups failed: {e}")

        # Bib Ranges
        print("\n7. BIB RANGES")
        try:
            bibranges = await event.bibranges.get()
            print(f"   Found {len(bibranges)} bib ranges")
            for br in bibranges[:5]:
                print(f"   - ID {br.id}: {br.bib_start}-{br.bib_end} (Contest: {br.contest})")
        except Exception as e:
            print(f"   ✗ Bib ranges failed: {e}")

        # Custom Fields
        print("\n8. CUSTOM FIELDS")
        try:
            customfields = await event.customfields.get()
            print(f"   Found {len(customfields)} custom fields")
            for cf in customfields[:5]:
                print(f"   - ID {cf.id}: {cf.name} (Type: {cf.field_type.name})")
        except Exception as e:
            print(f"   ✗ Custom fields failed: {e}")

        # Entry Fees
        print("\n9. ENTRY FEES")
        try:
            entryfees = await event.entryfees.get()
            print(f"   Found {len(entryfees)} entry fees")
            for ef in entryfees[:5]:
                print(f"   - ID {ef.id}: {ef.name} = {ef.fee} (Contest: {ef.contest})")
        except Exception as e:
            print(f"   ✗ Entry fees failed: {e}")

        # Results
        print("\n10. RESULTS")
        try:
            results = await event.results.get()
            print(f"   Found {len(results)} results")
            for r in results[:5]:
                formula_info = f" (Formula: {r.formula[:30]}...)" if r.formula else ""
                print(f"   - ID {r.id}: {r.name}{formula_info}")
        except Exception as e:
            print(f"   ✗ Results failed: {e}")

        # Timing Points
        print("\n11. TIMING POINTS")
        try:
            timingpoints = await event.timingpoints.get()
            print(f"   Found {len(timingpoints)} timing points")
            for tp in timingpoints[:5]:
                print(f"   - {tp.name} (Type: {tp.type}, OrderPos: {tp.order_pos})")
        except Exception as e:
            print(f"   ✗ Timing points failed: {e}")

        # Timing Point Rules
        print("\n12. TIMING POINT RULES")
        try:
            rules = await event.timingpointrules.get()
            print(f"   Found {len(rules)} timing point rules")
            for r in rules[:5]:
                print(f"   - ID {r.id}: {r.timing_point} (Decoder: {r.decoder_id})")
        except Exception as e:
            print(f"   ✗ Timing point rules failed: {e}")

        # Lists
        print("\n13. LISTS")
        try:
            list_names = await event.lists.names()
            print(f"   Found {len(list_names)} lists")
            for name in list_names[:5]:
                print(f"   - {name}")
        except Exception as e:
            print(f"   ✗ Lists failed: {e}")

        # Exporters
        print("\n14. EXPORTERS")
        try:
            exporters = await event.exporters.get()
            print(f"   Found {len(exporters)} exporters")
            for ex in exporters[:5]:
                print(f"   - ID {ex.id}: {ex.name} ({ex.destination_type})")
        except Exception as e:
            print(f"   ✗ Exporters failed: {e}")

        # Vouchers
        print("\n15. VOUCHERS")
        try:
            vouchers = await event.vouchers.get()
            print(f"   Found {len(vouchers)} vouchers")
            for v in vouchers[:5]:
                print(f"   - {v.code}: {v.amount} ({v.type.name})")
        except Exception as e:
            print(f"   ✗ Vouchers failed: {e}")

        # Registrations
        print("\n16. REGISTRATIONS")
        try:
            reg_names = await event.registrations.names()
            print(f"   Found {len(reg_names)} registration forms: {reg_names}")
            if reg_names:
                reg = await event.registrations.get(reg_names[0])
                print(f"   First reg '{reg.name}':")
                print(f"     - Enabled: {reg.enabled}")
                print(f"     - Steps: {len(reg.steps)}")
                print(f"     - Payment methods: {len(reg.payment_methods)}")
        except Exception as e:
            print(f"   ✗ Registrations failed: {e}")

        # Email templates
        print("\n17. EMAIL TEMPLATES")
        try:
            email_names = await event.email_templates.names()
            print(f"   Found {len(email_names)} templates")
            for name in email_names[:5]:
                print(f"   - {name}")
        except Exception as e:
            print(f"   ✗ Email templates failed: {e}")

        # Chip file
        print("\n18. CHIP FILE")
        try:
            chips = await event.chipfile.get()
            print(f"   Found {len(chips)} chip file entries")
            for c in chips[:3]:
                print(f"   - {c.transponder} -> {c.identification}")
        except Exception as e:
            print(f"   ✗ Chip file failed: {e}")

        # Data count (participants)
        print("\n19. PARTICIPANTS COUNT")
        try:
            count = await event.data.count()
            print(f"   Total participants: {count}")
        except Exception as e:
            print(f"   ✗ Count failed: {e}")

        # Data list (sample participants)
        print("\n20. PARTICIPANT DATA (first 5)")
        try:
            data = await event.data.list(
                fields=["Bib", "Firstname", "Lastname", "Contest", "Status"],
                limit_to=5
            )
            for row in data:
                print(f"   Bib {row[0]}: {row[1]} {row[2]} (Contest: {row[3]}, Status: {row[4]})")
        except Exception as e:
            print(f"   ✗ Data list failed: {e}")

        # Times (for first participant with bib)
        print("\n21. TIMES (first participant)")
        try:
            data = await event.data.list(fields=["Bib"], limit_to=1)
            if data and data[0][0]:
                bib = int(data[0][0])
                times = await event.times.get(Identifier.by_bib(bib))
                print(f"   Times for Bib {bib}: {len(times)} entries")
                for t in times[:3]:
                    print(f"   - Result {t.result}: {t.time_text}")
        except Exception as e:
            print(f"   ✗ Times failed: {e}")

        # Raw Data count
        print("\n22. RAW DATA")
        try:
            count = await event.rawdata.count(Identifier.by_filter(""))
            print(f"   Total raw data entries: {count}")
            distinct = await event.rawdata.distinct_values()
            print(f"   Decoder IDs: {distinct.decoder_id[:3]}")
        except Exception as e:
            print(f"   ✗ Raw data failed: {e}")

        # History (for first participant)
        print("\n23. HISTORY (first participant)")
        try:
            data = await event.data.list(fields=["Bib"], limit_to=1)
            if data and data[0][0]:
                bib = int(data[0][0])
                history = await event.history.get(Identifier.by_bib(bib))
                print(f"   History for Bib {bib}: {len(history)} entries")
                for h in history[:3]:
                    print(f"   - {h.field_name}: {h.old_value} -> {h.new_value}")
        except Exception as e:
            print(f"   ✗ History failed: {e}")

        # User Rights
        print("\n24. USER RIGHTS")
        try:
            rights = await api.user_rights_get(event_id)
            print(f"   Found {len(rights)} users with rights")
            for r in rights[:3]:
                print(f"   - {r.user_name} (ID: {r.user_id})")
        except Exception as e:
            print(f"   ✗ User rights failed: {e}")

        print("\n" + "=" * 60)
        print("LIVE TEST COMPLETE")
        print(f"Tested {24} API endpoint groups")


if __name__ == "__main__":
    asyncio.run(main())
