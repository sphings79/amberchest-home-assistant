/** The card's texts. English is the fallback for anything missing. */
export interface Strings {
  title: string;
  noAccounts: string;
  messages: string;
  size: string;
  lastBackup: string;
  never: string;
  running: string;
  backUpNow: string;
  nextRun: string;
  total: string;
}

export const en: Strings = {
  title: 'AmberChest',
  noAccounts: 'No mailbox found. Is the AmberChest integration set up?',
  messages: 'Messages',
  size: 'Size',
  lastBackup: 'Last backup',
  never: 'never',
  running: 'backing up',
  backUpNow: 'Back up now',
  nextRun: 'Next run',
  total: 'Archive',
};

export const de: Strings = {
  title: 'AmberChest',
  noAccounts: 'Kein Postfach gefunden. Ist die AmberChest-Integration eingerichtet?',
  messages: 'Nachrichten',
  size: 'Größe',
  lastBackup: 'Letzte Sicherung',
  never: 'nie',
  running: 'sichert gerade',
  backUpNow: 'Jetzt sichern',
  nextRun: 'Nächster Lauf',
  total: 'Archiv',
};

export function strings(language: string | undefined): Strings {
  // Home Assistant hands out regional codes like de-CH.
  return (language ?? 'en').split('-')[0] === 'de' ? de : en;
}
