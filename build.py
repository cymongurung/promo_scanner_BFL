"""Build index.html from the daily stock Excel.  Usage: python build.py [file.xlsx]"""
import json, sys, pathlib, pandas as pd
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "naya_calculation.xlsx")
df = pd.read_excel(src, dtype={"Item No.": str, "Barcode": str, "Primary VPN": str})
df = df.dropna(subset=["Barcode"])
rows = []
for r in df.itertuples(index=False):
    d = dict(zip(df.columns, r))
    p = str(d["Item"]).split(":")
    vpn = str(d.get("Primary VPN") or p[0])
    color = p[1].split(".", 1)[-1] if len(p) > 3 else ""
    size = p[2] if len(p) > 3 else ""
    desc = ":".join(p[3:]) if len(p) > 3 else p[-1]
    rows.append([str(d["Department Brand"]), str(d["Subclass"]), vpn, color, size, desc,
                 str(d["Item No."]), str(d["Barcode"]).strip(), round(float(d["price"]), 2),
                 int(round(float(d["percentage"]) * 100)), round(float(d["final price"]), 2), int(d["SOH"])])
html = pathlib.Path(__file__).with_name("template.html").read_text(encoding="utf-8")
html = html.replace("__DATA__", json.dumps(rows, ensure_ascii=False, separators=(",", ":"))).replace("__SRC__", src.name)
pathlib.Path(__file__).with_name("index.html").write_text(html, encoding="utf-8")
print(f"{len(rows)} items -> index.html ({len(html)/1e6:.1f} MB)")
