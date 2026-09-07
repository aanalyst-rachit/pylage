from __future__ import annotations

CSS_FOUNDATION = """
*, *::before, *::after {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background-color: var(--color-background);
    color: var(--color-text);
}

body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.5;
}

button, input, textarea, select {
    font: inherit;
    box-sizing: border-box;
}

[hidden] {
    display: none !important;
}

table {
    border-collapse: collapse;
}

th,
td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid var(--color-border);
}

td {
    background-color: var(--color-background);
}

th {
    background-color: var(--color-surface-variant);
}

tbody tr:last-child td {
    border-bottom: none;
}

button:focus-visible,
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

button:disabled,
input:disabled,
textarea:disabled,
select:disabled {
    cursor: not-allowed;
    opacity: 0.6;
}

input[readonly],
textarea[readonly] {
    cursor: default;
}

input[type="checkbox"]:checked {
    accent-color: var(--color-primary);
}
"""

__all__ = ["CSS_FOUNDATION"]
