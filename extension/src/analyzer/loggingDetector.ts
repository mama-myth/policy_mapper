export class LoggingDetector {
  private static loggingPatterns = [
    /\bprint\s*\(/,
    /\blogging\.debug\s*\(/,
    /\blogging\.info\s*\(/,
    /\blogging\.warning\s*\(/,
    /\blogging\.error\s*\(/,
    /\blogging\.critical\s*\(/,
    /\blogging\.exception\s*\(/,
    /\blogger\.debug\s*\(/,
    /\blogger\.info\s*\(/,
    /\blogger\.warning\s*\(/,
    /\blogger\.error\s*\(/,
    /\blogger\.critical\s*\(/,
    /\blogger\.exception\s*\(/
  ];

  public static isLoggingLine(line: string): { isLogging: boolean; matchedFunction?: string } {
    for (const pattern of this.loggingPatterns) {
      const match = line.match(pattern);
      if (match) {
        // Extract function name, e.g. "logger.info" or "print"
        const funcName = match[0].replace(/\s*\($/, '');
        return { isLogging: true, matchedFunction: funcName };
      }
    }
    return { isLogging: false };
  }
}
