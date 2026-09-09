# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[semantic versioning](https://semver.org/).

## [1.0.0] - 2026-09-08

### Added

- Config flow for a AmberChest instance: host, port, HTTPS and the interface
  password, with re-authentication when the server forgets its sessions.
- One device per mailbox, with sensors for messages, archive size, folders and
  the last backup, a binary sensor for a running backup and buttons to start or
  cancel one.
- A device for the instance itself, with the total archive size and the next
  scheduled backup.
- A Lovelace card that lists every mailbox with its numbers and a backup button.
- English and German, for both the interface and the card.
