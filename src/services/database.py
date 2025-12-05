"""
SQLite database for tracking carbon footprint history
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class CarbonFootprintDB:
    """
    Manages historical carbon footprint data
    """

    def __init__(self, db_path: str = "carbon_footprint.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Main footprint records
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS footprint_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_emissions REAL NOT NULL,
                transport_emissions REAL,
                diet_emissions REAL,
                heating_emissions REAL,
                electricity_emissions REAL,
                consumption_emissions REAL,
                transport_mode TEXT,
                distance_km REAL,
                diet_type TEXT,
                heating_type TEXT,
                heating_hours REAL,
                electricity_kwh REAL,
                grid_carbon_intensity REAL,
                atmospheric_co2_ppm REAL,
                notes TEXT
            )
        ''')

        # User goals and achievements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_type TEXT NOT NULL,
                target_value REAL NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                achieved BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')

        # Insights from LLM
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS llm_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                footprint_id INTEGER,
                insight_text TEXT NOT NULL,
                model_used TEXT,
                FOREIGN KEY (footprint_id) REFERENCES footprint_records (id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_footprint(self, data: Dict) -> int:
        """Save a footprint calculation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO footprint_records (
                timestamp, total_emissions, transport_emissions, diet_emissions,
                heating_emissions, electricity_emissions, consumption_emissions,
                transport_mode, distance_km, diet_type, heating_type,
                heating_hours, electricity_kwh, grid_carbon_intensity,
                atmospheric_co2_ppm, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('timestamp', datetime.now().isoformat()),
            data['total_emissions'],
            data.get('transport_emissions', 0),
            data.get('diet_emissions', 0),
            data.get('heating_emissions', 0),
            data.get('electricity_emissions', 0),
            data.get('consumption_emissions', 0),
            data.get('transport_mode'),
            data.get('distance_km'),
            data.get('diet_type'),
            data.get('heating_type'),
            data.get('heating_hours'),
            data.get('electricity_kwh'),
            data.get('grid_carbon_intensity'),
            data.get('atmospheric_co2_ppm'),
            data.get('notes')
        ))

        record_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return record_id

    def save_llm_insight(self, footprint_id: int, insight: str, model: str = "llama3:8b"):
        """Save an LLM-generated insight"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO llm_insights (timestamp, footprint_id, insight_text, model_used)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), footprint_id, insight, model))

        conn.commit()
        conn.close()

    def get_recent_records(self, limit: int = 30) -> List[Dict]:
        """Get recent footprint records"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM footprint_records
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        records = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return records

    def get_statistics(self, days: int = 30) -> Dict:
        """Get statistics for the past N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute('''
            SELECT
                COUNT(*) as record_count,
                AVG(total_emissions) as avg_emissions,
                MIN(total_emissions) as min_emissions,
                MAX(total_emissions) as max_emissions,
                SUM(total_emissions) as total_emissions,
                AVG(transport_emissions) as avg_transport,
                AVG(diet_emissions) as avg_diet,
                AVG(heating_emissions) as avg_heating,
                AVG(electricity_emissions) as avg_electricity
            FROM footprint_records
            WHERE timestamp >= ?
        ''', (cutoff_date,))

        row = cursor.fetchone()
        conn.close()

        if row and row[0] > 0:
            return {
                'record_count': row[0],
                'avg_daily_emissions': row[1],
                'min_emissions': row[2],
                'max_emissions': row[3],
                'total_emissions': row[4],
                'avg_transport': row[5],
                'avg_diet': row[6],
                'avg_heating': row[7],
                'avg_electricity': row[8],
                'period_days': days
            }
        else:
            return {
                'record_count': 0,
                'period_days': days
            }

    def get_trend_data(self, days: int = 30) -> List[Dict]:
        """Get time-series data for charts"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute('''
            SELECT
                timestamp,
                total_emissions,
                transport_emissions,
                diet_emissions,
                heating_emissions,
                electricity_emissions,
                consumption_emissions
            FROM footprint_records
            WHERE timestamp >= ?
            ORDER BY timestamp ASC
        ''', (cutoff_date,))

        records = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return records

    def get_category_breakdown(self, days: int = 30) -> Dict:
        """Get average breakdown by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        cursor.execute('''
            SELECT
                AVG(transport_emissions) as transport,
                AVG(diet_emissions) as diet,
                AVG(heating_emissions) as heating,
                AVG(electricity_emissions) as electricity,
                AVG(consumption_emissions) as consumption
            FROM footprint_records
            WHERE timestamp >= ?
        ''', (cutoff_date,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'Transport': row[0] or 0,
                'Diet': row[1] or 0,
                'Heating': row[2] or 0,
                'Electricity': row[3] or 0,
                'Consumption': row[4] or 0
            }
        else:
            return {}

    def clear_all_data(self):
        """Clear all records (use with caution)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM footprint_records')
        cursor.execute('DELETE FROM llm_insights')
        cursor.execute('DELETE FROM user_goals')

        conn.commit()
        conn.close()


if __name__ == "__main__":
    # Test the database
    db = CarbonFootprintDB("test_carbon.db")

    # Test saving a record
    test_data = {
        'timestamp': datetime.now().isoformat(),
        'total_emissions': 15.5,
        'transport_emissions': 5.0,
        'diet_emissions': 5.0,
        'heating_emissions': 3.0,
        'electricity_emissions': 2.5,
        'consumption_emissions': 0,
        'transport_mode': 'car_petrol',
        'distance_km': 25,
        'diet_type': 'omnivore',
        'heating_type': 'natural_gas',
        'heating_hours': 4,
        'electricity_kwh': 10,
        'atmospheric_co2_ppm': 425.0,
        'notes': 'Test record'
    }

    record_id = db.save_footprint(test_data)
    print(f"Saved record with ID: {record_id}")

    # Get statistics
    stats = db.get_statistics(30)
    print(f"\nStatistics: {json.dumps(stats, indent=2)}")

    # Get recent records
    recent = db.get_recent_records(5)
    print(f"\nRecent records: {len(recent)}")
