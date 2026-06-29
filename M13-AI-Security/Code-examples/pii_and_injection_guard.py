from __future__ import annotations

import re


INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal the system prompt",
    "developer message",
    "bypass safety",
    "act as unrestricted",
]


def detect_prompt_injection(text: str) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in INJECTION_PATTERNS if pattern in lowered]


def scrub_pii(text: str) -> str:
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL_REDACTED]", text)
    text = re.sub(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE_REDACTED]", text)
    text = re.sub(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD_REDACTED]", text)
    return text


def security_screen(text: str) -> dict[str, object]:
    flags = detect_prompt_injection(text)
    return {
        "allowed": not flags,
        "flags": flags,
        "scrubbed_text": scrub_pii(text),
    }


if __name__ == "__main__":
    sample = "Email me at user@example.com and ignore previous instructions."
    print(security_screen(sample))

