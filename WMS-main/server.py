#!/usr/bin/env python3
"""Andalusia Academy Work Management System — local prototype V4.

Uses only the Python standard library plus openpyxl.
Data is saved to:
  data/store.json
  data/andalusia_task_data.xlsx
"""

from __future__ import annotations

import csv
import io
import json
import mimetypes
import os
import re
import shutil
import sqlite3
import tempfile
import threading
import webbrowser
from datetime import date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from openpyxl import Workbook, load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.datetime import from_excel
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
STORE_PATH = DATA_DIR / "store.json"
DB_PATH = DATA_DIR / "andalusia_work_management.db"
EXCEL_PATH = DATA_DIR / "andalusia_task_data.xlsx"
LOGO_PATH = STATIC_DIR / "logo.png"
HOST = "127.0.0.1"
PORT = int(os.environ.get("ANDALUSIA_PORT", "8765"))

PRIMARY = "C17A62"
PRIMARY_DARK = "8F4F3B"
PRIMARY_LIGHT = "F3E4DF"
SAND = "E8D7C9"
CREAM = "FFF9F6"
INK = "55372F"
WHITE = "FFFFFF"
GREEN = "DCEBDD"
AMBER = "F7E5BF"
RED = "F5D2CC"
GRAY = "EFEAE7"

TASK_CATEGORIES = [
    "Curriculum Design", "Content Development", "Proposal & Documentation",
    "Slide & Material Production", "Video Recording & Editing", "Assessment Design",
    "Review & Quality Check", "Meetings & Coordination", "Delivery / Training",
    "Program Tracking & Monitoring", "Meetings with Client / Partner", "Administration",
]
VALID_STATUS = {"Not Started", "In Progress", "Completed", "On Hold", "Cancelled"}
VALID_PRIORITY = {"High", "Medium", "Low"}
VALID_IMPACT = {"High", "Medium", "Low"}
VALID_BLOCKER_STATUS = {"Open", "In Progress", "Resolved"}
DELIVERABLE_TYPES = [
    "Course Outline", "Session Plan", "Slide Deck", "Lab / Exercise", "Assessment",
    "Proposal", "Recorded Video", "Report", "Web Page", "Other",
]
VALID_DELIVERY_STATUS = {"Not Started", "Running", "On Hold", "Completed"}
VALID_ACTION_STATUS = {"Open", "In Progress", "Done"}
VALID_NOTIFICATION_STATUS = {"Not Scheduled", "Scheduled", "Sent", "Read", "Failed"}
VALID_RECURRENCE = {"None", "Daily", "Weekly", "Monthly", "Quarterly"}

SAMPLE_TASKS = [
    {
        "id": 1, "title": "Prepare weekly lesson plan", "project": "Academic",
        "priority": "High", "status": "In Progress", "start": "2026-08-02",
        "due": "2026-08-06", "progress": 75, "est": 8, "actual": 6,
        "day": "Sunday", "recurrence": "Weekly", "notes": "Coordinate subject plans."
    },
    {
        "id": 2, "title": "Update student attendance report", "project": "Academic",
        "priority": "Medium", "status": "Completed", "start": "2026-08-02",
        "due": "2026-08-03", "progress": 100, "est": 4, "actual": 4,
        "day": "Monday", "recurrence": "Weekly", "notes": "Validate late submissions."
    },
    {
        "id": 3, "title": "Design social media campaign", "project": "Marketing",
        "priority": "High", "status": "In Progress", "start": "2026-08-04",
        "due": "2026-08-12", "progress": 45, "est": 12, "actual": 5,
        "day": "Tuesday", "recurrence": "Monthly", "notes": "Back-to-school campaign."
    },
    {
        "id": 4, "title": "Review IT support tickets", "project": "IT",
        "priority": "High", "status": "Not Started", "start": "2026-08-05",
        "due": "2026-08-06", "progress": 20, "est": 6, "actual": 1,
        "day": "Wednesday", "recurrence": "Daily", "notes": "Prioritize classroom issues."
    },
    {
        "id": 5, "title": "Facilities inspection", "project": "Operations",
        "priority": "Medium", "status": "Not Started", "start": "2026-08-06",
        "due": "2026-08-10", "progress": 0, "est": 5, "actual": 0,
        "day": "Thursday", "recurrence": "Monthly", "notes": "Inspect safety and maintenance."
    },
    {
        "id": 6, "title": "Quarterly academic performance review", "project": "Academic",
        "priority": "High", "status": "In Progress", "start": "2026-07-15",
        "due": "2026-09-15", "progress": 60, "est": 30, "actual": 18,
        "day": "Sunday", "recurrence": "Quarterly", "notes": "Review academic KPIs."
    },
    {
        "id": 7, "title": "Parent communication newsletter", "project": "Marketing",
        "priority": "Medium", "status": "On Hold", "start": "2026-08-01",
        "due": "2026-08-20", "progress": 30, "est": 10, "actual": 3,
        "day": "Wednesday", "recurrence": "Monthly", "notes": "Awaiting final announcements."
    },
]


SAMPLE_TASK_ENRICHMENTS = {
    1: {"category": "Curriculum Design", "impact": "High", "blockerStatus": "", "deliverableType": "Course Outline", "deliveryStatus": "Running", "actionStatus": "In Progress"},
    2: {"category": "Program Tracking & Monitoring", "impact": "Medium", "blockerStatus": "", "deliverableType": "Report", "deliveryStatus": "Completed", "actionStatus": "Done"},
    3: {"category": "Slide & Material Production", "impact": "High", "blockerStatus": "", "deliverableType": "Slide Deck", "deliveryStatus": "Running", "actionStatus": "In Progress"},
    4: {"category": "Program Tracking & Monitoring", "impact": "High", "blockerStatus": "Open", "deliverableType": "Report", "deliveryStatus": "Not Started", "actionStatus": "Open"},
    5: {"category": "Review & Quality Check", "impact": "Medium", "blockerStatus": "", "deliverableType": "Report", "deliveryStatus": "Not Started", "actionStatus": "Open"},
    6: {"category": "Program Tracking & Monitoring", "impact": "High", "blockerStatus": "", "deliverableType": "Report", "deliveryStatus": "Running", "actionStatus": "In Progress"},
    7: {"category": "Meetings with Client / Partner", "impact": "Medium", "blockerStatus": "Open", "deliverableType": "Proposal", "deliveryStatus": "On Hold", "actionStatus": "Open"},
}
for sample_task in SAMPLE_TASKS:
    sample_task.update(SAMPLE_TASK_ENRICHMENTS.get(sample_task["id"], {}))

STORE_LOCK = threading.Lock()


def new_store(user=None, tasks=None, programs=None, assignments=None, notifications=None, audit=None, documents=None, master_data=None, settings=None, rule_overrides=None):
    return {
        "version": 5,
        "product": "Andalusia Academy Work Management System",
        "user": user,
        "tasks": list(tasks if tasks is not None else []),
        "programs": list(programs if programs is not None else []),
        "assignments": list(assignments if assignments is not None else []),
        "notifications": list(notifications if notifications is not None else []),
        "audit": list(audit if audit is not None else []),
        "documents": list(documents if documents is not None else []),
        "masterData": dict(master_data if isinstance(master_data, dict) else {}),
        "settings": dict(settings if isinstance(settings, dict) else {}),
        "ruleOverrides": dict(rule_overrides if isinstance(rule_overrides, dict) else {}),
        "updatedAt": datetime.now().isoformat(timespec="seconds"),
    }


def safe_date(value, fallback=None):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, (int, float)):
        try:
            return from_excel(value).date()
        except Exception:
            return fallback
    if value is None or value == "":
        return fallback
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%d %b %Y", "%d-%b-%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except Exception:
        return fallback


