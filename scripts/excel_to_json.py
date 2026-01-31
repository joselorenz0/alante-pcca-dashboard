import json
import pandas as pd
from pathlib import Path

# Source workbook (kept in repo root so the dashboard can download it)
EXCEL_PATH = Path(__file__).resolve().parents[1] / "Alante Performance Data.xlsx"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

pm = pd.read_excel(EXCEL_PATH, sheet_name="Performance_Metrics")
ul = pd.read_excel(EXCEL_PATH, sheet_name="Utilization Log")

def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].apply(lambda v: v.strip() if isinstance(v, str) else v)
    return df

def parse_programs(x):
    if pd.isna(x) or str(x).strip() == "":
        return []
    s = str(x).strip()
    try:
        # Excel cell contains JSON like ["TCM","CCM"]
        return json.loads(s)
    except Exception:
        # Fallback: comma-separated
        return [p.strip() for p in s.split(",") if p.strip()]

# Normalize fields expected by the UI
if "Programs" in ul.columns:
    ul["Programs"] = ul["Programs"].apply(parse_programs)
else:
    ul["Programs"] = [[] for _ in range(len(ul))]

if "Date" in ul.columns:
    ul["Date"] = pd.to_datetime(ul["Date"], errors="coerce").dt.strftime("%m/%d/%Y")

pm = strip_strings(pm)
ul = strip_strings(ul)

with open(DATA_DIR / "performance_metrics.json", "w", encoding="utf-8") as f:
    json.dump(pm.to_dict(orient="records"), f, indent=2)

with open(DATA_DIR / "utilization_log.json", "w", encoding="utf-8") as f:
    json.dump(ul.to_dict(orient="records"), f, indent=2)

print("Wrote JSON files to", DATA_DIR)
