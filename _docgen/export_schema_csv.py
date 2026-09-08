"""Export the logical schema as a design CSV (not a SQL script)."""

import csv
from pathlib import Path
import model as M

out = Path(r"C:\Users\bwaly\Desktop\Group 20 Pharmacy-project\Pharmacy-POS\Database-Design\schema-columns.csv")
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Table", "Column", "Data Type", "PK", "FK", "Nullable", "Description"])
    for table, cols in M.TABLES.items():
        for c in cols:
            w.writerow([table, *c])
print(out)
