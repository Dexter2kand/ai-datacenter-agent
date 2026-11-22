
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "datacenter.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                manufacturer TEXT,
                model TEXT,
                location TEXT,
                status TEXT DEFAULT 'Operational'
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NOT NULL,
                alarm_code TEXT,
                symptoms TEXT NOT NULL,
                root_cause TEXT,
                corrective_action TEXT,
                contractor TEXT,
                verification_status TEXT DEFAULT 'Unverified',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (equipment_id)
                    REFERENCES equipment(id)
            )
        """)


def add_equipment(name, category, manufacturer, model, location):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO equipment
            (name, category, manufacturer, model, location)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category, manufacturer, model, location))


def get_equipment():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM equipment ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def add_incident(
    equipment_id, alarm_code, symptoms,
    root_cause="", corrective_action="",
    contractor="", verification_status="Unverified"
):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO incidents (
                equipment_id, alarm_code, symptoms,
                root_cause, corrective_action,
                contractor, verification_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            equipment_id, alarm_code, symptoms,
            root_cause, corrective_action,
            contractor, verification_status
        ))


def get_incidents():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                incidents.*,
                equipment.name AS equipment_name,
                equipment.category AS category
            FROM incidents
            JOIN equipment
                ON incidents.equipment_id = equipment.id
            ORDER BY incidents.id DESC
        """).fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    init_database()
    print("Data Center database initialized successfully!")

