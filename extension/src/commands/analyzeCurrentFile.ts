import * as vscode from 'vscode';
import { PolicyLoader } from '../policies/policyLoader';
import { CodeContextDetector } from '../analyzer/codeContextDetector';
import { DetectedCodeContext } from '../analyzer/types';

export function registerAnalyzeCurrentFileCommand(
  context: vscode.ExtensionContext,
  policyLoader: PolicyLoader,
  outputChannel: vscode.OutputChannel
): vscode.Disposable {
  return vscode.commands.registerCommand('policyToCode.analyzeCurrentFile', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showInformationMessage('Policy-to-Code: No active text editor found.');
      return;
    }

    const document = editor.document;
    if (document.languageId !== 'python') {
      vscode.window.showInformationMessage(`Policy-to-Code: Analysis supports Python files (.py). Active file language is '${document.languageId}'.`);
      return;
    }

    const policies = policyLoader.loadPolicies();
    if (policies.length === 0) {
      vscode.window.showWarningMessage('Policy-to-Code: No policies loaded.');
      return;
    }

    const fileUri = document.uri.toString();
    const fileName = document.fileName;
    const text = document.getText();

    const findings: DetectedCodeContext[] = CodeContextDetector.analyzeDocumentText(
      fileUri,
      fileName,
      text,
      policies
    );

    outputChannel.clear();
    outputChannel.appendLine(`=== Policy-to-Code Analysis Report ===`);
    outputChannel.appendLine(`File: ${fileName}`);
    outputChannel.appendLine(`Timestamp: ${new Date().toLocaleString()}`);
    outputChannel.appendLine(`Total Findings: ${findings.length}\n`);

    if (findings.length === 0) {
      outputChannel.appendLine('No policy-relevant code patterns detected in this file.');
      outputChannel.show(true);
      vscode.window.showInformationMessage('Policy-to-Code: Analysis complete. No sensitive policy concerns detected.');
      return;
    }

    findings.forEach((finding, index) => {
      const policy = policyLoader.getPolicyById(finding.matchedPolicyId);
      outputChannel.appendLine(`Finding #${index + 1}:`);
      outputChannel.appendLine(`  Line: ${finding.lineNumber}`);
      outputChannel.appendLine(`  Code: ${finding.lineText.trim()}`);
      outputChannel.appendLine(`  Detected Function: ${finding.detectedLoggingFunction}`);
      outputChannel.appendLine(`  Matched Identifier: ${finding.matchedSensitiveIdentifier}`);
      outputChannel.appendLine(`  Matched Policy: ${finding.matchedPolicyId} - ${policy?.title || ''}`);
      outputChannel.appendLine(`  Severity: ${finding.severity.toUpperCase()}`);
      if (policy) {
        outputChannel.appendLine(`  Suggested Action: ${policy.suggestedAction}`);
        outputChannel.appendLine(`  Safer Example: ${policy.saferExample}`);
      }
      outputChannel.appendLine('');
    });

    outputChannel.show(true);
    vscode.window.showWarningMessage(`Policy-to-Code: Identified ${findings.length} advisory policy guidance item(s) in current file.`);
  });
}
