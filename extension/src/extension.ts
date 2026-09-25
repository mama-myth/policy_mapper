import * as vscode from 'vscode';
import { PolicyLoader } from './policies/policyLoader';
import { registerShowPolicyGuidanceCommand } from './commands/showPolicyGuidance';
import { registerAnalyzeCurrentFileCommand } from './commands/analyzeCurrentFile';

export function activate(context: vscode.ExtensionContext) {
    console.log('Policy-to-Code Mapper extension is now active!');

    const outputChannel = vscode.window.createOutputChannel('Policy-to-Code Guidance');
    context.subscriptions.push(outputChannel);

    const policyLoader = new PolicyLoader(context.extensionUri);

    const analyzeCommand = registerAnalyzeCurrentFileCommand(context, policyLoader, outputChannel);
    const showGuidanceCommand = registerShowPolicyGuidanceCommand(context, policyLoader);

    const viewTraceabilityCommand = vscode.commands.registerCommand('policyToCode.showTraceability', () => {
        vscode.window.showInformationMessage('Policy-to-Code: View Traceability invoked (Phase 2).');
    });

    context.subscriptions.push(analyzeCommand, showGuidanceCommand, viewTraceabilityCommand);
}

export function deactivate() {}