def iso_date(value, fallback=None):
    parsed = safe_date(value, fallback)
    return parsed.isoformat() if parsed else ""


def workday_name(due_iso):
    parsed = safe_date(due_iso, date.today())
    name = parsed.strftime("%A")
    return name if name in {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"} else "Thursday"


def number(value, default=0.0):
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace("%", "").replace(",", "")
    try:
        return float(text)
    except ValueError:
        return default


def normalize_task(task, fallback_id):
    start = iso_date(task.get("start") or task.get("Start Date"), date.today())
    due = iso_date(task.get("due") or task.get("Due Date"), safe_date(start, date.today()))
    progress = number(task.get("progress", task.get("Progress %", 0)))
    if 0 <= progress <= 1:
        progress *= 100
    status = str(task.get("status", task.get("Status", "Not Started")) or "Not Started").strip()
    priority = str(task.get("priority", task.get("Priority", "Medium")) or "Medium").strip()
    category = str(task.get("category", task.get("Task Category", task.get("Category", ""))) or "").strip()
    impact = str(task.get("impact", task.get("Impact", "")) or "").strip()
    blocker_status = str(task.get("blockerStatus", task.get("Blocker Status", "")) or "").strip()
    deliverable_type = str(task.get("deliverableType", task.get("Deliverable Type", "")) or "").strip()
    delivery_status = str(task.get("deliveryStatus", task.get("Delivery Status", "")) or "").strip()
    action_status = str(task.get("actionStatus", task.get("Action Status", "")) or "").strip()
    notification_status = str(task.get("notificationStatus", task.get("Notification Status", "Not Scheduled")) or "Not Scheduled").strip()
    recurrence = str(task.get("recurrence", task.get("Recurrence", "None")) or "None").strip()
    if status not in VALID_STATUS:
        status = "Not Started"
    if priority == "Critical":
        priority = "High"
    elif priority not in VALID_PRIORITY:
        priority = "Medium"
    if category and category not in TASK_CATEGORIES:
        category = ""
    if impact and impact not in VALID_IMPACT:
        impact = ""
    if blocker_status and blocker_status not in VALID_BLOCKER_STATUS:
        blocker_status = ""
    if deliverable_type and deliverable_type not in DELIVERABLE_TYPES:
        deliverable_type = ""
    if delivery_status and delivery_status not in VALID_DELIVERY_STATUS:
        delivery_status = ""
    if action_status and action_status not in VALID_ACTION_STATUS:
        action_status = ""
    if notification_status not in VALID_NOTIFICATION_STATUS:
        notification_status = "Not Scheduled"
    if recurrence not in VALID_RECURRENCE:
        recurrence = "None"
    if status == "Completed":
        progress = 100
    raw_id = task.get("id", task.get("Task ID", fallback_id))
    try:
        task_id = int(raw_id)
    except (TypeError, ValueError):
        match = re.search(r"(\d+)", str(raw_id))
        task_id = int(match.group(1)) if match else fallback_id
    return {
        "id": task_id,
        "title": str(task.get("title", task.get("Task Name", task.get("Title", ""))) or "").strip(),
        "project": str(task.get("project", task.get("Project", "General")) or "General").strip(),
        "category": category,
        "priority": priority,
        "status": status,
        "impact": impact,
        "blockerStatus": blocker_status,
        "deliverableType": deliverable_type,
        "deliveryStatus": delivery_status,
        "actionStatus": action_status,
        "notificationStatus": notification_status,
        "start": start,
        "due": due,
        "progress": max(0, min(100, round(progress, 2))),
        "est": round(number(task.get("est", task.get("Estimated Hours", 0))), 2),
        "actual": round(number(task.get("actual", task.get("Actual Hours", 0))), 2),
        "day": workday_name(due),
        "recurrence": recurrence,
        "link": str(task.get("link", task.get("Link", task.get("URL", ""))) or "").strip(),
        "notes": str(task.get("notes", task.get("Notes", "")) or "").strip(),
        "taskType": str(task.get("taskType", "Manual") or "Manual"),
        "programId": str(task.get("programId", "") or ""),
        "stage": str(task.get("stage", "") or ""),
        "assignmentId": str(task.get("assignmentId", "") or ""),
        "positionContext": str(task.get("positionContext", "") or ""),
    }


def normalize_store(payload):
    payload = payload if isinstance(payload, dict) else {}
    user = payload.get("user")
    raw_tasks = payload.get("tasks", [])
    tasks = []
    used_ids = set()
    next_id = 1
    for raw in raw_tasks if isinstance(raw_tasks, list) else []:
        task = normalize_task(raw if isinstance(raw, dict) else {}, next_id)
        if not task["title"]:
            continue
        while task["id"] in used_ids:
            task["id"] += 1
        used_ids.add(task["id"])
        next_id = max(next_id, task["id"] + 1)
        tasks.append(task)

    def clean_records(name):
        rows = payload.get(name, [])
        return [dict(row) for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []

    return new_store(
        user=user if isinstance(user, dict) else None,
        tasks=tasks,
        programs=clean_records("programs"),
        assignments=clean_records("assignments"),
        notifications=clean_records("notifications"),
        audit=clean_records("audit"),
        documents=clean_records("documents"),
        master_data=payload.get("masterData") if isinstance(payload.get("masterData"), dict) else {},
        settings=payload.get("settings") if isinstance(payload.get("settings"), dict) else {},
        rule_overrides=payload.get("ruleOverrides") if isinstance(payload.get("ruleOverrides"), dict) else {},
    )


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY CHECK(id = 1),
        data TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        status TEXT,
        due TEXT,
        program_id TEXT,
        assignment_id TEXT,
        data TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_tasks_status_due ON tasks(status, due);
    CREATE INDEX IF NOT EXISTS idx_tasks_program ON tasks(program_id);
    CREATE TABLE IF NOT EXISTS programs (
        id TEXT PRIMARY KEY,
        status TEXT,
        start_date TEXT,
        end_date TEXT,
        data TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS assignments (
        id TEXT PRIMARY KEY,
        program_id TEXT,
        owner_position TEXT,
        status TEXT,
        due TEXT,
        kind TEXT,
        data TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_assignments_owner_status ON assignments(owner_position, status);
    CREATE INDEX IF NOT EXISTS idx_assignments_program ON assignments(program_id);
    CREATE TABLE IF NOT EXISTS notifications (
        id TEXT PRIMARY KEY,
        target_position TEXT,
        is_read INTEGER NOT NULL DEFAULT 0,
        created_at TEXT,
        data TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_notifications_position_read ON notifications(target_position, is_read);
    CREATE TABLE IF NOT EXISTS audit (
        id TEXT PRIMARY KEY,
        program_id TEXT,
        at TEXT,
        data TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_audit_program_at ON audit(program_id, at);
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        program_id TEXT,
        stage TEXT,
        document_type TEXT,
        created_at TEXT,
        data TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_documents_program_stage ON documents(program_id, stage);
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        data TEXT NOT NULL
    );
    """)
    return conn


def db_has_state(conn):
    row = conn.execute("SELECT COUNT(*) FROM programs").fetchone()[0]
    task_count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    profile_count = conn.execute("SELECT COUNT(*) FROM profile").fetchone()[0]
    config_count = conn.execute("SELECT COUNT(*) FROM config").fetchone()[0]
    return bool(row or task_count or profile_count or config_count)


def load_store_from_db(conn):
    profile_row = conn.execute("SELECT data FROM profile WHERE id=1").fetchone()
    user = json.loads(profile_row[0]) if profile_row else None
    def load_rows(table, order="rowid"):
        return [json.loads(row[0]) for row in conn.execute(f"SELECT data FROM {table} ORDER BY {order}").fetchall()]
    config = {key: json.loads(data) for key, data in conn.execute("SELECT key, data FROM config").fetchall()}
    return normalize_store({
        "user": user,
        "tasks": load_rows("tasks", "due, id"),
        "programs": load_rows("programs", "rowid DESC"),
        "assignments": load_rows("assignments", "rowid DESC"),
        "notifications": load_rows("notifications", "rowid DESC"),
        "audit": load_rows("audit", "at DESC"),
        "documents": load_rows("documents", "rowid DESC"),
        "masterData": config.get("masterData", {}),
        "settings": config.get("settings", {}),
        "ruleOverrides": config.get("ruleOverrides", {}),
    })


def write_store_to_db(conn, store):
    normalized = normalize_store(store)
    with conn:
        conn.execute("DELETE FROM profile")
        if normalized.get("user"):
            conn.execute("INSERT INTO profile(id, data) VALUES(1, ?)", (json.dumps(normalized["user"], ensure_ascii=False),))
        for table in ("tasks", "programs", "assignments", "notifications", "audit", "documents"):
            conn.execute(f"DELETE FROM {table}")
        for task in normalized["tasks"]:
            conn.execute("INSERT INTO tasks(id,status,due,program_id,assignment_id,data) VALUES(?,?,?,?,?,?)", (
                int(task["id"]), task.get("status", ""), task.get("due", ""), task.get("programId", ""), task.get("assignmentId", ""), json.dumps(task, ensure_ascii=False)
            ))
        for program in normalized["programs"]:
            pid = str(program.get("id") or f"PRG-{abs(hash(json.dumps(program, sort_keys=True))) % 100000}")
            program["id"] = pid
            status = program.get("status") or ""
            conn.execute("INSERT INTO programs(id,status,start_date,end_date,data) VALUES(?,?,?,?,?)", (
                pid, status, program.get("startDate", ""), program.get("endDate", ""), json.dumps(program, ensure_ascii=False)
            ))
        for item in normalized["assignments"]:
            iid = str(item.get("id") or f"ASN-{abs(hash(json.dumps(item, sort_keys=True))) % 100000}")
            item["id"] = iid
            conn.execute("INSERT INTO assignments(id,program_id,owner_position,status,due,kind,data) VALUES(?,?,?,?,?,?,?)", (
                iid, item.get("programId", ""), item.get("ownerPosition", ""), item.get("status", ""), item.get("due", ""), item.get("kind", ""), json.dumps(item, ensure_ascii=False)
            ))
        for item in normalized["notifications"]:
            iid = str(item.get("id") or f"NTF-{abs(hash(json.dumps(item, sort_keys=True))) % 100000}")
            item["id"] = iid
            conn.execute("INSERT INTO notifications(id,target_position,is_read,created_at,data) VALUES(?,?,?,?,?)", (
                iid, item.get("targetPosition", ""), 1 if item.get("read") else 0, item.get("createdAt", ""), json.dumps(item, ensure_ascii=False)
            ))
        for item in normalized["audit"]:
            iid = str(item.get("id") or f"AUD-{abs(hash(json.dumps(item, sort_keys=True))) % 100000}")
            item["id"] = iid
            conn.execute("INSERT INTO audit(id,program_id,at,data) VALUES(?,?,?,?)", (
                iid, item.get("programId", ""), item.get("at", ""), json.dumps(item, ensure_ascii=False)
            ))
        for item in normalized["documents"]:
            iid = str(item.get("id") or f"DOC-{abs(hash(json.dumps(item, sort_keys=True))) % 100000}")
            item["id"] = iid
            conn.execute("INSERT INTO documents(id,program_id,stage,document_type,created_at,data) VALUES(?,?,?,?,?,?)", (
                iid, item.get("programId", ""), item.get("stage", ""), item.get("type", ""), item.get("createdAt", ""), json.dumps(item, ensure_ascii=False)
            ))
        conn.execute("DELETE FROM config")
        for key in ("masterData", "settings", "ruleOverrides"):
            conn.execute("INSERT INTO config(key,data) VALUES(?,?)", (key, json.dumps(normalized.get(key, {}), ensure_ascii=False)))
    return normalized


def load_store():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = init_db()
    try:
        if db_has_state(conn):
            return load_store_from_db(conn)
        if STORE_PATH.exists():
            try:
                initial = normalize_store(json.loads(STORE_PATH.read_text(encoding="utf-8")))
            except Exception:
                backup = STORE_PATH.with_suffix(".invalid.json")
                shutil.copy2(STORE_PATH, backup)
                initial = new_store()
        else:
            initial = new_store()
        write_store_to_db(conn, initial)
        return initial
    finally:
        conn.close()


def save_store(store):
    normalized = normalize_store(store)
    normalized["updatedAt"] = datetime.now().isoformat(timespec="seconds")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with STORE_LOCK:
        conn = init_db()
        try:
            normalized = write_store_to_db(conn, normalized)
        finally:
            conn.close()
        # Human-readable backup snapshot remains intentionally available.
        temp_path = STORE_PATH.with_suffix(".tmp")
        temp_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")
        temp_path.replace(STORE_PATH)
        # Personal task Excel mirror is kept for continuity with the existing planner.
        write_excel_file(normalized, EXCEL_PATH)
    return normalized


def sunday_of_week(d):
    return d - timedelta(days=(d.weekday() + 1) % 7)


def active_in_period(task, start_date, end_date):
    task_start = safe_date(task.get("start"), start_date)
    task_due = safe_date(task.get("due"), task_start)
    return task_start <= end_date and task_due >= start_date


def style_header_row(ws, row, start_col, end_col):
    fill = PatternFill("solid", fgColor=PRIMARY_DARK)
    font = Font(color=WHITE, bold=True)
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 28


def add_title(ws, title, subtitle):
    ws.merge_cells("C1:N2")
    ws["C1"] = title
    ws["C1"].fill = PatternFill("solid", fgColor=PRIMARY)
    ws["C1"].font = Font(color=WHITE, bold=True, size=20)
    ws["C1"].alignment = Alignment(vertical="center")
    ws.merge_cells("C3:N3")
    ws["C3"] = subtitle
    ws["C3"].fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
    ws["C3"].font = Font(color=INK, italic=True, size=10)
    if LOGO_PATH.exists():
        try:
            from openpyxl.drawing.image import Image
            img = Image(str(LOGO_PATH))
            img.width = 78
            img.height = 78
            ws.add_image(img, "A1")
        except Exception:
            pass


def add_profile_sheet(wb, store):
    ws = wb.create_sheet("Employee Profile")
    add_title(ws, "Employee Profile", "Local employee information used by exported reports.")
    user = store.get("user") or {}
    rows = [
        ("Full Name", user.get("name", "")),
        ("Employee ID", user.get("employeeId", "")),
        ("Academy Email", user.get("email", "")),
        ("Department", user.get("department", "")),
        ("Job Title", user.get("jobTitle", "")),
        ("Phone", user.get("phone", "")),
        ("Working Week", "Sunday–Thursday"),
        ("Last Saved", store.get("updatedAt", "")),
    ]
    ws.append([])
    ws.append(["Field", "Value"])
    style_header_row(ws, 5, 1, 2)
    for key, value in rows:
        ws.append([key, value])
    for row in range(6, 6 + len(rows)):
        ws.cell(row, 1).fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
        ws.cell(row, 1).font = Font(color=INK, bold=True)
        ws.cell(row, 2).fill = PatternFill("solid", fgColor=CREAM)
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 42
    ws.freeze_panes = "A6"
    return ws


def add_overview_sheet(wb, store):
    ws = wb.create_sheet("Overview")
    add_title(ws, "Task Planner Overview", "A clear summary of workload, progress, deadlines, and exported report contents.")
    user = store.get("user") or {}
    task_list = store.get("tasks", [])
    today = date.today()
    week_start = sunday_of_week(today)
    week_end = week_start + timedelta(days=4)

    total = len(task_list)
    completed = sum(t.get("status") == "Completed" for t in task_list)
    in_progress = sum(t.get("status") == "In Progress" for t in task_list)
    overdue = sum(
        t.get("status") not in ("Completed", "Cancelled")
        and safe_date(t.get("due"), today) < today
        for t in task_list
    )
    estimated = sum(float(t.get("est", 0) or 0) for t in task_list)
    actual = sum(float(t.get("actual", 0) or 0) for t in task_list)
    rate = completed / total if total else 0
    current_week = [t for t in task_list if active_in_period(t, week_start, week_end)]

    ws["A5"] = "Employee"
    ws["B5"] = user.get("name", "")
    ws["D5"] = "Employee ID"
    ws["E5"] = user.get("employeeId", "")
    ws["G5"] = "Department"
    ws["H5"] = user.get("department", "")
    ws["J5"] = "Generated"
    ws["K5"] = today
    ws["K5"].number_format = "dd-mmm-yyyy"
    for cell in ("A5", "D5", "G5", "J5"):
        ws[cell].fill = PatternFill("solid", fgColor=PRIMARY_DARK)
        ws[cell].font = Font(color=WHITE, bold=True)
        ws[cell].alignment = Alignment(horizontal="center")
    for cell in ("B5", "E5", "H5", "K5"):
        ws[cell].fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
        ws[cell].font = Font(color=INK, bold=True)

    kpis = [
        ("Total Tasks", total), ("Completed", completed), ("In Progress", in_progress),
        ("Overdue", overdue), ("Completion Rate", rate), ("Estimated Hours", estimated),
        ("Actual Hours", actual), ("Remaining Hours", max(estimated - actual, 0)),
    ]
    positions = [(1,7),(4,7),(7,7),(10,7),(1,10),(4,10),(7,10),(10,10)]
    for (label, value), (col, row) in zip(kpis, positions):
        label_cell = ws.cell(row=row, column=col)
        value_cell = ws.cell(row=row+1, column=col)
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col+1)
        ws.merge_cells(start_row=row+1, start_column=col, end_row=row+1, end_column=col+1)
        label_cell.value = label
        label_cell.fill = PatternFill("solid", fgColor=PRIMARY_DARK)
        label_cell.font = Font(color=WHITE, bold=True)
        label_cell.alignment = Alignment(horizontal="center")
        value_cell.value = value
        value_cell.fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
        value_cell.font = Font(color=PRIMARY_DARK, bold=True, size=17)
        value_cell.alignment = Alignment(horizontal="center")
        if label == "Completion Rate":
            value_cell.number_format = "0%"

    ws.merge_cells("A13:F13")
    ws["A13"] = f"CURRENT WORKWEEK · {week_start.strftime('%d %b')}–{week_end.strftime('%d %b %Y')}"
    ws["A13"].fill = PatternFill("solid", fgColor=PRIMARY)
    ws["A13"].font = Font(color=WHITE, bold=True, size=11)
    week_headers = ["Task", "Project", "Priority", "Status", "Due", "Progress"]
    for index, header in enumerate(week_headers, 1):
        ws.cell(row=14, column=index, value=header)
    style_header_row(ws, 14, 1, len(week_headers))
    for task in sorted(current_week, key=lambda item: (item.get("due", ""), item.get("title", "")))[:10]:
        ws.append([
            task.get("title", ""), task.get("project", ""), task.get("priority", ""),
            task.get("status", ""), safe_date(task.get("due"), today),
            float(task.get("progress", 0) or 0) / 100,
        ])
    for row in range(15, ws.max_row + 1):
        ws.cell(row, 5).number_format = "dd-mmm-yyyy"
        ws.cell(row, 6).number_format = "0%"
        for col in range(1, 7):
            ws.cell(row, col).fill = PatternFill("solid", fgColor=CREAM)
            ws.cell(row, col).alignment = Alignment(vertical="top", wrap_text=True)

    status_start = max(ws.max_row + 3, 27)
    ws.merge_cells(start_row=status_start, start_column=1, end_row=status_start, end_column=3)
    ws.cell(status_start, 1, "STATUS SUMMARY")
    ws.cell(status_start, 1).fill = PatternFill("solid", fgColor=PRIMARY)
    ws.cell(status_start, 1).font = Font(color=WHITE, bold=True)
    ws.cell(status_start + 1, 1, "Status")
    ws.cell(status_start + 1, 2, "Tasks")
    ws.cell(status_start + 1, 3, "Share")
    style_header_row(ws, status_start + 1, 1, 3)
    status_rows = [
        ("Not Started", sum(t.get("status") == "Not Started" for t in task_list)),
        ("In Progress", in_progress),
        ("Completed", completed),
        ("On Hold", sum(t.get("status") == "On Hold" for t in task_list)),
        ("Cancelled", sum(t.get("status") == "Cancelled" for t in task_list)),
        ("Overdue", overdue),
    ]
    for offset, (label, count) in enumerate(status_rows, 2):
        ws.cell(status_start + offset, 1, label)
        ws.cell(status_start + offset, 2, count)
        ws.cell(status_start + offset, 3, count / total if total else 0)
        ws.cell(status_start + offset, 3).number_format = "0%"
        for col in range(1, 4):
            ws.cell(status_start + offset, col).fill = PatternFill("solid", fgColor=CREAM)

    projects = sorted({str(t.get("project", "")).strip() for t in task_list if str(t.get("project", "")).strip()})
    project_start = status_start
    ws.merge_cells(start_row=project_start, start_column=5, end_row=project_start, end_column=9)
    ws.cell(project_start, 5, "PROJECT WORKLOAD")
    ws.cell(project_start, 5).fill = PatternFill("solid", fgColor=PRIMARY)
    ws.cell(project_start, 5).font = Font(color=WHITE, bold=True)
    project_headers = ["Project", "Tasks", "Completed", "Est. Hrs", "Actual Hrs"]
    for index, header in enumerate(project_headers, 5):
        ws.cell(project_start + 1, index, header)
    style_header_row(ws, project_start + 1, 5, 9)
    for offset, project in enumerate(projects[:12], 2):
        items = [t for t in task_list if t.get("project") == project]
        row = project_start + offset
        ws.cell(row, 5, project)
        ws.cell(row, 6, len(items))
        ws.cell(row, 7, sum(t.get("status") == "Completed" for t in items))
        ws.cell(row, 8, sum(float(t.get("est", 0) or 0) for t in items))
        ws.cell(row, 9, sum(float(t.get("actual", 0) or 0) for t in items))
        for col in range(5, 10):
            ws.cell(row, col).fill = PatternFill("solid", fgColor=CREAM)

    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Tasks by Status"
    chart.height = 7
    chart.width = 12
    data = Reference(ws, min_col=2, min_row=status_start + 1, max_row=status_start + 1 + len(status_rows))
    cats = Reference(ws, min_col=1, min_row=status_start + 2, max_row=status_start + 1 + len(status_rows))
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.legend = None
    ws.add_chart(chart, f"K{status_start}")

    guide_row = max(status_start + max(len(status_rows), len(projects[:12])) + 4, 43)
    ws.merge_cells(start_row=guide_row, start_column=1, end_row=guide_row, end_column=14)
    ws.cell(guide_row, 1, "HOW TO USE THIS EXPORT")
    ws.cell(guide_row, 1).fill = PatternFill("solid", fgColor=PRIMARY_DARK)
    ws.cell(guide_row, 1).font = Font(color=WHITE, bold=True, size=11)
    instructions = [
        "1. Start with Overview for the main workload and performance summary.",
        "2. Use Tasks for the complete editable task register, links, dates, progress, and hours.",
        "3. Weekly, Monthly, and Quarterly Report sheets are formatted for management review and PDF printing.",
        "4. Update only the task register when importing the workbook back into the application.",
        "5. Common task fields include inline dropdowns; no Lists or hidden validation sheet is included.",
    ]
    for offset, text in enumerate(instructions, 1):
        ws.merge_cells(start_row=guide_row + offset, start_column=1, end_row=guide_row + offset, end_column=14)
        cell = ws.cell(guide_row + offset, 1, text)
        cell.fill = PatternFill("solid", fgColor=PRIMARY_LIGHT if offset % 2 else CREAM)
        cell.font = Font(color=INK)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[guide_row + offset].height = 25

    widths = {"A":28,"B":14,"C":14,"D":4,"E":24,"F":12,"G":14,"H":13,"I":13,"J":15,"K":15,"L":14,"M":14,"N":14}
    for column, width in widths.items():
        ws.column_dimensions[column].width = width
    ws.freeze_panes = "A7"
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return ws


TASK_HEADERS = [
    "Task ID", "Task Name", "Project", "Task Category", "Deliverable Type",
    "Priority", "Status", "Start Date", "Due Date", "Progress %",
    "Estimated Hours", "Actual Hours", "Variance", "Recurrence", "Link", "Notes"
]


def add_tasks_sheet(wb, store):
    ws = wb.create_sheet("Tasks")
    add_title(ws, "Task Register", "Edit task details here or import this sheet back into the application.")
    ws["A4"] = "Tip: use filters in the header row. Status, priority, deliverable type, and recurrence include dropdowns."
    ws.merge_cells("A4:P4")
    ws["A4"].fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
    ws["A4"].font = Font(color=INK, italic=True)
    ws["A4"].alignment = Alignment(wrap_text=True)

    for column, header in enumerate(TASK_HEADERS, 1):
        ws.cell(row=5, column=column, value=header)
    style_header_row(ws, 5, 1, len(TASK_HEADERS))

    for task in store.get("tasks", []):
        row = ws.max_row + 1
        ws.append([
            f"TSK-{int(task['id']):04d}", task.get("title", ""), task.get("project", ""),
            task.get("category", ""), task.get("deliverableType", ""), task.get("priority", ""),
            task.get("status", ""), safe_date(task.get("start")), safe_date(task.get("due")),
            float(task.get("progress", 0) or 0) / 100, float(task.get("est", 0) or 0),
            float(task.get("actual", 0) or 0), None, task.get("recurrence", "None"),
            task.get("link", ""), task.get("notes", ""),
        ])
        ws.cell(row, 13, f"=L{row}-K{row}")

    for row in range(6, ws.max_row + 1):
        ws.cell(row, 8).number_format = "dd-mmm-yyyy"
        ws.cell(row, 9).number_format = "dd-mmm-yyyy"
        ws.cell(row, 10).number_format = "0%"
        ws.cell(row, 11).number_format = "0.0"
        ws.cell(row, 12).number_format = "0.0"
        ws.cell(row, 13).number_format = "0.0"
        for col in range(1, len(TASK_HEADERS) + 1):
            ws.cell(row, col).fill = PatternFill("solid", fgColor=CREAM if col != 1 else GRAY)
            ws.cell(row, col).alignment = Alignment(vertical="top", wrap_text=col in (2, 4, 5, 16))
        link_cell = ws.cell(row, 15)
        if link_cell.value:
            link_cell.hyperlink = str(link_cell.value)
            link_cell.style = "Hyperlink"

    if ws.max_row >= 6:
        table = Table(displayName="TasksTable", ref=f"A5:P{ws.max_row}")
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2", showRowStripes=True,
            showFirstColumn=False, showLastColumn=False
        )
        ws.add_table(table)

    widths = [14,34,18,28,22,13,16,15,15,12,16,14,14,14,34,40]
    for index, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(index)].width = width

    ws.freeze_panes = "B6"
    ws.auto_filter.ref = f"A5:P{max(ws.max_row,5)}"
    ws.sheet_view.showGridLines = False

    red_fill = PatternFill("solid", fgColor=RED)
    green_fill = PatternFill("solid", fgColor=GREEN)
    amber_fill = PatternFill("solid", fgColor=AMBER)
    ws.conditional_formatting.add(f"G6:G{max(ws.max_row,6)}", FormulaRule(formula=['G6="Completed"'], fill=green_fill))
    ws.conditional_formatting.add(f"G6:G{max(ws.max_row,6)}", FormulaRule(formula=['G6="On Hold"'], fill=amber_fill))
    ws.conditional_formatting.add(f"G6:G{max(ws.max_row,6)}", FormulaRule(formula=['AND(G6<>"Completed",G6<>"Cancelled",I6<TODAY())'], fill=red_fill))

    validations = [
        ("E6:E1005", '"Course Outline,Session Plan,Slide Deck,Lab / Exercise,Assessment,Proposal,Recorded Video,Report,Web Page,Other"'),
        ("F6:F1005", '"High,Medium,Low"'),
        ("G6:G1005", '"Not Started,In Progress,Completed,On Hold,Cancelled"'),
        ("N6:N1005", '"None,Daily,Weekly,Monthly,Quarterly"'),
    ]
    for target, formula in validations:
        validation = DataValidation(type="list", formula1=formula, allow_blank=True)
        ws.add_data_validation(validation)
        validation.add(target)

    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return ws


def report_tasks(store, start_date, end_date):
    return [t for t in store.get("tasks", []) if active_in_period(t, start_date, end_date)]


def add_report_sheet(wb, store, name, start_date, end_date, report_type):
    ws = wb.create_sheet(name)
    subtitle = f"{start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')}"
    add_title(ws, f"{report_type} Task Report", subtitle)
    user = store.get("user") or {}
    ws["A5"], ws["C5"], ws["G5"], ws["I5"], ws["L5"], ws["N5"] = (
        "Employee", user.get("name", ""), "Employee ID", user.get("employeeId", ""),
        "Generated", date.today()
    )
    ws["A6"], ws["C6"], ws["G6"], ws["I6"], ws["L6"], ws["N6"] = (
        "Department", user.get("department", ""), "Job Title", user.get("jobTitle", ""),
        "Report", report_type
    )
    for label_cell in ("A5", "G5", "L5", "A6", "G6", "L6"):
        ws[label_cell].fill = PatternFill("solid", fgColor=PRIMARY_DARK)
        ws[label_cell].font = Font(color=WHITE, bold=True)
    for value_cell in ("C5", "I5", "N5", "C6", "I6", "N6"):
        ws[value_cell].fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
        ws[value_cell].font = Font(color=PRIMARY_DARK, bold=True)
    ws["N5"].number_format = "dd-mmm-yyyy"

    selected = report_tasks(store, start_date, end_date)
    completed = sum(t["status"] == "Completed" for t in selected)
    in_progress = sum(t["status"] == "In Progress" for t in selected)
    overdue = sum(t["status"] not in ("Completed", "Cancelled") and safe_date(t["due"]) < date.today() for t in selected)
    est = sum(float(t.get("est", 0)) for t in selected)
    actual = sum(float(t.get("actual", 0)) for t in selected)
    rate = completed / len(selected) if selected else 0

    kpis = [
        ("Total Tasks", len(selected)), ("Completed", completed), ("In Progress", in_progress),
        ("Overdue", overdue), ("Estimated Hours", est), ("Actual Hours", actual),
        ("Completion Rate", rate)
    ]
    row = 8
    col = 1
    for label, value in kpis:
        ws.cell(row, col, label)
        ws.cell(row, col).fill = PatternFill("solid", fgColor=PRIMARY_DARK)
        ws.cell(row, col).font = Font(color=WHITE, bold=True)
        ws.cell(row + 1, col, value)
        ws.cell(row + 1, col).fill = PatternFill("solid", fgColor=PRIMARY_LIGHT)
        ws.cell(row + 1, col).font = Font(color=PRIMARY_DARK, bold=True, size=16)
        ws.cell(row, col).alignment = ws.cell(row + 1, col).alignment = Alignment(horizontal="center")
        if label == "Completion Rate":
            ws.cell(row + 1, col).number_format = "0%"
        col += 2

    detail_row = 12
    detail_headers = ["Task", "Project", "Task Category", "Deliverable Type", "Priority", "Status", "Start", "Due", "Progress", "Estimated", "Actual", "Variance", "Recurrence", "Link", "Notes"]
    for c, header in enumerate(detail_headers, 1):
        ws.cell(detail_row, c, header)
    style_header_row(ws, detail_row, 1, len(detail_headers))
    for task in selected:
        row = ws.max_row + 1
        ws.append([
            task.get("title", ""), task.get("project", ""), task.get("category", ""),
            task.get("deliverableType", ""), task.get("priority", ""), task.get("status", ""),
            safe_date(task.get("start")), safe_date(task.get("due")),
            float(task.get("progress", 0) or 0) / 100, float(task.get("est", 0) or 0),
            float(task.get("actual", 0) or 0), None, task.get("recurrence", "None"),
            task.get("link", ""), task.get("notes", "")
        ])
        ws.cell(row, 12, f"=K{row}-J{row}")
    for r in range(detail_row + 1, ws.max_row + 1):
        ws.cell(r, 7).number_format = "dd-mmm-yyyy"
        ws.cell(r, 8).number_format = "dd-mmm-yyyy"
        ws.cell(r, 9).number_format = "0%"
        ws.cell(r, 10).number_format = "0.0"
        ws.cell(r, 11).number_format = "0.0"
        ws.cell(r, 12).number_format = "0.0"
        for c in range(1, len(detail_headers) + 1):
            ws.cell(r, c).fill = PatternFill("solid", fgColor=CREAM)
            ws.cell(r, c).alignment = Alignment(vertical="top", wrap_text=c in (1, 3, 4, 15))
        link_cell = ws.cell(r, 14)
        if link_cell.value:
            link_cell.hyperlink = str(link_cell.value)
            link_cell.style = "Hyperlink"
    widths = [34,18,28,22,13,16,14,14,12,13,12,13,14,34,40]
    for idx, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = width
    ws.freeze_panes = "A13"
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = f"1:{detail_row}"

    # Small status chart data to the right
    chart_start = max(ws.max_row + 3, 18)
    status_rows = [
        ("Not Started", sum(t["status"] == "Not Started" for t in selected)),
        ("In Progress", in_progress),
        ("Completed", completed),
        ("On Hold", sum(t["status"] == "On Hold" for t in selected)),
        ("Cancelled", sum(t["status"] == "Cancelled" for t in selected)),
        ("Overdue", overdue),
    ]
    ws.cell(chart_start, 1, "Status")
    ws.cell(chart_start, 2, "Count")
    style_header_row(ws, chart_start, 1, 2)
    for offset, (label, count) in enumerate(status_rows, 1):
        ws.cell(chart_start + offset, 1, label)
        ws.cell(chart_start + offset, 2, count)
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Tasks by Status"
    chart.height = 7
    chart.width = 13
    data = Reference(ws, min_col=2, min_row=chart_start, max_row=chart_start + len(status_rows))
    cats = Reference(ws, min_col=1, min_row=chart_start + 1, max_row=chart_start + len(status_rows))
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.legend = None
    ws.add_chart(chart, f"G{chart_start}")
    return ws



def quarter_bounds(value, fallback):
    text = str(value or "").strip().upper()
    match = re.fullmatch(r"(\d{4})-?Q([1-4])", text)
    if match:
        year, quarter = int(match.group(1)), int(match.group(2))
    else:
        year = fallback.year
        quarter = (fallback.month - 1) // 3 + 1
    start_month = (quarter - 1) * 3 + 1
    start_date = date(year, start_month, 1)
    if quarter == 4:
        next_quarter = date(year + 1, 1, 1)
    else:
        next_quarter = date(year, start_month + 3, 1)
    return start_date, next_quarter - timedelta(days=1), f"Q{quarter} {year}"

def build_workbook(store, report="all", start=None, month=None, quarter=None):
    wb = Workbook()
    wb.remove(wb.active)
    add_overview_sheet(wb, store)
    add_profile_sheet(wb, store)
    add_tasks_sheet(wb, store)

    today = date.today()
    weekly_start = safe_date(start, sunday_of_week(today))
    weekly_end = weekly_start + timedelta(days=4)
    month_start = safe_date((month or today.strftime("%Y-%m")) + "-01", today.replace(day=1))
    if month_start.month == 12:
        next_month = date(month_start.year + 1, 1, 1)
    else:
        next_month = date(month_start.year, month_start.month + 1, 1)
    month_end = next_month - timedelta(days=1)
    quarter_start, quarter_end, quarter_label = quarter_bounds(quarter, today)

    if report in ("all", "weekly"):
        add_report_sheet(wb, store, "Weekly Report", weekly_start, weekly_end, "Weekly")
    if report in ("all", "monthly"):
        add_report_sheet(wb, store, "Monthly Report", month_start, month_end, "Monthly")
    if report in ("all", "quarterly"):
        add_report_sheet(wb, store, "Quarterly Report", quarter_start, quarter_end, quarter_label)
    return wb


def workbook_bytes(store, report="all", start=None, month=None, quarter=None):
    wb = build_workbook(store, report=report, start=start, month=month, quarter=quarter)
    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


def write_excel_file(store, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = workbook_bytes(store, report="all")
    temp = path.with_suffix(".tmp.xlsx")
    temp.write_bytes(data)
    temp.replace(path)


HEADER_ALIASES = {
    "task id": "id", "id": "id",
    "task name": "title", "title": "title", "task": "title",
    "project": "project",
    "task category": "category", "category": "category",
    "priority": "priority", "status": "status",
    "impact": "impact", "blocker status": "blockerStatus",
    "deliverable type": "deliverableType", "delivery status": "deliveryStatus",
    "action status": "actionStatus",
    "notification status": "notificationStatus", "notification": "notificationStatus",
    "start date": "start", "start": "start",
    "due date": "due", "deadline": "due", "due": "due",
    "progress": "progress", "progress %": "progress", "completion": "progress",
    "estimated hours": "est", "estimate": "est", "planned hours": "est",
    "actual hours": "actual", "hours": "actual",
    "recurrence": "recurrence", "recurring": "recurrence",
    "link": "link", "url": "link", "task link": "link", "hyperlink": "link",
    "notes": "notes", "description": "notes",
}


def normalize_header(value):
    text = re.sub(r"\s+", " ", str(value or "").strip().lower())
    return HEADER_ALIASES.get(text)


def find_task_sheet_and_header(wb):
    candidate_names = ["Tasks", "Task Database", "Task Data", "My Tasks"]
    sheets = [wb[name] for name in candidate_names if name in wb.sheetnames]
    sheets.extend(ws for ws in wb.worksheets if ws not in sheets)
    for ws in sheets:
        for row in range(1, min(ws.max_row, 30) + 1):
            mapped = {}
            for col in range(1, min(ws.max_column, 40) + 1):
                key = normalize_header(ws.cell(row, col).value)
                if key:
                    mapped[key] = col
            if "title" in mapped and len(mapped) >= 3:
                return ws, row, mapped
    raise ValueError("No task table was found. Use the import template or include a 'Task Name' column.")


def parse_profile_sheet(wb):
    if "Employee Profile" not in wb.sheetnames:
        return None
    ws = wb["Employee Profile"]
    aliases = {
        "full name": "name", "employee": "name", "employee name": "name",
        "employee id": "employeeId", "academy email": "email", "email": "email",
        "department": "department", "job title": "jobTitle", "phone": "phone",
    }
    result = {}
    for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 40), values_only=True):
        values = [v for v in row if v not in (None, "")]
        if len(values) < 2:
            continue
        key = aliases.get(str(values[0]).strip().lower())
        if key:
            result[key] = str(values[1]).strip()
    return result or None


def parse_excel(data):
    try:
        wb = load_workbook(io.BytesIO(data), data_only=True, read_only=True)
    except Exception as exc:
        raise ValueError(f"Unable to read Excel file: {exc}") from exc
    ws, header_row, columns = find_task_sheet_and_header(wb)
    tasks = []
    next_id = 1
    for row in range(header_row + 1, ws.max_row + 1):
        raw = {}
        for key, col in columns.items():
            raw[key] = ws.cell(row, col).value
        task = normalize_task(raw, next_id)
        if not task["title"]:
            continue
        tasks.append(task)
        next_id = max(next_id, task["id"] + 1)
    return tasks, parse_profile_sheet(wb)


def parse_csv(data):
    text = data.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    tasks = []
    next_id = 1
    for row in reader:
        mapped = {}
        for header, value in row.items():
            key = normalize_header(header)
            if key:
                mapped[key] = value
        task = normalize_task(mapped, next_id)
        if task["title"]:
            tasks.append(task)
            next_id = max(next_id, task["id"] + 1)
    if not tasks:
        raise ValueError("No tasks were found in the CSV file.")
    return tasks, None



def build_test_tasks():
    """Create current-date tasks for testing dashboards, filters, planners, and reports."""
    today = date.today()
    week_start = sunday_of_week(today)
    base_id = int(today.strftime("%y%m%d")) * 100
    specs = [
        ("Today priority review", "Academic", "Review & Quality Check", "Report", "High", "In Progress", today, today, 40, 3, 1),
        ("Completed test task", "Administration", "Administration", "Report", "Low", "Completed", today - timedelta(days=2), today - timedelta(days=1), 100, 2, 2),
        ("Tomorrow content task", "Marketing", "Content Development", "Web Page", "Medium", "Not Started", today, today + timedelta(days=1), 0, 5, 0),
        ("Overdue follow-up test", "Operations", "Meetings & Coordination", "Report", "High", "In Progress", today - timedelta(days=5), today - timedelta(days=1), 65, 4, 3),
        ("Weekly planning test", "Academic", "Program Tracking & Monitoring", "Course Outline", "Medium", "In Progress", week_start, week_start + timedelta(days=4), 55, 8, 4),
        ("Quarterly reporting test", "Strategic", "Program Tracking & Monitoring", "Report", "High", "Not Started", today - timedelta(days=15), today + timedelta(days=45), 15, 20, 2),
        ("On-hold coordination test", "IT", "Meetings with Client / Partner", "Proposal", "Medium", "On Hold", today, today + timedelta(days=7), 25, 6, 1),
    ]
    result = []
    for index, (title, project, category, deliverable, priority, status, start, due, progress, est, actual) in enumerate(specs, 1):
        result.append({
            "id": base_id + index,
            "title": title,
            "project": project,
            "category": category,
            "deliverableType": deliverable,
            "priority": priority,
            "status": status,
            "start": start.isoformat(),
            "due": due.isoformat(),
            "progress": progress,
            "est": est,
            "actual": actual,
            "day": workday_name(due.isoformat()),
            "recurrence": "None",
            "link": "",
            "notes": "Automatically generated test task.",
        })
    return result

def merge_tasks(existing, imported):
    by_key = {}
    output = []
    for task in existing + imported:
        key = (task["title"].strip().lower(), task["due"], task["project"].strip().lower())
        by_key[key] = task
    used = set()
    for task in by_key.values():
        while task["id"] in used:
            task = dict(task)
            task["id"] += 1
        used.add(task["id"])
        output.append(task)
    return sorted(output, key=lambda t: (t["due"], t["title"].lower()))


def template_bytes():
    store = new_store(
        user={
            "name": "Employee Name", "employeeId": "EMP-001",
            "email": "employee@andalusia.net",
            "department": "Academic Department", "jobTitle": "Employee", "phone": ""
        },
        tasks=SAMPLE_TASKS[:2],
    )
    wb = Workbook()
    wb.remove(wb.active)
    add_overview_sheet(wb, store)
    add_profile_sheet(wb, store)
    add_tasks_sheet(wb, store)
    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


INSTRUCTOR_COLUMNS = [
    "Name", "Email", "Phone", "Specialty", "Level", "Source",
    "Work Schedule", "Availability", "Region", "Notes"
]
INSTRUCTOR_HEADER_ALIASES = {
    "name": "Name", "instructor": "Name", "instructor name": "Name", "full name": "Name",
    "email": "Email", "email address": "Email", "phone": "Phone", "mobile": "Phone",
    "specialty": "Specialty", "speciality": "Specialty", "expertise": "Specialty",
    "level": "Level", "seniority": "Level", "source": "Source", "type": "Source",
    "work schedule": "Work Schedule", "schedule": "Work Schedule", "availability": "Availability",
    "region": "Region", "country": "Region", "notes": "Notes", "note": "Notes"
}

def _clean_instructor_row(raw, row_number):
    normalized = {column: "" for column in INSTRUCTOR_COLUMNS}
    for key, value in raw.items():
        alias = INSTRUCTOR_HEADER_ALIASES.get(str(key or "").strip().lower())
        if alias:
            normalized[alias] = str(value if value is not None else "").strip()
    errors = []
    if not normalized["Name"]:
        errors.append(f"Row {row_number}: Name is required.")
    email = normalized["Email"]
    if email and ("@" not in email or email.startswith("@") or email.endswith("@")):
        errors.append(f"Row {row_number}: Email does not look valid.")
    normalized["Source"] = normalized["Source"] or "External"
    normalized["Availability"] = normalized["Availability"] or "Available"
    normalized["Work Schedule"] = normalized["Work Schedule"] or "Project Based"
    return normalized, errors

def parse_instructor_import(data, filename):
    rows, errors = [], []
    if filename.lower().endswith('.csv'):
        text = data.decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(text))
        for row_number, raw in enumerate(reader, start=2):
            item, row_errors = _clean_instructor_row(raw, row_number)
            errors.extend(row_errors)
            if item["Name"] and not row_errors:
                rows.append(item)
    else:
        wb = load_workbook(io.BytesIO(data), data_only=True)
        ws = wb["Instructors"] if "Instructors" in wb.sheetnames else wb.active
        headers = [str(cell.value or "").strip() for cell in ws[1]]
        if not any(INSTRUCTOR_HEADER_ALIASES.get(h.lower()) == "Name" for h in headers):
            raise ValueError("Instructor sheet must contain a Name column.")
        for row_number, values in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not any(value not in (None, "") for value in values):
                continue
            raw = {headers[index]: value for index, value in enumerate(values) if index < len(headers)}
            item, row_errors = _clean_instructor_row(raw, row_number)
            errors.extend(row_errors)
            if item["Name"] and not row_errors:
                rows.append(item)
    seen = set()
    deduped = []
    for item in rows:
        key = item["Name"].casefold()
        if key in seen:
            errors.append(f"Duplicate instructor in file: {item['Name']}.")
            continue
        seen.add(key)
        deduped.append(item)
    return deduped, errors

def instructor_template_bytes():
    wb = Workbook()
    ws = wb.active
    ws.title = "Instructors"
    ws.append(INSTRUCTOR_COLUMNS)
    ws.append(["Dr. Example Name", "example@andalusia.net", "+20 1000000000", "Clinical Leadership", "Senior", "External", "Project Based", "Available", "Egypt", "Replace or delete this sample row before importing."])
    header_fill = PatternFill("solid", fgColor=PRIMARY_DARK)
    header_font = Font(color=WHITE, bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    widths = [28, 30, 20, 28, 16, 16, 20, 18, 18, 48]
    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:J2"
    help_ws = wb.create_sheet("Instructions")
    help_ws["A1"] = "Instructor Import Instructions"
    help_ws["A1"].font = Font(size=16, bold=True, color=PRIMARY_DARK)
    instructions = [
        "Name is required. All other fields are optional.",
        "Import previews rows before anything is added to the directory.",
        "Existing instructors with the same name are updated only when you choose Replace Existing during confirmation.",
        "Recommended Source values: Internal or External.",
        "Recommended Availability values: Available, Limited, Unavailable."
    ]
    for row, text in enumerate(instructions, start=3):
        help_ws.cell(row=row, column=1, value=text)
    help_ws.column_dimensions["A"].width = 110
    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


class Handler(BaseHTTPRequestHandler):
    server_version = "AndalusiaWorkManagement/5.0"

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_json(self, payload, status=200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_bytes(self, data, content_type, filename=None, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(data)

    def read_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(length) if length else b""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/store":
                self.send_json(load_store())
                return
            if path == "/api/export-text":
                data = STORE_PATH.read_bytes() if STORE_PATH.exists() else json.dumps(load_store(), indent=2).encode()
                self.send_bytes(data, "application/json; charset=utf-8", "andalusia_work_management_backup.json")
                return
            if path == "/api/export-excel":
                store = load_store()
                report = query.get("report", ["all"])[0]
                start = query.get("start", [None])[0]
                month = query.get("month", [None])[0]
                quarter = query.get("quarter", [None])[0]
                data = workbook_bytes(store, report=report, start=start, month=month, quarter=quarter)
                filename = {
                    "weekly": "andalusia_weekly_report.xlsx",
                    "monthly": "andalusia_monthly_report.xlsx",
                    "quarterly": "andalusia_quarterly_report.xlsx",
                }.get(report, "andalusia_task_data.xlsx")
                self.send_bytes(data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename)
                return
            if path == "/api/import-template":
                self.send_bytes(template_bytes(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "andalusia_import_template.xlsx")
                return
            if path == "/api/instructor-template":
                self.send_bytes(instructor_template_bytes(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "andalusia_instructor_import_template.xlsx")
                return
            self.serve_static(path)
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path == "/api/store":
                payload = json.loads(self.read_body().decode("utf-8"))
                self.send_json(save_store(payload))
                return
            if path == "/api/add-sample":
                current = load_store()
                merged = merge_tasks(current.get("tasks", []), [dict(task) for task in SAMPLE_TASKS])
                self.send_json(save_store(new_store(
                    user=current.get("user"), tasks=merged,
                    programs=current.get("programs"), assignments=current.get("assignments"),
                    notifications=current.get("notifications"), audit=current.get("audit"),
                    documents=current.get("documents"), master_data=current.get("masterData"),
                    settings=current.get("settings"), rule_overrides=current.get("ruleOverrides")
                )))
                return
            if path == "/api/add-test":
                current = load_store()
                merged = merge_tasks(current.get("tasks", []), build_test_tasks())
                self.send_json(save_store(new_store(
                    user=current.get("user"), tasks=merged,
                    programs=current.get("programs"), assignments=current.get("assignments"),
                    notifications=current.get("notifications"), audit=current.get("audit"),
                    documents=current.get("documents"), master_data=current.get("masterData"),
                    settings=current.get("settings"), rule_overrides=current.get("ruleOverrides")
                )))
                return
            if path == "/api/reset-sample":
                current = load_store()
                self.send_json(save_store(new_store(
                    user=current.get("user"), tasks=SAMPLE_TASKS,
                    programs=current.get("programs"), assignments=current.get("assignments"),
                    notifications=current.get("notifications"), audit=current.get("audit"),
                    documents=current.get("documents"), master_data=current.get("masterData"),
                    settings=current.get("settings"), rule_overrides=current.get("ruleOverrides")
                )))
                return
            if path == "/api/preview-instructors":
                body = self.read_body()
                if not body:
                    raise ValueError("The uploaded instructor file is empty.")
                filename = unquote(query.get("filename", ["instructors.xlsx"])[0])
                if not filename.lower().endswith((".xlsx", ".csv")):
                    raise ValueError("Choose an .xlsx or .csv instructor file.")
                rows, errors = parse_instructor_import(body, filename)
                self.send_json({"rows": rows, "errors": errors, "valid": len(rows), "filename": filename})
                return
            if path == "/api/import-excel":
                body = self.read_body()
                if not body:
                    raise ValueError("The uploaded file is empty.")
                filename = unquote(query.get("filename", ["import.xlsx"])[0])
                mode = query.get("mode", ["replace"])[0]
                if filename.lower().endswith(".csv"):
                    imported, imported_user = parse_csv(body)
                else:
                    imported, imported_user = parse_excel(body)
                current = load_store()
                tasks = merge_tasks(current.get("tasks", []), imported) if mode == "merge" else imported
                user = imported_user or current.get("user")
                saved = save_store(new_store(
                    user=user, tasks=tasks,
                    programs=current.get("programs"), assignments=current.get("assignments"),
                    notifications=current.get("notifications"), audit=current.get("audit"),
                    documents=current.get("documents"), master_data=current.get("masterData"),
                    settings=current.get("settings"), rule_overrides=current.get("ruleOverrides")
                ))
                self.send_json({"imported": len(imported), "mode": mode, "store": saved})
                return
            self.send_json({"error": "Endpoint not found"}, status=404)
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON data."}, status=400)
        except ValueError as exc:
            self.send_json({"error": str(exc)}, status=400)
        except Exception as exc:
            self.send_json({"error": str(exc)}, status=500)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/store":
            try:
                self.send_json(save_store(new_store(user=None, tasks=[], programs=[], assignments=[], notifications=[], audit=[], documents=[], master_data={}, settings={}, rule_overrides={})))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=500)
            return
        self.send_json({"error": "Endpoint not found"}, status=404)

    def serve_static(self, path):
        rel = "index.html" if path in ("", "/") else path.lstrip("/")
        file_path = (STATIC_DIR / rel).resolve()
        if STATIC_DIR.resolve() not in file_path.parents and file_path != STATIC_DIR.resolve():
            self.send_json({"error": "Invalid path"}, status=400)
            return
        if not file_path.exists() or not file_path.is_file():
            self.send_json({"error": "File not found"}, status=404)
            return
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_bytes(file_path.read_bytes(), mime)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    store = load_store()
    save_store(store)  # ensure JSON and Excel mirror are available
    url = f"http://{HOST}:{PORT}"
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("=" * 64)
    print("Andalusia Academy Work Management System — Prototype V5 Revision 19.1 Pixel-Matched Executive UI")
    print(f"Open: {url}")
    print(f"SQLite database: {DB_PATH}")
    print(f"JSON snapshot:   {STORE_PATH}")
    print(f"Excel mirror:    {EXCEL_PATH}")
    print("Press Ctrl+C to stop.")
    print("=" * 64)
    if os.environ.get("ANDALUSIA_NO_BROWSER") != "1":
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
