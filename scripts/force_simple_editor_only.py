from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "scheduler-card.js"


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8", errors="ignore")

    render_markers = [
        "render(){return this.config.simple_editor?q`",
        "render(){return q`",
    ]
    start = -1
    for marker in render_markers:
        idx = text.find(marker)
        if idx != -1:
            start = idx
            break
    if start == -1:
        raise ValueError("render() marker not found")
    end = text.index("`}_getSlotStop", start)

    replacement = """render(){return q`
    ${this.schedule.entries.map((e,t)=>q`
      <div class="editor-header">
        <div class="weekdays">
          <span>
            ${Fi("ui.panel.editor.repeated_days",this.hass)}:
            ${js(e.weekdays,"short",this.hass)}
          </span>
          <ha-icon-button .path=${Is} @click=${e=>this._showWeekdayDialog(e,t)}></ha-icon-button>
        </div>
      </div>

      <div class="simple-slot-list">
        ${e.slots.map((i,s)=>q`
          <button
            class="simple-slot-row ${this.selectedEntry===t&&this.selectedSlot===s?"selected":""}"
            @click=${()=>this._selectSlot(t,s)}
          >
            <span class="simple-slot-time">${this._formatSlotTime(i.start)} - ${this._formatSlotTime(this._getSlotStop(e,s))}</span>
            <span class="simple-slot-action">${this._describeSlotAction(i)}</span>
          </button>
        `)}
      </div>

      ${this.selectedEntry===t?q`
      <div class="simple-ops">
        <ha-button appearance="plain" @click=${e=>{this.selectedEntry=t,this._addTimeslot(e)}}>
          <ha-icon slot="start" icon="mdi:plus"></ha-icon>
          新增一段
        </ha-button>
        <ha-button
          appearance="plain"
          @click=${e=>{this.selectedEntry=t,this._removeTimeslot(e)}}
          ?disabled=${null===this.selectedSlot||e.slots.length<=2}
        >
          <ha-icon slot="start" icon="mdi:delete-outline"></ha-icon>
          刪除此段
        </ha-button>
      </div>
      ${this.renderSlot()}
      `:q``}
    `)}
    `"""

    text = text[:start] + replacement + text[end:]
    text = text.replace('if(!t)return"?芾身摰?;', 'if(!t)return"未設定";')
    text = text.replace('||"?芾身摰?', '||"未設定"')
    text = text.replace("新增一段", "新增一段")
    text = text.replace("刪除此段", "刪除此段")
    text = text.replace("``}_getSlotStop", "`}_getSlotStop")

    old_start = text.find("toggleViewMode(){")
    old_end = text.find("renderSlot(){", old_start)
    if old_start != -1 and old_end != -1:
        text = text[:old_start] + text[old_end:]

    source_snippet = """
        <span>${Fi("ui.panel.card_editor.fields.default_editor.heading",this.hass)}</span>
        <div class="two-columns">
          <div class="column">
            <ha-formfield label="${Fi("ui.panel.card_editor.fields.default_editor.options.single",this.hass)}">
              <ha-radio
                name="default_editor"
                value="${me.Single}"
                @change=${()=>{this._updateConfig({default_editor:me.Single})}}
                ?checked=${this._config.default_editor!=me.Scheme}
              >
              </ha-radio>
            </ha-formfield>
          </div>
          <div class="column">
            <ha-formfield label="${Fi("ui.panel.card_editor.fields.default_editor.options.scheme",this.hass)}">
              <ha-radio
                name="default_editor"
                value="${me.Scheme}"
                @change=${()=>{this._updateConfig({default_editor:me.Scheme})}}
                ?checked=${this._config.default_editor==me.Scheme}
              >
              </ha-radio>
            </ha-formfield>
          </div>
        </div>
"""
    text = text.replace(source_snippet, "")

    SOURCE.write_text(text, encoding="utf-8", newline="\n")
    print(f"Updated {SOURCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
