# GS Scheduler Card

This repo contains a reusable Home Assistant frontend plugin derived from `scheduler-card`, but renamed and packaged as a separate custom card so it can be maintained independently from the upstream HACS `scheduler-card`.

## Included customizations

- Traditional Chinese UI patching
- Strong selected-timeslot highlight color
- Action row shows selected script name instead of icon-only display
- Customer-facing simplified editor enabled by default
- Designed to coexist with the original HACS `scheduler-card`

## Files

- `assets/scheduler-card.js`
  - Current validated source bundle used to build the independent plugin
- `scripts/build_independent_bundle.py`
  - Rewrites internal custom element tags and card type to `gs-*`
- `gs-scheduler-card.js`
  - Final HACS-installable frontend plugin bundle
- `src_schedule_summary_card.js`
  - Lightweight summary card source that renders timeslots/actions from one scheduler switch entity
- `hacs.json`
  - HACS metadata for a standalone dashboard plugin
- `examples/farm_schedule_template_sensors.yaml`
  - Reusable template sensors for current slot and current action
- `examples/farm_schedule_cards.yaml`
  - Reusable Lovelace cards for scheduler, current status, and full schedule summary

## Build

Run this locally after updating `assets/scheduler-card.js`:

```bash
python3 scripts/build_independent_bundle.py
```

Then always validate the bundle before releasing:

```bash
node --check assets/scheduler-card.js
node --check gs-scheduler-card.js
node scripts/check_bundle_registration.js gs-scheduler-card.js gs-scheduler-card
```

If you need to replace customer-facing Chinese text safely, prefer:

```bash
python scripts/utf8_replace.py <file> <old> <new>
```

## Install with HACS

1. Add this repository as a custom repository in HACS
2. Repository type: `Dashboard`
3. Install `GS Scheduler Card`
4. Reload Home Assistant frontend
5. Add card with:

```yaml
type: custom:gs-scheduler-card
```

For the summary card:

```yaml
type: custom:gs-schedule-summary-card
entity: switch.schedule_feng_shan_pai_cheng
title: 風扇排程總攬
```

By default, `GS Scheduler Card` opens the schedule editor in the simplified customer-facing mode.

If you want to be explicit:

```yaml
type: custom:gs-scheduler-card
simple_editor: true
```

To fall back to the more advanced/original editing workflow:

```yaml
type: custom:gs-scheduler-card
simple_editor: false
```

## Reuse the farm schedule UI on another host

1. Install `GS Scheduler Card` from HACS
2. Import the template sensors from:

```text
examples/farm_schedule_template_sensors.yaml
```

3. Copy the card examples from:

```text
examples/farm_schedule_cards.yaml
```

4. Replace the entity IDs, script IDs, and schedule switch IDs with the target site values

## Refresh frontend

After install or update:

```text
Ctrl + Shift + R
```

If the page still looks unchanged, fully close and reopen the browser tab.

## Notes

- This plugin is meant to be maintained separately from the original HACS `scheduler-card`
- Upstream scheduler-card changes are not automatically inherited
- When you want to import new upstream fixes, update `assets/scheduler-card.js` and rebuild `gs-scheduler-card.js`
- This plugin coexists with the original card because all custom elements and the Lovelace card type are renamed to the `gs-` prefix
- The repo now enforces UTF-8 plus LF through `.editorconfig` and `.gitattributes`
- When editing customer-facing Chinese text, prefer UTF-8-safe file writes over shell heredocs that depend on terminal codepages
- See [WORKFLOW.md](/C:/Users/bbman/OneDrive/文件/Building/scheduler-card-customer-kit/WORKFLOW.md) for the release and validation checklist
