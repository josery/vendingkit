"""
VendingKit Memory Module
Gestiona el almacenamiento de conversaciones en SQLite
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
import os

DB_PATH = os.getenv("DB_PATH", "vendingkit.db")


class Memory:
    """Gestor de memoria basado en SQLite"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabla de conversaciones
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT UNIQUE,
                messages TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            """
        )

        # Tabla de incidentes
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                name TEXT,
                location TEXT,
                company TEXT,
                floor TEXT,
                extension TEXT,
                celular TEXT,
                category TEXT,
                description TEXT,
                response TEXT,
                monto REAL,
                created_at TEXT,
                synced_to_sheets INTEGER DEFAULT 0
            )
            """
        )

        conn.commit()
        conn.close()

    def save_conversation(self, phone_number: str, message: str, role: str = "user"):
        """Guarda un mensaje en la conversación"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()

        cursor.execute("SELECT messages FROM conversations WHERE phone_number = ?", (phone_number,))
        row = cursor.fetchone()

        if row:
            messages = json.loads(row[0])
        else:
            messages = []

        messages.append({"role": role, "content": message, "timestamp": timestamp})

        cursor.execute(
            """
            INSERT OR REPLACE INTO conversations (phone_number, messages, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (phone_number, json.dumps(messages), timestamp, timestamp),
        )

        conn.commit()
        conn.close()

    def get_conversation_history(self, phone_number: str) -> List[Dict[str, Any]]:
        """Obtiene el historial de conversación de un usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT messages FROM conversations WHERE phone_number = ?", (phone_number,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return json.loads(row[0])
        return []

    def save_incident(self, incident_data: Dict[str, Any]) -> int:
        """Guarda un incidente y retorna su ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO incidents
            (phone_number, name, location, company, floor, extension, celular, category, description, response, monto, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                incident_data.get("phone_number"),
                incident_data.get("name"),
                incident_data.get("location"),
                incident_data.get("company"),
                incident_data.get("floor"),
                incident_data.get("extension"),
                incident_data.get("celular"),
                incident_data.get("category"),
                incident_data.get("description"),
                incident_data.get("response"),
                incident_data.get("monto"),
                datetime.now().isoformat(),
            ),
        )

        incident_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return incident_id

    def get_unsync_incidents(self) -> List[Dict[str, Any]]:
        """Obtiene incidentes no sincronizados con Google Sheets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM incidents WHERE synced_to_sheets = 0")
        rows = cursor.fetchall()

        conn.close()

        incidents = []
        for row in rows:
            incidents.append(
                {
                    "id": row[0],
                    "phone_number": row[1],
                    "name": row[2],
                    "location": row[3],
                    "company": row[4],
                    "floor": row[5],
                    "extension": row[6],
                    "celular": row[7],
                    "category": row[8],
                    "description": row[9],
                    "response": row[10],
                    "monto": row[11],
                    "created_at": row[12],
                }
            )

        return incidents

    def mark_incident_synced(self, incident_id: int):
        """Marca un incidente como sincronizado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("UPDATE incidents SET synced_to_sheets = 1 WHERE id = ?", (incident_id,))

        conn.commit()
        conn.close()
