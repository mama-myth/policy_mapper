import ast
from typing import List, Optional

SENSITIVE_KEYWORDS = {
    "password",
    "passwd",
    "pwd",
    "token",
    "access_token",
    "refresh_token",
    "api_key",
    "apikey",
    "secret",
    "credential",
    "credentials",
    "email",
}


def is_sensitive_identifier_name(name: str) -> bool:
    """Checks if a variable name or attribute name matches or contains sensitive keywords.

    """
    if not name:
        return False
    lower_name = name.lower()

    # Direct match or exact substring match against sensitive keywords
    for kw in SENSITIVE_KEYWORDS:
        if kw in lower_name:
            return True

    # Check split parts
    parts = lower_name.replace(".", "_").split("_")
    for part in parts:
        if part in SENSITIVE_KEYWORDS:
            return True

    return False


def extract_sensitive_identifiers(node: ast.AST) -> List[str]:
    """Recursively inspects an AST expression node for sensitive identifiers.

    """
    sensitive_found = []

    if isinstance(node, ast.Name):
        if is_sensitive_identifier_name(node.id):
            sensitive_found.append(node.id)

    elif isinstance(node, ast.Attribute):
        full_attr = get_attribute_full_name(node)
        if is_sensitive_identifier_name(
                node.attr) or is_sensitive_identifier_name(full_attr):
            sensitive_found.append(full_attr)

    elif isinstance(node, ast.JoinedStr):
        for value in node.values:
            sensitive_found.extend(extract_sensitive_identifiers(value))

    elif isinstance(node, ast.FormattedValue):
        sensitive_found.extend(extract_sensitive_identifiers(node.value))

    elif isinstance(node, ast.Call):
        for arg in node.args:
            sensitive_found.extend(extract_sensitive_identifiers(arg))
        for kw in node.keywords:
            sensitive_found.extend(extract_sensitive_identifiers(kw.value))

    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        for elt in node.elts:
            sensitive_found.extend(extract_sensitive_identifiers(elt))

    elif isinstance(node, ast.Dict):
        for val in node.values:
            if val:
                sensitive_found.extend(extract_sensitive_identifiers(val))

    return list(dict.fromkeys(sensitive_found))


def get_attribute_full_name(node: ast.AST) -> str:
    """Helper to reconstruct full attribute name like user.password or req.auth.token."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        parent = get_attribute_full_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""
