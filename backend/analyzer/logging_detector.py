import ast
from typing import List, Optional, Dict, Any
from backend.analyzer.sensitivity import extract_sensitive_identifiers
from backend.analyzer.ast_parser import parse_python_code

LOGGING_FUNCTIONS = {
    "print",
    "logging.debug",
    "logging.info",
    "logging.warning",
    "logging.error",
    "logging.critical",
    "logger.debug",
    "logger.info",
    "logger.warning",
    "logger.error",
    "logger.critical",
    "logger.exception",
}


def get_call_func_name(node: ast.Call) -> Optional[str]:
    """Extracts function name from AST Call node, e.g.

    'print', 'logging.info', or 'logger.error'.
    """
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        value_name = ""
        if isinstance(node.func.value, ast.Name):
            value_name = node.func.value.id
        elif isinstance(node.func.value, ast.Attribute):
            value_name = f"{node.func.value.value.id if isinstance(node.func.value.value, ast.Name) else ''}.{node.func.value.attr}"

        if value_name:
            return f"{value_name}.{node.func.attr}"
        return node.func.attr
    return None


class LoggingCallVisitor(ast.NodeVisitor):

    def __init__(self, code_lines: List[str]):
        self.code_lines = code_lines
        self.findings: List[Dict[str, Any]] = []

    def visit_Call(self, node: ast.Call):
        func_name = get_call_func_name(node)

        if func_name in LOGGING_FUNCTIONS:
            sensitive_ids = []

            # Check positional arguments
            for arg in node.args:
                sensitive_ids.extend(extract_sensitive_identifiers(arg))

            # Check keyword arguments
            for kw in node.keywords:
                if kw.arg and is_sensitive_keyword_arg(kw.arg):
                    sensitive_ids.append(kw.arg)
                sensitive_ids.extend(extract_sensitive_identifiers(kw.value))

            sensitive_ids = list(dict.fromkeys(sensitive_ids))

            if sensitive_ids:
                line_start = node.lineno
                line_end = getattr(node, "end_lineno", node.lineno)
                snippet = self._extract_snippet(line_start, line_end)

                for sens_id in sensitive_ids:
                    self.findings.append({
                        "observed_pattern":
                        "sensitive_value_passed_to_logging_function",
                        "function_called": func_name,
                        "sensitive_identifier": sens_id,
                        "line_start": line_start,
                        "line_end": line_end,
                        "snippet": snippet,
                    })

        self.generic_visit(node)

    def _extract_snippet(self, start: int, end: int) -> str:
        if 1 <= start <= len(self.code_lines):
            return "\n".join(self.code_lines[start - 1:end]).strip()
        return ""


def is_sensitive_keyword_arg(arg_name: str) -> bool:
    from backend.analyzer.sensitivity import is_sensitive_identifier_name
    return is_sensitive_identifier_name(arg_name)


def detect_sensitive_logging(
        code: str, file_name: str = "sample.py") -> Dict[str, Any]:
    """Main entry point to detect sensitive logging patterns in Python code string using AST.

    """
    tree, syntax_error = parse_python_code(code)
    if syntax_error:
        return {"file_name": file_name, "error": syntax_error.to_dict()}

    code_lines = code.splitlines()
    visitor = LoggingCallVisitor(code_lines)
    visitor.visit(tree)

    return {"file_name": file_name, "patterns": visitor.findings}
