from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "scheduler-card.js"
OUTPUT = ROOT / "gs-scheduler-card.js"


REPLACEMENTS = [
    ("dialog-scheduler-editor", "gs-dialog-scheduler-editor"),
    ("dialog-select-action", "gs-dialog-select-action"),
    ("dialog-select-condition", "gs-dialog-select-condition"),
    ("dialog-select-entities", "gs-dialog-select-entities"),
    ("dialog-select-weekdays", "gs-dialog-select-weekdays"),
    ("scheduler-card-editor", "gs-scheduler-card-editor"),
    ("scheduler-collapsible-group", "gs-scheduler-collapsible-group"),
    ("scheduler-collapsible-section", "gs-scheduler-collapsible-section"),
    ("scheduler-combo-selector", "gs-scheduler-combo-selector"),
    ("scheduler-entity-picker", "gs-scheduler-entity-picker"),
    ("scheduler-generic-dialog", "gs-scheduler-generic-dialog"),
    ("scheduler-item-row", "gs-scheduler-item-row"),
    ("scheduler-main-panel", "gs-scheduler-main-panel"),
    ("scheduler-options-panel", "gs-scheduler-options-panel"),
    ("scheduler-relative-time", "gs-scheduler-relative-time"),
    ("scheduler-settings-row", "gs-scheduler-settings-row"),
    ("scheduler-time-picker", "gs-scheduler-time-picker"),
    ("scheduler-timeslot-editor", "gs-scheduler-timeslot-editor"),
    ("scheduler-chip-set", "gs-scheduler-chip-set"),
    ("scheduler-chip", "gs-scheduler-chip"),
    ('type:"scheduler-card"', 'type:"gs-scheduler-card"'),
    ("type:'scheduler-card'", "type:'gs-scheduler-card'"),
    ('document.createElement("scheduler-card-editor")', 'document.createElement("gs-scheduler-card-editor")'),
    ('re("scheduler-card")', 're("gs-scheduler-card")'),
    ('name:"Scheduler Card"', 'name:"GS Scheduler Card"'),
    ('console.info("%c  SCHEDULER-CARD', 'console.info("%c  GS-SCHEDULER-CARD'),
    ("nielsfaber/scheduler-card/issues", "JasonPeng99/ha-scheduler-card-customer-kit/issues"),
]


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8", errors="ignore")
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    OUTPUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
