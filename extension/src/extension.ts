import * as vscode from 'vscode';
import * as http from 'http';

interface CodeEvidence {
    line_start: number;
    line_end: number;
    function_called: string;
    sensitive_identifier: string;
    snippet: string;
}

interface PolicyReference {
    id: string;
    title: string;
    category: string;
}

interface RegulatoryContext {
    framework: string;
    article: string;
    title: string;
    relationship: string;
}

interface Traceability {
    code_to_pattern: string;
    pattern_to_policy: string;
    policy_to_context: string;
}

interface Finding {
    finding_id: string;
    guidance_type: string;
    severity: string;
    title: string;
    potential_policy_consideration: string;
    code_evidence: CodeEvidence;
    observed_pattern: string;
    policy_reference: PolicyReference;
    supporting_regulatory_context: RegulatoryContext[];
    why_this_matters: string;
    recommended_action: string;
    safer_example: string;
    traceability: Traceability;
    disclaimer: string;
}

interface AnalysisResponse {
    analysis_id: string;
    language: string;
    file_name: string;
    findings: Finding[];
}

let activeFindings: Finding[] = [];
let localFeedbackLog: { finding_id: string; action: string; timestamp: string }[] = [];
let diagnosticCollection: vscode.DiagnosticCollection;

export function activate(context: vscode.ExtensionContext) {
    diagnosticCollection = vscode.languages.createDiagnosticCollection('policyToCode');
    context.subscriptions.push(diagnosticCollection);

    // Command: Analyze Current File
    const analyzeCommand = vscode.commands.registerCommand('policyToCode.analyzeFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('Policy-to-Code: No active editor found.');
            return;
        }

        const document = editor.document;
        if (document.languageId !== 'python') {
            vscode.window.showWarningMessage('Policy-to-Code Mapper currently supports Python files only.');
            return;
        }

        const code = document.getText();
        const fileName = document.fileName;

        try {
            const response = await sendAnalyzeRequest(code, fileName);
            activeFindings = response.findings;
            updateDiagnostics(document, activeFindings);

            if (activeFindings.length === 0) {
                vscode.window.showInformationMessage('Policy-to-Code: Analysis complete. No sensitive policy concerns detected.');
            } else {
                vscode.window.showWarningMessage(`Policy-to-Code: Identified ${activeFindings.length} advisory policy guidance item(s).`);
            }
        } catch (error: any) {
            vscode.window.showErrorMessage(`Policy-to-Code Backend Unavailable: Ensure local server is running on http://127.0.0.1:8000 (${error.message})`);
        }
    });

    // Command: View Traceability
    const traceabilityCommand = vscode.commands.registerCommand('policyToCode.viewTraceability', () => {
        if (activeFindings.length === 0) {
            vscode.window.showInformationMessage('Policy-to-Code: No active guidance findings to display traceability for.');
            return;
        }

        const finding = activeFindings[0];
        const reg = finding.supporting_regulatory_context[0];

        const message = [
            `Policy-to-Code Traceability Chain:`,
            `1. Source Code Evidence: ${finding.code_evidence.snippet}`,
            `2. Observed Code Pattern: ${finding.code_evidence.sensitive_identifier} -> ${finding.code_evidence.function_called}()`,
            `3. Internal Policy Requirement: ${finding.policy_reference.id} - ${finding.policy_reference.title}`,
            `4. Supporting Regulatory Context: ${reg.framework} ${reg.article} - ${reg.title}`,
            `5. Suggested Developer Action: ${finding.recommended_action}`,
            `\nDisclaimer: ${finding.disclaimer}`
        ].join('\n\n');

        vscode.window.showInformationMessage(message, { modal: true });
    });

    // Feedback Commands (Local storage only)
    const feedbackHelpful = vscode.commands.registerCommand('policyToCode.feedbackHelpful', () => {
        if (activeFindings.length > 0) {
            recordFeedback(activeFindings[0].finding_id, 'helpful');
            vscode.window.showInformationMessage('Policy-to-Code: Feedback recorded locally (Helpful). Thank you!');
        }
    });

    const feedbackNotHelpful = vscode.commands.registerCommand('policyToCode.feedbackNotHelpful', () => {
        if (activeFindings.length > 0) {
            recordFeedback(activeFindings[0].finding_id, 'not_helpful');
            vscode.window.showInformationMessage('Policy-to-Code: Feedback recorded locally (Not Helpful). Thank you!');
        }
    });

    const dismissGuidance = vscode.commands.registerCommand('policyToCode.dismissGuidance', () => {
        diagnosticCollection.clear();
        activeFindings = [];
        vscode.window.showInformationMessage('Policy-to-Code: Guidance dismissed.');
    });

    // Hover Provider Registration
    const hoverProvider = vscode.languages.registerHoverProvider('python', {
        provideHover(document, position, token) {
            for (const finding of activeFindings) {
                const line = finding.code_evidence.line_start - 1;
                if (position.line === line) {
                    const markdown = new vscode.MarkdownString();
                    markdown.isTrusted = true;

                    markdown.appendMarkdown(`### Policy-to-Code Guidance (${finding.policy_reference.id})\n\n`);
                    markdown.appendMarkdown(`**Potential Policy Consideration:** ${finding.potential_policy_consideration}\n\n`);
                    markdown.appendMarkdown(`**Relevant Organizational Policy:** ${finding.policy_reference.id} — ${finding.policy_reference.title}\n\n`);
                    markdown.appendMarkdown(`**Why This Matters:** ${finding.why_this_matters}\n\n`);

                    if (finding.supporting_regulatory_context.length > 0) {
                        const reg = finding.supporting_regulatory_context[0];
                        markdown.appendMarkdown(`**Supporting Regulatory Context:** ${reg.framework} ${reg.article} (${reg.title})\n\n`);
                    }

                    markdown.appendMarkdown(`**Suggested Developer Action:** ${finding.recommended_action}\n\n`);
                    markdown.appendMarkdown(`**Safer Example:** \`${finding.safer_example}\` \n\n`);
                    markdown.appendMarkdown(`---\n*Disclaimer: ${finding.disclaimer}*`);

                    return new vscode.Hover(markdown);
                }
            }
            return undefined;
        }
    });

    context.subscriptions.push(
        analyzeCommand,
        traceabilityCommand,
        feedbackHelpful,
        feedbackNotHelpful,
        dismissGuidance,
        hoverProvider
    );
}

