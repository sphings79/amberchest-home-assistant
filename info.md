# Mail Archiver for Home Assistant

Brings [Mail Archiver](https://github.com/sphings79/mail-archiver) — the
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

Mail Archiver itself is by [sphings79](https://github.com/sphings79) and
licensed under the AGPL-3.0; this integration is an MIT licensed client for its
HTTP API. Unofficial, community built, not affiliated with the Home Assistant
project.
