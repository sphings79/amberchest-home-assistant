# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[semantic versioning](https://semver.org/).

## [2.0.0] - 2026-09-09

### Changed

- **The project is now called AmberChest.** The application this integration
  talks to was renamed to avoid a collision with an older project of the same
  name, and this repository follows.
- **The domain changes from `mail_archiver` to `amberchest`**, which is a
  breaking change: entity ids, unique ids and the Lovelace card tag all carry
  the domain. There is no automatic migration — 1.0.0 was never listed in HACS
  and nobody is running it. Remove the old integration, install this one, add
  the instance again.
- The card is now `custom:amberchest-card`; a dashboard that used
  `custom:mail-archiver-card` has to be edited.

## [1.0.0] - 2026-09-08

### Added

- Config flow for an AmberChest instance: host, port, HTTPS and the interface
  password, with re-authentication when the server forgets its sessions.
- One device per mailbox, with sensors for messages, archive size, folders and
  the last backup, a binary sensor for a running backup and buttons to start or
  cancel one.
- A device for the instance itself, with the total archive size and the next
  scheduled backup.
- A Lovelace card that lists every mailbox with its numbers and a backup button.
- English and German, for both the interface and the card.
