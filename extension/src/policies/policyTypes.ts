export interface SupportingRegulatoryContext {
  framework: string;
  article: string;
  title: string;
  relationship: string;
}

export interface PolicyRecord {
  id: string;
  title: string;
  category: string;
  description: string;
  riskExplanation: string;
  sensitiveIdentifiers: string[];
  loggingFunctions: string[];
  suggestedAction: string;
  saferExample: string;
  supportingRegulatoryContext: SupportingRegulatoryContext[];
  severity: 'high' | 'medium' | 'low';
}
