import { PolicyRecord } from '../policies/policyTypes';
import { LoggingDetector } from './loggingDetector';
import { SensitiveIdentifierDetector } from './sensitiveIdentifierDetector';
import { DetectedCodeContext } from './types';

export class CodeContextDetector {
  public static analyzeLine(
    fileUri: string,
    fileName: string,
    lineNumber: number,
    lineText: string,
    policies: PolicyRecord[]
  ): DetectedCodeContext | null {
    const trimmed = lineText.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      return null;
    }

    const loggingResult = LoggingDetector.isLoggingLine(lineText);
    if (!loggingResult.isLogging || !loggingResult.matchedFunction) {
      return null;
    }

    for (const policy of policies) {
      // Check if function is listed in policy logging functions
      const funcMatch = policy.loggingFunctions.some(f => loggingResult.matchedFunction === f || loggingResult.matchedFunction?.startsWith(f));
      if (!funcMatch) {
        continue;
      }

      const matchedIdentifier = SensitiveIdentifierDetector.findMatchedIdentifier(
        lineText,
        policy.sensitiveIdentifiers
      );

      if (matchedIdentifier) {
        return {
          fileUri,
          fileName,
          lineNumber,
          lineText,
          detectedLoggingFunction: loggingResult.matchedFunction,
          matchedSensitiveIdentifier: matchedIdentifier,
          detectedPatternId: `${policy.id}-PAT-${lineNumber}`,
          matchedPolicyId: policy.id,
          severity: policy.severity
        };
      }
    }

    return null;
  }

  public static analyzeDocumentText(
    fileUri: string,
    fileName: string,
    documentText: string,
    policies: PolicyRecord[]
  ): DetectedCodeContext[] {
    const lines = documentText.split(/\r?\n/);
    const findings: DetectedCodeContext[] = [];

    lines.forEach((lineText, index) => {
      const result = this.analyzeLine(fileUri, fileName, index + 1, lineText, policies);
      if (result) {
        findings.push(result);
      }
    });

    return findings;
  }
}
