import { LitElement, css, html, nothing, type TemplateResult } from 'lit';
import { strings, type Strings } from './locales.js';

interface HassEntity {
  entity_id: string;
  state: string;
  attributes: Record<string, unknown>;
}

interface HassEntityRegistryEntry {
  platform?: string;
  device_id?: string | null;
}

interface HassDevice {
  id: string;
  name_by_user?: string | null;
  name?: string | null;
}

interface Hass {
  language?: string;
  states: Record<string, HassEntity>;
  entities?: Record<string, HassEntityRegistryEntry>;
  devices?: Record<string, HassDevice>;
  callService: (domain: string, service: string, data: Record<string, unknown>) => Promise<unknown>;
  formatEntityState?: (entity: HassEntity) => string;
}

interface CardConfig {
  type: string;
  title?: string;
  /** Hide the row of mailboxes that have nothing archived yet. */
  hide_empty?: boolean;
}

interface Mailbox {
  deviceId: string;
  name: string;
  messages: number | null;
  bytes: number | null;
  lastBackup: string | null;
  running: boolean;
  phase: string | null;
  backupButton: string | null;
}

const DOMAIN = 'amberchest';

function bytes(value: number | null): string {
  if (value === null) return '–';
  if (value < 1024) return `${value} B`;
  const units = ['KB', 'MB', 'GB', 'TB'];
  let size = value / 1024;
  let unit = 0;
  while (size >= 1024 && unit < units.length - 1) {
    size /= 1024;
    unit += 1;
  }
  return `${size.toFixed(size < 10 ? 1 : 0)} ${units[unit]}`;
}

/** "vor 3 Std." style, using the browser's own relative time formatting. */
function ago(iso: string | null, language: string, never: string): string {
  if (!iso) return never;
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return never;

  const seconds = Math.round((then - Date.now()) / 1000);
  const format = new Intl.RelativeTimeFormat(language, { numeric: 'auto' });
  const steps: Array<[Intl.RelativeTimeFormatUnit, number]> = [
    ['second', 60],
    ['minute', 60],
    ['hour', 24],
    ['day', 30],
    ['month', 12],
  ];

  let value = seconds;
  for (const [unit, limit] of steps) {
    if (Math.abs(value) < limit) return format.format(Math.round(value), unit);
    value /= limit;
  }
  return format.format(Math.round(value), 'year');
}

export class AmberChestCard extends LitElement {
  static properties = {
    hass: { attribute: false },
    _config: { state: true },
  };

  declare hass?: Hass;
  declare private _config?: CardConfig;

  static styles = css`
    ha-card {
      padding: 12px 0 4px;
    }
    .head {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 4px 16px 10px;
    }
    .head .name {
      font-size: 1.15rem;
      font-weight: 500;
      color: var(--primary-text-color);
    }
    .head .total {
      margin-left: auto;
      font-size: 0.85rem;
      color: var(--secondary-text-color);
      text-align: right;
    }
    .row {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 16px;
      border-top: 1px solid var(--divider-color);
    }
    .row .label {
      min-width: 0;
      flex: 1;
    }
    .row .name {
      color: var(--primary-text-color);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .row .meta {
      font-size: 0.8rem;
      color: var(--secondary-text-color);
    }
    .numbers {
      text-align: right;
      font-size: 0.8rem;
      color: var(--secondary-text-color);
      white-space: nowrap;
    }
    .numbers strong {
      display: block;
      font-size: 0.95rem;
      font-weight: 500;
      color: var(--primary-text-color);
    }
    button {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--divider-color);
      border-radius: 18px;
      background: none;
      color: var(--primary-color);
      font: inherit;
      font-size: 0.8rem;
      padding: 6px 12px;
      cursor: pointer;
    }
    button:disabled {
      color: var(--secondary-text-color);
      cursor: default;
    }
    .empty {
      padding: 8px 16px 16px;
      color: var(--secondary-text-color);
    }
    .spin {
      animation: spin 1.4s linear infinite;
    }
    @keyframes spin {
      to {
        transform: rotate(360deg);
      }
    }
  `;

  setConfig(config: CardConfig): void {
    this._config = config;
  }

  getCardSize(): number {
    return 1 + this._mailboxes().length;
  }

  static getStubConfig(): CardConfig {
    return { type: `custom:${DOMAIN}-card` };
  }

