# compliance.py
# -------------
# Compliance-aware helpers for tagging and redacting sensitive data.

import re


SENSITIVE_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}

REDACTION_LABELS = {
    "email": "[REDACTED_EMAIL]",
    "phone": "[REDACTED_PHONE]",
    "ssn": "[REDACTED_SSN]",
    "credit_card": "[REDACTED_CARD]",
}


def detect_sensitive_types(text):
    """Return a list of sensitive data types found in text."""
    if not text:
        return []

    return [
        data_type
        for data_type, pattern in SENSITIVE_PATTERNS.items()
        if pattern.search(text)
    ]


def classify_sensitivity(data_types, default="public"):
    """Map detected data types to a simple sensitivity level."""
    if not data_types:
        return default

    if "ssn" in data_types or "credit_card" in data_types:
        return "restricted"

    return "confidential"


def build_metadata(text, source, default_sensitivity="public"):
    """
    Build metadata tags for a text item.

    ChromaDB metadata values must be simple scalar values, so lists are stored
    as comma-separated strings.
    """
    data_types = detect_sensitive_types(text)
    sensitivity = classify_sensitivity(data_types, default=default_sensitivity)

    return {
        "source": source,
        "sensitivity": sensitivity,
        "data_type": ",".join(data_types) if data_types else "operational",
        "contains_sensitive_data": bool(data_types),
    }


def redact_sensitive_text(text):
    """Replace sensitive values with labels that preserve the type of data."""
    if not text:
        return text

    redacted = text
    for data_type, pattern in SENSITIVE_PATTERNS.items():
        redacted = pattern.sub(REDACTION_LABELS[data_type], redacted)

    return redacted
