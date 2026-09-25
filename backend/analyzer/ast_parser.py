import ast
from typing import Any, Dict, List, Optional


class SyntaxErrorResult:

    def __init__(self, message: str, lineno: int, offset: int):
        self.message = message
        self.lineno = lineno
        self.offset = offset

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": "SyntaxError",
            "message": self.message,
            "line": self.lineno,
            "offset": self.offset,
        }


def parse_python_code(
        code: str) -> tuple[Optional[ast.AST], Optional[SyntaxErrorResult]]:
    """Parses raw Python source code string into an AST module.

    Returns (ast_tree, None) on success or (None, SyntaxErrorResult) on syntax error.
    """
    try:
        tree = ast.parse(code)
        return tree, None
    except SyntaxError as e:
        return None, SyntaxErrorResult(
            message=e.msg, lineno=e.lineno or 1, offset=e.offset or 1)
