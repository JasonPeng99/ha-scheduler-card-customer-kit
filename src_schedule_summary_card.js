class GsScheduleSummaryCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  setConfig(config) {
    if (!config || !config.entity) {
      throw new Error("You need to define an entity");
    }
    this._config = config;
    this.render();
  }

  getCardSize() {
    return 3;
  }

  _friendlyAction(service) {
    if (!service || !this._hass) return "未設定";
    const state = this._hass.states[service];
    if (state?.attributes?.friendly_name) {
      return state.attributes.friendly_name;
    }
    return service;
  }

  _formatRows() {
    const entity = this._config.entity;
    const state = this._hass?.states?.[entity];
    const times = state?.attributes?.timeslots || [];
    const acts = state?.attributes?.actions || [];
    const current = state?.attributes?.current_slot;

    if (!times.length) {
      return `<div class="empty">尚無排程資料</div>`;
    }

    const rows = times.map((slot, idx) => {
      const parts = String(slot).split(" - ");
      const short = parts.length > 1 ? `${parts[0].slice(0, 5)} - ${parts[1].slice(0, 5)}` : slot;
      const service = acts[idx]?.service || "";
      const action = this._friendlyAction(service);
      const isCurrent = current === idx;
      return `
        <tr class="${isCurrent ? "current" : ""}">
          <td>${isCurrent ? "👉 目前" : ""}</td>
          <td>${isCurrent ? `<strong>${short}</strong>` : short}</td>
          <td>${isCurrent ? `<strong>${action}</strong>` : action}</td>
        </tr>
      `;
    }).join("");

    return `
      <table>
        <thead>
          <tr>
            <th>狀態</th>
            <th>時段</th>
            <th>動作</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    `;
  }

  render() {
    if (!this._config || !this._hass) return;
    if (!this.shadowRoot) {
      this.attachShadow({ mode: "open" });
    }
    const title = this._config.title || "排程總攬";
    this.shadowRoot.innerHTML = `
      <style>
        ha-card {
          display: block;
          padding: 16px;
        }
        .title {
          font-size: 1.1rem;
          font-weight: 600;
          margin-bottom: 12px;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.95rem;
        }
        th, td {
          text-align: left;
          padding: 8px 6px;
          border-bottom: 1px solid rgba(127,127,127,0.18);
          vertical-align: top;
        }
        th {
          color: var(--secondary-text-color);
          font-weight: 600;
        }
        td:first-child {
          white-space: nowrap;
          width: 72px;
        }
        td:nth-child(2) {
          white-space: nowrap;
          width: 120px;
        }
        .current td {
          background: rgba(var(--rgb-primary-color), 0.08);
        }
        .empty {
          color: var(--secondary-text-color);
        }
      </style>
      <ha-card>
        <div class="title">${title}</div>
        ${this._formatRows()}
      </ha-card>
    `;
  }
}

customElements.define("gs-schedule-summary-card", GsScheduleSummaryCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "gs-schedule-summary-card",
  name: "GS Schedule Summary Card",
  description: "Summary table for a scheduler switch entity",
});
