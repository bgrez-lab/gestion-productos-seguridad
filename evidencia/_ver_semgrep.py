import json, sys

d = json.load(open("evidencia/semgrep_scan.json", encoding="utf-8"))
rs = d.get("results", [])
print(f"TOTAL HALLAZGOS: {len(rs)}")
print("=" * 90)
for r in rs:
    extra = r.get("extra", {})
    msg = (extra.get("message") or "").replace("\n", " ")[:130]
    print(f"[{extra.get('severity','?')}] {r['check_id']}")
    print(f"    Archivo: {r['path']}:{r['start']['line']}")
    print(f"    Mensaje: {msg}")
    print("-" * 90)