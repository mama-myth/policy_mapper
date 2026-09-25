import * as vscode from 'vscode';
import { PolicyLoader } from '../policies/policyLoader';
import { PolicyRecord } from '../policies/policyTypes';

export function registerShowPolicyGuidanceCommand(
  context: vscode.ExtensionContext,
  policyLoader: PolicyLoader
): vscode.Disposable {
  return vscode.commands.registerCommand('policyToCode.showPolicyGuidance', async () => {
    const policies = policyLoader.loadPolicies();

    if (policies.length === 0) {
      vscode.window.showWarningMessage('Policy-to-Code: No policy records available.');
      return;
    }

    const items = policies.map((policy: PolicyRecord) => ({
      label: `${policy.id}: ${policy.title}`,
      description: `[${policy.category}] - Severity: ${policy.severity}`,
      detail: policy.description,
      policy: policy
    }));

    const selected = await vscode.window.showQuickPick(items, {
      placeHolder: 'Select a policy record to view detailed guidance',
      matchOnDescription: true,
      matchOnDetail: true
    });

    if (selected) {
      const policy = selected.policy;
      const regContext = policy.supportingRegulatoryContext.map(
        r => `• ${r.framework} ${r.article} (${r.title}): ${r.relationship}`
      ).join('\n');

      const message = [
        `=== POLICY GUIDANCE: ${policy.id} ===`,
        `Title: ${policy.title}`,
        `Category: ${policy.category}`,
        `Description: ${policy.description}`,
        `Risk Explanation: ${policy.riskExplanation}`,
        `Suggested Action: ${policy.suggestedAction}`,
        `Safer Example: ${policy.saferExample}`,
        `Supporting Regulatory Context:\n${regContext}`,
        `\nDisclaimer: This is automated developer guidance, not legal advice or a compliance determination.`
      ].join('\n\n');

      vscode.window.showInformationMessage(message, { modal: true });
    }
  });
}
