"""Draws the SVG artwork for the README and the brand assets.

Self contained pictures in the same palette Home Assistant uses, so they look
right in both GitHub themes.

    python3 dev/make-assets.py
"""

from pathlib import Path

BG = "#0f1720"
PANEL = "#16202b"
BORDER = "#28394a"
TEXT = "#e6edf3"
MUTED = "#9fb0c0"
HA = "#41BDF5"
VIOLET = "#7C7CF5"
GREEN = "#3ddc97"
AMBER = "#FFC107"
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, monospace"

OUT = Path("assets")


def frame(width: int, height: int, label: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{HA}"/>
      <stop offset="1" stop-color="{VIOLET}"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="16" fill="{BG}"/>
  <g font-family="{FONT}">
{body}  </g>
</svg>
"""


def escape(value: str) -> str:
    """Make a string safe to drop into an XML text node."""
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, value, fill=TEXT, size=14, weight=None, anchor=None, family=None):
    parts = [f'    <text x="{x}" y="{y}" fill="{fill}" font-size="{size}"']
    if weight:
        parts.append(f' font-weight="{weight}"')
    if anchor:
        parts.append(f' text-anchor="{anchor}"')
    if family:
        parts.append(f' font-family="{family}"')
    parts.append(f">{escape(str(value))}</text>\n")
    return "".join(parts)


def card(x, y, w, h, r=14, fill=PANEL, stroke=BORDER):
    return f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>\n'


def envelope(x, y, scale=1.0, colour="#fff", width=2.2):
    w, h = 26 * scale, 19 * scale
    return (
        f'    <g stroke="{colour}" stroke-width="{width}" fill="none" stroke-linejoin="round">\n'
        f'      <rect x="{x}" y="{y}" width="{w:.1f}" height="{h:.1f}" rx="{3 * scale:.1f}"/>\n'
        f'      <path d="M{x} {y + 4 * scale:.1f} {x + w / 2:.1f} {y + h - 4 * scale:.1f} {x + w:.1f} {y + 4 * scale:.1f}"/>\n'
        f"    </g>\n"
    )


def house(x, y, size=1.0, colour=HA, width=2.4):
    s = 28 * size
    return (
        f'    <g stroke="{colour}" stroke-width="{width}" fill="none" stroke-linejoin="round">\n'
        f'      <path d="M{x} {y + s * 0.5} {x + s * 0.5} {y} {x + s} {y + s * 0.5}"/>\n'
        f'      <path d="M{x + s * 0.14} {y + s * 0.45}v{s * 0.55}h{s * 0.72}v-{s * 0.55}"/>\n'
        # A door standing on the floor. An arc in the middle of the wall reads
        # as a mouth once the picture is big enough, and a downturned one.
        f'      <path d="M{x + s * 0.36} {y + s} v-{s * 0.32} a{s * 0.14} {s * 0.14} 0 0 1 {s * 0.28} 0 v{s * 0.32}"/>\n'
        f"    </g>\n"
    )


def banner() -> str:
    body = (
        card(0, 0, 1200, 400, 16, BG, "none")
        + f'    <circle cx="1040" cy="90" r="180" fill="url(#accent)" opacity="0.10"/>\n'
        + card(72, 96, 72, 72, 22, "url(#accent)", "none")
        + envelope(95, 120, 1.0)
        + text(172, 132, "Mail Archiver", TEXT, 34, "700")
        + text(172, 162, "for Home Assistant", HA, 20, "600")
        + text(
            72,
            224,
            "Every archived mailbox as a device: messages, archive size, last backup,",
            MUTED,
            17,
        )
        + text(
            72,
            250,
            "a running flag and a button that starts the next backup.",
            MUTED,
            17,
        )
        + card(72, 288, 190, 42, 21, PANEL, BORDER)
        + text(96, 315, "HACS · local polling", HA, 14, "600")
        + card(278, 288, 210, 42, 21, PANEL, BORDER)
        + text(302, 315, "Sensors · Button · Card", VIOLET, 14, "600")
        + card(504, 288, 168, 42, 21, PANEL, BORDER)
        + text(528, 315, "English · Deutsch", MUTED, 14, "600")
        + house(1020, 150, 3.4, HA, 3)
    )
    return frame(1200, 400, "Mail Archiver for Home Assistant", body)


def architecture() -> str:
    body = (
        text(60, 62, "How it works", TEXT, 22, "700")
        + text(
            60,
            92,
            "Home Assistant asks your Mail Archiver every 30 seconds. Nothing leaves your network.",
            MUTED,
            15,
        )
        + card(60, 140, 300, 200)
        + text(88, 180, "Mail Archiver", TEXT, 17, "600")
        + text(88, 206, "Desktop app or container", MUTED, 13)
        + text(88, 244, "GET  /api/accounts", HA, 13, family=MONO)
        + text(88, 268, "GET  /api/schedule", HA, 13, family=MONO)
        + text(88, 292, "POST /api/…/sync", VIOLET, 13, family=MONO)
        + text(88, 320, "port 8484", MUTED, 12, family=MONO)
        + f'    <path d="M372 240h96" stroke="{HA}" stroke-width="2.5" fill="none" marker-end="url(#arrow)"/>\n'
        + f'    <path d="M462 234l10 6-10 6z" fill="{HA}"/>\n'
        + text(420, 226, "HTTP", MUTED, 12, anchor="middle")
        + card(480, 140, 300, 200)
        + text(508, 180, "This integration", TEXT, 17, "600")
        + text(508, 206, "One coordinator per instance", MUTED, 13)
        + text(508, 244, "· a device per mailbox", MUTED, 13)
        + text(508, 268, "· sensors, binary sensor, buttons", MUTED, 13)
        + text(508, 292, "· re-login when the session drops", MUTED, 13)
        + f'    <path d="M792 240h96" stroke="{VIOLET}" stroke-width="2.5" fill="none"/>\n'
        + f'    <path d="M882 234l10 6-10 6z" fill="{VIOLET}"/>\n'
        + card(900, 140, 240, 200)
        + house(986, 176, 2.4, HA, 2.6)
        + text(1020, 280, "Home Assistant", TEXT, 16, "600", anchor="middle")
        + text(1020, 304, "Entities, automations, card", MUTED, 13, anchor="middle")
        + text(
            60,
            400,
            "No cloud, no broker, no account: the integration only talks to the address you enter.",
            MUTED,
            14,
        )
    )
    return frame(1200, 460, "How the integration talks to Mail Archiver", body)


def entities() -> str:
    rows = [
        ("sensor", "messages", "Messages", "12480", HA),
        ("sensor", "archive_size", "Archive size", "1.84 GB", HA),
        ("sensor", "folders", "Folders", "37", MUTED),
        ("sensor", "last_backup", "Last backup", "today, 03:00", HA),
        ("binary_sensor", "backup_running", "Backup running", "off", GREEN),
        ("button", "backup_now", "Back up now", "press", VIOLET),
        ("button", "cancel_backup", "Cancel backup", "press", MUTED),
    ]
    body = (
        text(60, 62, "Entities you get", TEXT, 22, "700")
        + text(
            60,
            92,
            "One device per mailbox, plus one for the instance itself.",
            MUTED,
            15,
        )
        + card(60, 130, 1080, 62, 14, "#101a24")
        + text(88, 168, "Domain", MUTED, 12, "600")
        + text(240, 168, "Entity", MUTED, 12, "600")
        + text(560, 168, "Name", MUTED, 12, "600")
        + text(980, 168, "Example", MUTED, 12, "600")
    )
    y = 192
    for domain, key, name, example, colour in rows:
        body += card(60, y, 1080, 56, 0, PANEL if (y // 56) % 2 else "#141d27", "none")
        body += text(88, y + 35, domain, MUTED, 13, family=MONO)
        body += text(240, y + 35, f"{key}", colour, 13, family=MONO)
        body += text(560, y + 35, name, TEXT, 14)
        body += text(980, y + 35, example, MUTED, 13, family=MONO)
        y += 56
    body += card(60, y + 20, 1080, 74)
    body += house(92, y + 40, 1.2, HA, 2.2)
    body += text(140, y + 52, "Instance device", TEXT, 15, "600")
    body += text(
        140,
        y + 74,
        "Total archive size and the next scheduled backup of the container.",
        MUTED,
        13,
    )
    return frame(1200, y + 130, "The entities the integration creates", body)


def dashboard() -> str:
    body = (
        text(60, 62, "The card", TEXT, 22, "700")
        + text(
            60,
            92,
            "Every mailbox with its numbers and a button, in one card.",
            MUTED,
            15,
        )
        + card(60, 130, 620, 300, 14)
        + envelope(92, 158, 0.8, HA, 2)
        + text(136, 178, "Mail Archiver", TEXT, 17, "500")
        + text(650, 168, "Archive: 1.84 GB", MUTED, 13, anchor="end")
        + text(650, 190, "Next run: in 6 hours", MUTED, 13, anchor="end")
        + f'    <line x1="60" y1="206" x2="680" y2="206" stroke="{BORDER}"/>\n'
        + text(92, 240, "Privat", TEXT, 15)
        + text(92, 262, "Last backup: 3 hours ago", MUTED, 12)
        + text(470, 240, "12,480", TEXT, 15, "500", anchor="end")
        + text(470, 262, "612 MB", MUTED, 12, anchor="end")
        + card(496, 226, 152, 34, 17, "none", BORDER)
        + text(572, 248, "Back up now", HA, 13, anchor="middle")
        + f'    <line x1="60" y1="286" x2="680" y2="286" stroke="{BORDER}"/>\n'
        + text(92, 320, "Arbeit", TEXT, 15)
        + text(92, 342, "backing up · downloading", GREEN, 12)
        + text(470, 320, "35,733", TEXT, 15, "500", anchor="end")
        + text(470, 342, "1.24 GB", MUTED, 12, anchor="end")
        + card(496, 306, 152, 34, 17, "none", BORDER)
        + text(572, 328, "Back up now", MUTED, 13, anchor="middle")
        + card(720, 130, 420, 300)
        + text(752, 172, "Automation example", TEXT, 16, "600")
        + text(752, 208, "trigger: state", MUTED, 13, family=MONO)
        + text(752, 232, "  entity_id: sensor.privat_last_backup", HA, 12, family=MONO)
        + text(752, 262, "condition: template", MUTED, 13, family=MONO)
        + text(752, 286, "  older than 26 hours", MUTED, 12, family=MONO)
        + text(752, 316, "action: notify.mobile_app", VIOLET, 13, family=MONO)
        + text(752, 348, '"The mail backup is overdue."', MUTED, 12, family=MONO)
        + text(752, 392, "Every value is a normal entity, so", MUTED, 13)
        + text(752, 412, "history and automations just work.", MUTED, 13)
    )
    return frame(1200, 480, "The Lovelace card and an automation example", body)


def install() -> str:
    steps = [
        (
            "1",
            "HACS",
            "Add this repository as a custom repository, category Integration.",
        ),
        ("2", "Install", "Install “Mail Archiver” and restart Home Assistant."),
        ("3", "Add", "Settings, Devices & services, Add integration, Mail Archiver."),
        (
            "4",
            "Connect",
            "Enter host, port 8484 and the password of the web interface.",
        ),
    ]
    body = text(60, 62, "Installation", TEXT, 22, "700")
    x = 60
    for number, title, description in steps:
        body += card(x, 100, 258, 200)
        body += f'    <circle cx="{x + 44}" cy="146" r="22" fill="url(#accent)"/>\n'
        body += text(x + 44, 153, number, "#0f1720", 18, "700", anchor="middle")
        body += text(x + 24, 206, title, TEXT, 17, "600")
        words = description.split()
        line, lines = "", []
        for word in words:
            if len(line) + len(word) > 30:
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        lines.append(line)
        for index, entry in enumerate(lines[:4]):
            body += text(x + 24, 234 + index * 20, entry, MUTED, 13)
        x += 282
    return frame(1200, 340, "The four installation steps", body)


def social() -> str:
    body = (
        f'    <circle cx="1120" cy="120" r="260" fill="url(#accent)" opacity="0.12"/>\n'
        + card(96, 150, 96, 96, 28, "url(#accent)", "none")
        + envelope(126, 186, 1.3)
        + text(224, 200, "Mail Archiver", TEXT, 46, "700")
        + text(224, 244, "for Home Assistant", HA, 28, "600")
        + text(
            96, 330, "Your mail backup as devices, sensors and a button —", MUTED, 22
        )
        + text(96, 366, "with a Lovelace card, in English and German.", MUTED, 22)
        + card(96, 420, 232, 52, 26, PANEL, BORDER)
        + text(212, 453, "HACS ready", HA, 17, "600", anchor="middle")
        + card(344, 420, 232, 52, 26, PANEL, BORDER)
        + text(460, 453, "Local polling", VIOLET, 17, "600", anchor="middle")
        + house(940, 300, 7.0, HA, 4)
    )
    return frame(1280, 640, "Mail Archiver for Home Assistant", body)


def brand_icon() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512" role="img" aria-label="Mail Archiver icon">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{HA}"/>
      <stop offset="1" stop-color="{VIOLET}"/>
    </linearGradient>
  </defs>
  <rect x="36" y="36" width="440" height="440" rx="112" fill="url(#g)"/>
  <g fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round">
    <rect x="132" y="168" width="248" height="182" rx="30"/>
    <path d="M132 202l124 92 124-92"/>
  </g>
</svg>
"""


def brand_logo() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 446 160" width="446" height="160" role="img" aria-label="Mail Archiver">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{HA}"/>
      <stop offset="1" stop-color="{VIOLET}"/>
    </linearGradient>
  </defs>
  <rect x="8" y="36" width="88" height="88" rx="26" fill="url(#g)"/>
  <g fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <rect x="30" y="60" width="44" height="34" rx="7"/>
    <path d="M30 68l22 17 22-17"/>
  </g>
  <text x="118" y="82" font-family="{FONT}" font-size="34" font-weight="700" fill="{HA}">Mail Archiver</text>
  <text x="118" y="112" font-family="{FONT}" font-size="18" fill="{VIOLET}">backup entities and a card</text>
</svg>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "banner.svg").write_text(banner())
    (OUT / "architecture.svg").write_text(architecture())
    (OUT / "entities.svg").write_text(entities())
    (OUT / "dashboard.svg").write_text(dashboard())
    (OUT / "install.svg").write_text(install())
    (OUT / "social-preview.svg").write_text(social())
    (OUT / "brand-icon.svg").write_text(brand_icon())
    (OUT / "brand-logo.svg").write_text(brand_logo())
    print("wrote", ", ".join(sorted(p.name for p in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