function recordFeedback(findingId: string, action: string) {
    localFeedbackLog.push({
        finding_id: findingId,
        action: action,
        timestamp: new Date().toISOString()
    });
}

function updateDiagnostics(document: vscode.TextDocument, findings: Finding[]) {
    diagnosticCollection.clear();
    const diagnostics: vscode.Diagnostic[] = [];

    for (const finding of findings) {
        const line = Math.max(0, finding.code_evidence.line_start - 1);
        const lineText = document.lineAt(line).text;
        const range = new vscode.Range(line, 0, line, lineText.length);

        const diagnostic = new vscode.Diagnostic(
            range,
            `[Policy Guidance] ${finding.title}: ${finding.potential_policy_consideration} (${finding.policy_reference.id})`,
            vscode.DiagnosticSeverity.Warning
        );
        diagnostic.source = 'Policy-to-Code';
        diagnostics.push(diagnostic);
    }

    diagnosticCollection.set(document.uri, diagnostics);
}

function sendAnalyzeRequest(code: string, fileName: string): Promise<AnalysisResponse> {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({
            language: 'python',
            file_name: fileName,
            code: code
        });

        const options: http.RequestOptions = {
            hostname: '127.0.0.1',
            port: 8000,
            path: '/analyze',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const responseObj: AnalysisResponse = JSON.parse(data);
                        resolve(responseObj);
                    } catch (e) {
                        reject(new Error('Invalid JSON response from backend.'));
                    }
                } else {
                    reject(new Error(`Server returned HTTP ${res.statusCode}`));
                }
            });
        });

        req.on('error', (e) => {
            reject(e);
        });

        req.setTimeout(5000, () => {
            req.destroy();
            reject(new Error('Request timed out.'));
        });

        req.write(postData);
        req.end();
    });
}

export function deactivate() {
    if (diagnosticCollection) {
        diagnosticCollection.clear();
    }
}
