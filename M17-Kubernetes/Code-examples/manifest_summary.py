from __future__ import annotations

from pathlib import Path


def summarize_manifest(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    summary = {
        "file": path.name,
        "kind": "unknown",
        "name": "unknown",
    }
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("kind:"):
            summary["kind"] = stripped.split(":", 1)[1].strip()
        if stripped.startswith("name:") and summary["name"] == "unknown":
            summary["name"] = stripped.split(":", 1)[1].strip()
    return summary


if __name__ == "__main__":
    manifest_dir = Path(__file__).resolve().parents[1] / "Deployment-manifests"
    for manifest in sorted(manifest_dir.glob("*.yaml")):
        print(summarize_manifest(manifest))

