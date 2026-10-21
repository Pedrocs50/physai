from __future__ import annotations

import json
from pathlib import Path


def write_summary(payload: dict, output: str | None = None) -> str | None:
    """Escreve um resumo em JSON para execução reprodutível."""
    if output is None:
        return None
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(path)
