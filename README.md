# HA Scheduler Card Customer Kit

This repo contains a reusable patched `scheduler-card` bundle for Home Assistant customer deployments.

## Included customizations

- Traditional Chinese UI patching
- Strong selected-timeslot highlight color
- Action row shows selected script name instead of icon-only display
- Compatible with the current HACS `scheduler-card` resource path:
  - `/hacsfiles/scheduler-card/scheduler-card.js?...`

## Files

- `assets/scheduler-card.js`
  - Current patched frontend bundle
- `scripts/apply_to_home_assistant.py`
  - Copies the patched bundle into Home Assistant
  - Rebuilds `scheduler-card.js.gz`
  - Bumps the Lovelace resource version string

## Apply on Home Assistant

Run this on the Home Assistant host filesystem where `/homeassistant` is the config root:

```bash
python3 scripts/apply_to_home_assistant.py /homeassistant
```

Then refresh the frontend with:

```text
Ctrl + Shift + R
```

If the page still looks unchanged, fully close and reopen the browser tab.

## Notes

- This is a direct frontend patch of the installed `scheduler-card` bundle.
- HACS updates may overwrite the patched file.
- If HACS updates `scheduler-card`, re-run the apply script.