  /** Collects the entities of the integration and groups them by device. */
  private _mailboxes(): Mailbox[] {
    const hass = this.hass;
    if (!hass?.entities || !hass.devices) return [];

    const boxes = new Map<string, Mailbox>();

    for (const [entityId, entry] of Object.entries(hass.entities)) {
      if (entry.platform !== DOMAIN || !entry.device_id) continue;
      const state = hass.states[entityId];
      if (!state) continue;

      // The instance device carries the totals, not a mailbox.
      const unique = entityId.split('.')[1] ?? '';
      const device = hass.devices[entry.device_id];
      if (!device) continue;

      let box = boxes.get(entry.device_id);
      if (!box) {
        box = {
          deviceId: entry.device_id,
          name: device.name_by_user || device.name || unique,
          messages: null,
          bytes: null,
          lastBackup: null,
          running: false,
          phase: null,
          backupButton: null,
        };
        boxes.set(entry.device_id, box);
      }

      const kind = String(state.attributes.device_class ?? '');
      const unit = String(state.attributes.unit_of_measurement ?? '');

      if (entityId.startsWith('binary_sensor.')) {
        box.running = state.state === 'on';
        box.phase = (state.attributes.phase as string) ?? null;
      } else if (entityId.startsWith('button.')) {
        // The cancel button is disabled by default and never shows up here.
        if (box.backupButton === null) box.backupButton = entityId;
      } else if (kind === 'data_size') {
        box.bytes = Number(state.state) * (unit === 'MB' ? 1024 * 1024 : 1);
      } else if (kind === 'timestamp') {
        box.lastBackup = state.state === 'unknown' ? null : state.state;
      } else if (unit === 'messages') {
        box.messages = Number(state.state);
      }
    }

    // A mailbox has a message count; the instance device does not.
    return [...boxes.values()]
      .filter((box) => box.messages !== null)
      .sort((a, b) => a.name.localeCompare(b.name));
  }

  private _totals(): { bytes: number; nextRun: string | null } {
    const hass = this.hass;
    let total = 0;
    let nextRun: string | null = null;
    if (!hass?.entities) return { bytes: total, nextRun };

    for (const [entityId, entry] of Object.entries(hass.entities)) {
      if (entry.platform !== DOMAIN) continue;
      const state = hass.states[entityId];
      if (!state) continue;
      const accounts = state.attributes.accounts;
      if (typeof accounts === 'number') {
        const unit = String(state.attributes.unit_of_measurement ?? '');
        total = Number(state.state) * (unit === 'MB' ? 1024 * 1024 : 1);
      }
      if (state.attributes.cron !== undefined && state.state !== 'unknown') {
        nextRun = state.state;
      }
    }
    return { bytes: total, nextRun };
  }

  private async _backup(entityId: string): Promise<void> {
    await this.hass?.callService('button', 'press', { entity_id: entityId });
  }

  render(): TemplateResult | typeof nothing {
    const hass = this.hass;
    if (!hass || !this._config) return nothing;

    const t: Strings = strings(hass.language);
    const language = hass.language ?? 'en';
    const mailboxes = this._mailboxes().filter(
      (box) => !this._config?.hide_empty || (box.messages ?? 0) > 0,
    );
    const totals = this._totals();

    return html`
      <ha-card>
        <div class="head">
          <ha-icon icon="mdi:email-sync-outline"></ha-icon>
          <span class="name">${this._config.title ?? t.title}</span>
          <span class="total">
            ${t.total}: ${bytes(totals.bytes)}
            ${totals.nextRun
              ? html`<br />${t.nextRun}: ${ago(totals.nextRun, language, t.never)}`
              : nothing}
          </span>
        </div>

        ${mailboxes.length === 0
          ? html`<div class="empty">${t.noAccounts}</div>`
          : mailboxes.map(
              (box) => html`
                <div class="row">
                  <div class="label">
                    <div class="name">${box.name}</div>
                    <div class="meta">
                      ${box.running
                        ? html`<ha-icon class="spin" icon="mdi:loading" style="--mdc-icon-size:14px"></ha-icon>
                            ${t.running}${box.phase ? ` · ${box.phase}` : ''}`
                        : html`${t.lastBackup}: ${ago(box.lastBackup, language, t.never)}`}
                    </div>
                  </div>
                  <div class="numbers">
                    <strong>${(box.messages ?? 0).toLocaleString(language)}</strong>
                    ${bytes(box.bytes)}
                  </div>
                  <button
                    ?disabled=${box.running || !box.backupButton}
                    @click=${() => box.backupButton && this._backup(box.backupButton)}
                  >
                    <ha-icon icon="mdi:cloud-download" style="--mdc-icon-size:16px"></ha-icon>
                    ${t.backUpNow}
                  </button>
                </div>
              `,
            )}
      </ha-card>
    `;
  }
}

customElements.define('amberchest-card', AmberChestCard);

// Makes the card appear in the "add card" dialog.
const cards = ((window as unknown as { customCards?: unknown[] }).customCards ??= []);
cards.push({
  type: 'amberchest-card',
  name: 'AmberChest',
  description: 'Every archived mailbox with its numbers and a backup button.',
  preview: true,
});
