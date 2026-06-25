# BMB Lead Summary — Master Workflow (Mobile-First)

**Filed:** 2026-05-19
**Updated:** 2026-05-19 — switched from 5-workflow edit to 1 master workflow, added Tags + SMS as primary mobile-visibility layers.

## The mobile reality

Mike uses **LeadConnector mobile**. On that app:
- ✅ **Tags** = chips at top of contact card, visible without any tap
- ✅ **SMS to his phone** = lock-screen visible, no app open needed
- ❌ Notes = on a separate tab, requires navigation
- ❌ Custom fields = collapsed inside folder dropdowns, requires expansion

So the strategy is: **SMS hits his phone first** (lock-screen triage) → **tags show as chips** when he taps in (in-app triage) → **Note + custom fields** are the deeper reference for when he wants more detail.

## Goal

Every new BMB lead, regardless of source, gets:
1. **Auto-tagged** with `lead:`, `town:`, `timeline:`, `situation:`, `contact:` chips (visible on mobile contact card)
2. **SMS to Mike** with a one-line summary (visible on his lock screen)
3. **Note added** with the full structured summary (for desktop / deep review)

## One master workflow (5–7 min to build)

In **Automation → Workflows → + Create Workflow → Start from Scratch**:

### Name + trigger
- Name: `🔥 Lead Intake Summary (Master)`
- Trigger: **Contact Created** — no filter. Fires on every contact regardless of source.

### Actions (in this order)

#### Action 1 — Add Tags
**+ Add Action → Add Contact Tag**

This is where it gets manual: GHL workflow tag actions are static (one tag value per action), so to derive tags from field values you need **conditional logic** (If/Else branches). The pattern:

```
If contact.what_town_do_you_live_in CONTAINS "Duxbury" → add tag "town:duxbury"
Else if CONTAINS "Marshfield" → add tag "town:marshfield"
...
```

This is tedious. **Easier alternative:** skip in-workflow tag derivation and **let the existing tag backfill script run on a schedule** (e.g. every hour) to catch new contacts. Already built at `Modular/scripts/backfill_lead_tags.py`. Can wire it to a cron via the Apify MCP or a simple GitHub Action.

OR — even simpler — when Mike opens a new lead that doesn't have triage tags yet, the SMS + Note will already be there. The chips just show up within an hour via the scheduled script. Not real-time, but close enough.

#### Action 2 — Send SMS to User (Mike)
**+ Add Action → Send SMS → To User → Mike Biviano Jr**

Message (one line):
```
🔥 NEW LEAD: {{contact.first_name}} {{contact.last_name}} — {{contact.project_type}}{{contact.home_type}} — {{contact.what_town_do_you_live_in}} — {{contact.when_are_you_looking_to_move_into_your_new_home}}{{contact.project_timeframe}} — {{contact.preferred_contact_method}} — {{contact.phone}}
```

GHL renders empty merge tags as blanks, so a modular lead gets the move-in timeline; a decking lead gets the project timeframe; both work from the same line.

#### Action 3 — Add Note
**+ Add Action → Add Note**

Body:
```
🔥 NEW LEAD SUMMARY

Project Type: {{contact.project_type}}{{contact.home_type}}
Town:         {{contact.what_town_do_you_live_in}}
Timeline:     {{contact.when_are_you_looking_to_move_into_your_new_home}}{{contact.project_timeframe}}
Situation:    {{contact.what_best_describes_your_situation}}
What to build: {{contact.what_are_you_looking_to_build}}

Modular details:
  {{contact.number_of_bedrooms}}br / {{contact.number_of_bathrooms}}ba @ {{contact.estimated_square_footage}}{{contact.square_footage_youre_considering}} sqft
  Est cost: {{contact.home_total_number}}

Contact preference: {{contact.preferred_contact_method}}
Address: {{contact.address1}} {{contact.city}} {{contact.state}} {{contact.postal_code}}

Source: {{contact.utm_source}} → {{contact.utm_campaign}} → {{contact.utm_content}}
```

### Publish + test
1. Toggle workflow status **Draft → Published** (top right)
2. Test: submit a fake lead via `bivianomodularbuilders.com` form OR add a contact manually in GHL
3. Within 30 sec verify:
   - Your phone (Mike's number on his GHL user profile) buzzes with the SMS
   - The new contact has the `🔥 NEW LEAD SUMMARY` note attached
4. Delete the test contact when done

## What's already done ✅ (no action needed from you)

- **All 64 contacts from the last 30 days** have the summary Note backfilled. Mike opens any of them, sees the summary immediately.
- **20 contacts from that batch** got triage tags. The rest were bare/manual contacts with no survey data to tag from.
- The custom field reorg (49 fields into 6 emoji folders) is live.
- Tim Leedom (the example Mike sent) now has: `lead:modular · town:duxbury · timeline:asap · situation:owns-land · contact:text` as chips, plus the full Note. He's the canonical "this is the new format" reference contact.

## Optional: Run the tag-backfill on a schedule

Until someone wants to build the tedious If/Else tag derivation in the GHL workflow editor, the simplest play is to run the tag-backfill script every hour or two. New leads get tagged within an hour of landing. Options:

- **macOS launchd / cron** on Spencer's machine — single-line cron entry
- **GitHub Actions** — schedule the script in a small repo
- **Apify cron** — wrap the script as an Apify actor

Each ~5 min to set up. Just need to know which Spencer prefers.

## Why I couldn't auto-build the workflow

GHL Workflows are UI-only. Today I confirmed via 7+ API endpoint probes:
- ✅ List workflows
- ✅ Read/write contact notes
- ✅ Read/write contact tags
- ✅ Create custom field folders (new discovery)
- ❌ Create or modify workflows

If GHL ever opens workflow editing to API, we re-automate the whole thing.
