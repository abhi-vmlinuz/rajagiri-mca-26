#!/usr/bin/env python3
"""Replay Section A against the DB and capture the *real* output that the
record needs after sir's review:

  * every ALTER TABLE (questions 2-21)  ->  DESC <table> instead of "Table altered."
  * every INSERT      (questions 1-11)  ->  SELECT * FROM <table> instead of "1 row created."

The academic tables are dropped and rebuilt from A1_01 + A1_02_to_08, the 20
ALTERs are applied one by one (DESC captured after each), the DML statements
are replayed on the empty tables (SELECT * captured after each insert), and
A3_00_seed.sql restores the full dataset at the end.  The library tables used
by Section B are not touched.

Results land in tools/.section_a_capture.json, which the page generators read
so that a rebuild never needs the database again.

    python3 tools/capture_section_a.py
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(ROOT, "sql")
CACHE = os.path.join(ROOT, "tools", ".section_a_capture.json")

CONN = "mca/mca@localhost:1521/FREEPDB1"

sys.path.insert(0, os.path.join(ROOT, "tools"))
import gen_section_a_alter as ALTER  # noqa: E402
import gen_section_a_dml_sql as DML  # noqa: E402

TABLES = ["EVENT_REGISTRATION", "RESULT", "ENROLLMENT", "EVENT",
          "COURSE", "STUDENT", "FACULTY", "DEPARTMENT"]

# question -> table that DESC should be run against
DESC_TABLE = {
    2: "student", 3: "student", 4: "faculty", 5: "student", 6: "student",
    7: "student", 8: "course", 9: "student", 10: "faculty", 11: "faculty",
    12: "student", 13: "event", 14: "student", 15: "college_event",
    16: "event", 17: "department", 18: "department", 19: "department",
    20: "course", 21: "course",
}

# questions 11 and 12: prove the new CHECK constraint by trying to break it
VIOLATIONS = {
    11: "UPDATE faculty SET salary = -5000 WHERE faculty_id = 'F101';",
    12: "UPDATE student SET cgpa = 12 WHERE student_id = 'S101';",
}

STATUS_RE = re.compile(
    r"^(\d+ rows? (created|updated|deleted)\.|Table (altered|renamed)\.|"
    r"Commit complete\.|Savepoint created\.|Rollback complete\.)$")


def sqlplus(script):
    p = subprocess.run(
        ["podman", "exec", "-i", "oracledb", "sqlplus", "-S", CONN],
        input=script, capture_output=True, text=True)
    return (p.stdout + p.stderr).splitlines()


def read_sql(name):
    with open(os.path.join(SQL_DIR, name)) as f:
        return f.read()


def blocks(lines, tag):
    """Split sqlplus output on @@<tag>nn@@ markers -> {nn: [lines]}"""
    pat = re.compile(r"^@@([A-Z])(\d\d)@@$")
    out, cur = {}, None
    for line in lines:
        m = pat.match(line.strip())
        if m:
            if m.group(1) == tag:
                cur = m.group(2)
                out[cur] = []
            else:
                cur = None
        elif cur is not None:
            out[cur].append(line.rstrip())
    return out


def split_status(block):
    lines = [l for l in block if l.strip()]
    status = []
    while lines and STATUS_RE.match(lines[0].strip()):
        status.append(lines[0].strip())
        done = status[-1].startswith("Commit complete.")
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)
        if done:          # anything after a COMMIT belongs to the next script
            break
    return status, lines


def parse_rows(lines):
    rows = []
    for line in lines:
        if "rows selected." in line or "row selected." in line:
            continue
        if "~" not in line:
            continue
        fields = [c.strip() for c in line.split("~")]
        rows.append(fields)
    return rows


def select_of(stmt):
    """'SELECT a, b FROM t' -> (one-line statement, table, [A, B] or '*')."""
    flat = " ".join(stmt.split())
    m = re.match(r"SELECT\s+(.*?)\s+FROM\s+(\w+)", flat, re.I)
    sel = m.group(1).strip()
    cols = "*" if sel == "*" else [c.strip().upper() for c in sel.split(",")]
    return flat, m.group(2), cols


def column_info(lines):
    """'TABLE|COLUMN|DATATYPE' -> {table: [(column, datatype), ...]}"""
    cols = {}
    for line in lines:
        parts = [p.strip() for p in line.strip().split("|")]
        if len(parts) != 3:
            continue
        cols.setdefault(parts[0].lower(), []).append((parts[1], parts[2]))
    return cols


def main():
    cols = column_info(sqlplus(
        "SET HEADING OFF\nSET PAGESIZE 0\nSET FEEDBACK OFF\nSET LINESIZE 200\n"
        "SELECT table_name || '|' || column_name || '|' || data_type "
        "FROM user_tab_columns "
        "WHERE table_name IN (%s) ORDER BY table_name, column_id;\n"
        % ",".join("'%s'" % t for t in TABLES)))
    if not cols:
        print("could not read column names")
        sys.exit(1)

    script = ["SET LINESIZE 80", "SET PAGESIZE 5000", "SET NEWPAGE NONE",
              "SET FEEDBACK ON", "SET ECHO OFF", "SET VERIFY OFF", ""]
    for t in TABLES:
        script.append("DROP TABLE %s CASCADE CONSTRAINTS;" % t)
    script.append(read_sql("A1_01_department.sql"))
    script.append(read_sql("A1_02_to_08_tables.sql"))
    script.append("SET LINESIZE 80\nSET PAGESIZE 5000\nSET NEWPAGE NONE\n"
                  "SET FEEDBACK ON\nSET ECHO OFF")

    for num, _q, code, _out in ALTER.Q:
        script.append("PROMPT @@A%02d@@" % num)
        for stmt in code:
            script.append(stmt)
        if not any(s.strip().upper().startswith("DESC") for s in code):
            script.append("DESC %s;" % DESC_TABLE[num])

    # ---- DML phase: headings off, '~' as column separator -----------------
    script.append("SET HEADING OFF")
    script.append("SET LINESIZE 32767")
    script.append("SET COLSEP '~'")
    script.append("SET TRIMSPOOL ON")

    for num, _q, code, _out in DML.DML:
        script.append("PROMPT @@D%02d@@" % num)
        for stmt in code:
            script.append(stmt)
        post = DML.post_select(num, code)
        if post:
            script.append(post)
        script.append("COMMIT;")

    script.append(read_sql("A3_00_seed.sql"))
    for num, stmt in VIOLATIONS.items():
        script.append("PROMPT @@V%02d@@" % num)
        script.append(stmt)
    script.append("PROMPT @@Z99@@")

    out = sqlplus("\n".join(script) + "\n")
    ab, db, vb = blocks(out, "A"), blocks(out, "D"), blocks(out, "V")

    missing = [n for n, *_ in ALTER.Q if ("%02d" % n) not in ab] + \
              [n for n, *_ in DML.DML if ("%02d" % n) not in db]
    if missing:
        print("MISSING markers:", missing)
        print("\n".join(out[-40:]))
        sys.exit(1)

    cache = {"alter": {}, "dml": {}}

    for num, _q, code, _out in ALTER.Q:
        status, rest = split_status(ab["%02d" % num])
        bad = [l for l in rest if l.startswith("ORA-") or l.startswith("SP2-")]
        if bad:
            print("ALTER %d failed: %s" % (num, bad))
            sys.exit(1)
        cache["alter"]["%02d" % num] = {
            "status": status,
            "desc_sql": "DESC %s;" % DESC_TABLE[num],
            "desc": [l.expandtabs(8).rstrip() for l in rest if l.strip()]}

    for num, _q, code, _out in DML.DML:
        status, rest = split_status(db["%02d" % num])
        bad = [l for l in rest if l.startswith("ORA-") or l.startswith("SP2-")]
        if bad:
            print("DML %d failed: %s" % (num, bad))
            sys.exit(1)
        entry = {"status": status}
        post = DML.post_select(num, code)
        if post:
            sel, table, sel_cols = select_of(post)
            info = dict(cols.get(table.lower(), []))
            names = ([c for c, _t in cols.get(table.lower(), [])]
                     if sel_cols == "*" else sel_cols)
            entry["headers"] = names
            entry["types"] = [info[n] for n in names]
            entry["rows"] = parse_rows(rest)
        cache["dml"]["%02d" % num] = entry

    for num, stmt in VIOLATIONS.items():
        key = "%02d" % num
        lines = [l for l in vb.get(key, []) if l.strip()]
        if not any("ORA-" in l for l in lines):
            print("no constraint error captured for question", num)
            sys.exit(1)
        cache["alter"][key]["violation_sql"] = stmt
        cache["alter"][key]["violation"] = lines

    with open(CACHE, "w") as f:
        json.dump(cache, f, indent=1)

    for k in sorted(cache["alter"]):
        print("ALTER %s  %-16s desc=%d lines" %
              (k, " ".join(cache["alter"][k]["status"]),
               len(cache["alter"][k]["desc"])))
    for k in sorted(cache["dml"]):
        e = cache["dml"][k]
        print("DML   %s  %-16s rows=%s cols=%s" %
              (k, " ".join(e["status"]), len(e.get("rows", [])) or "-",
               len(e.get("headers", [])) or "-"))


if __name__ == "__main__":
    main()
