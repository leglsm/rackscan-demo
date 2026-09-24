"""Embed data/sample.json into template.html -> index.html (single self-contained file)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "sample.json").read_text())
html = (ROOT / "template.html").read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
(ROOT / "index.html").write_text(html)
print(f"index.html {len(html)/1024:.1f} KB, {len(data['issues'])} issues")
