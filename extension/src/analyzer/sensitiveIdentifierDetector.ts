export class SensitiveIdentifierDetector {
  public static findMatchedIdentifier(lineText: string, sensitiveIdentifiers: string[]): string | undefined {
    for (const identifier of sensitiveIdentifiers) {
      // Escape special characters if any
      const escaped = identifier.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      // Look for word boundaries or object dot notation e.g., user.email or password
      const regex = new RegExp(`(?:\\b|\\.)${escaped}\\b`, 'i');
      if (regex.test(lineText)) {
        return identifier;
      }
    }
    return undefined;
  }
}
