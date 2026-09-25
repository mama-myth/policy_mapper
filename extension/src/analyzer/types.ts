export interface DetectedCodeContext {
  fileUri: string;
  fileName: string;
  lineNumber: number;
  lineText: string;
  detectedLoggingFunction: string;
  matchedSensitiveIdentifier: string;
  detectedPatternId: string;
  matchedPolicyId: string;
  severity: 'high' | 'medium' | 'low';
}
