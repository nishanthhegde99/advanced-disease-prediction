#!/usr/bin/env python3
"""
Remove diseases, symptoms, and medicines that were added only in the expanded dataset.
Restores linkage tables to match the remaining baseline records.
"""

import sqlite3
import subprocess
import tempfile
from pathlib import Path

DB_PATH = "disease.db"
BASELINE_COMMIT = "e2c8d84"
EXPANDED_COMMIT = "3de88ac"


def _export_db(commit: str, dest: Path) -> None:
    data = subprocess.check_output(["git", "show", f"{commit}:disease.db"])
    dest.write_bytes(data)


def _names(conn: sqlite3.Connection, table: str) -> set[str]:
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM {table}")
    return {row[0] for row in cur.fetchall()}


def _delete_by_names(cur, table: str, names: set[str]) -> int:
    removed = 0
    for name in names:
        cur.execute(f"DELETE FROM {table} WHERE name = ?", (name,))
        removed += cur.rowcount
    return removed


def main():
    with tempfile.TemporaryDirectory() as tmp:
        baseline_path = Path(tmp) / "baseline.db"
        expanded_path = Path(tmp) / "expanded.db"
        _export_db(BASELINE_COMMIT, baseline_path)
        _export_db(EXPANDED_COMMIT, expanded_path)

        base = sqlite3.connect(baseline_path)
        exp = sqlite3.connect(expanded_path)

        remove_diseases = _names(exp, "disease") - _names(base, "disease")
        remove_symptoms = _names(exp, "symptom") - _names(base, "symptom")
        remove_medicines = _names(exp, "medicine") - _names(base, "medicine")
        base.close()
        exp.close()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    d = _delete_by_names(cur, "disease", remove_diseases)
    s = _delete_by_names(cur, "symptom", remove_symptoms)
    m = _delete_by_names(cur, "medicine", remove_medicines)

    cur.execute("""
        DELETE FROM disease_symptom
        WHERE disease_id NOT IN (SELECT id FROM disease)
           OR symptom_id NOT IN (SELECT id FROM symptom)
    """)
    orphan_ds = cur.rowcount

    cur.execute("""
        DELETE FROM disease_medicine
        WHERE disease_id NOT IN (SELECT id FROM disease)
           OR medicine_id NOT IN (SELECT id FROM medicine)
    """)
    orphan_dm = cur.rowcount

    conn.commit()

    diseases = cur.execute("SELECT COUNT(*) FROM disease").fetchone()[0]
    symptoms = cur.execute("SELECT COUNT(*) FROM symptom").fetchone()[0]
    medicines = cur.execute("SELECT COUNT(*) FROM medicine").fetchone()[0]
    ds_links = cur.execute("SELECT COUNT(*) FROM disease_symptom").fetchone()[0]
    dm_links = cur.execute("SELECT COUNT(*) FROM disease_medicine").fetchone()[0]
    conn.close()

    print("Removed expanded-only records:")
    print(f"  diseases: {d} (expected up to {len(remove_diseases)})")
    print(f"  symptoms: {s} (expected up to {len(remove_symptoms)})")
    print(f"  medicines: {m} (expected up to {len(remove_medicines)})")
    print(f"  cleaned orphan links: disease_symptom={orphan_ds}, disease_medicine={orphan_dm}")
    print("Current totals:")
    print(f"  diseases: {diseases}, symptoms: {symptoms}, medicines: {medicines}")
    print(f"  disease_symptom links: {ds_links}, disease_medicine links: {dm_links}")


if __name__ == "__main__":
    main()
