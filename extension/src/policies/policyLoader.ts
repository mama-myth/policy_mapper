import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { PolicyRecord } from './policyTypes';

export class PolicyLoader {
  private extensionUri: vscode.Uri;
  private policiesCache: PolicyRecord[] | null = null;

  constructor(extensionUri: vscode.Uri) {
    this.extensionUri = extensionUri;
  }

  public loadPolicies(): PolicyRecord[] {
    if (this.policiesCache) {
      return this.policiesCache;
    }

    try {
      const policyFilePath = path.join(this.extensionUri.fsPath, 'resources', 'policies.json');
      if (!fs.existsSync(policyFilePath)) {
        vscode.window.showErrorMessage(`Policy-to-Code: Policy file not found at ${policyFilePath}`);
        return [];
      }

      const fileContent = fs.readFileSync(policyFilePath, 'utf-8');
      const data = JSON.parse(fileContent);

      if (!Array.isArray(data)) {
        vscode.window.showErrorMessage('Policy-to-Code: Malformed policy data. Expected array.');
        return [];
      }

      this.policiesCache = data as PolicyRecord[];
      return this.policiesCache;
    } catch (error: any) {
      vscode.window.showErrorMessage(`Policy-to-Code: Failed to load policies (${error.message})`);
      return [];
    }
  }

  public getPolicyById(id: string): PolicyRecord | undefined {
    const policies = this.loadPolicies();
    return policies.find(p => p.id === id);
  }
}
