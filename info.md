# AmberChest for Home Assistant

Brings [AmberChest](https://github.com/sphings79/amberchest) — the
self-hosted IMAP backup tool — into Home Assistant.

- A device per mailbox: archived messages, size on disk, folders, last backup
- A button that starts a backup, and one that cancels it
- A binary sensor while a backup runs, with folder and progress
- Total archive size and the next scheduled backup of the container
- A Lovelace card that shows every mailbox with a backup button
- English and German

Local polling over HTTP: no cloud, no account, no broker. After installing, add
it under **Settings → Devices & services** and enter host, port `8484` and the
password of the web interface.

## Three projects, one archive

| | What it is |
| --- | --- |
| [AmberChest](https://github.com/sphings79/amberchest) | The application: desktop app for macOS, Windows and Linux, plus a Docker container. Needed — this integration talks to it |
| [AmberChest Integration](https://github.com/sphings79/amberchest-home-assistant) | This one: devices, sensors, backup button, Lovelace card |
| [Home Assistant App (Add-on)](https://github.com/sphings79/amberchest-ha-app) | Runs AmberChest on Home Assistant OS, in the sidebar through ingress |

AmberChest itself is by [sphings79](https://github.com/sphings79) and
licensed under the AGPL-3.0; this integration is an MIT licensed client for its
HTTP API. Unofficial, community built, not affiliated with the Home Assistant
project.

If it is useful to you: a ⭐ on
[either repository](https://github.com/sphings79/amberchest-home-assistant)
helps, and there is a [coffee](https://buymeacoffee.com/sphings) button as well.
