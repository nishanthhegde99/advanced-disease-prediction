#!/usr/bin/env python3
"""
================================================================================
TEMPORAL SYMPTOM PROGRESSION DATABASE SCHEMA
================================================================================
Database structure for tracking symptom timelines
================================================================================
"""

import sqlite3
from datetime import datetime

def create_temporal_tables():
    """Create tables for temporal symptom tracking"""
    conn = sqlite3.connect("disease.db")
    cur = conn.cursor()
    
    # Table for storing symptom timelines
    cur.execute("""
    CREATE TABLE IF NOT EXISTS symptom_timeline (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        symptom_id INTEGER,
        symptom_name TEXT,
        started_hours_ago REAL,
        severity INTEGER DEFAULT 5,
        timestamp TEXT,
        FOREIGN KEY (symptom_id) REFERENCES symptom(id)
    )
    """)
    
    # Table for disease progression patterns
    cur.execute("""
    CREATE TABLE IF NOT EXISTS disease_progression_pattern (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disease_id INTEGER,
        disease_name TEXT,
        symptom_sequence TEXT,
        typical_velocity REAL,
        min_hours REAL,
        max_hours REAL,
        urgency_level TEXT,
        pattern_description TEXT,
        FOREIGN KEY (disease_id) REFERENCES disease(id)
    )
    """)
    
    # Table for temporal predictions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS temporal_prediction (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        predicted_disease TEXT,
        temporal_confidence REAL,
        velocity_score REAL,
        pattern_match_score REAL,
        urgency_level TEXT,
        timestamp TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Temporal database tables created successfully")

def insert_disease_patterns():
    """Insert disease progression patterns (REFERENCE CLINICAL DATA)"""
    conn = sqlite3.connect("disease.db")
    cur = conn.cursor()
    
    # Disease progression patterns
    patterns = [
        # (disease_id, disease_name, symptom_sequence, velocity, min_hours, max_hours, urgency, description)
        (1, "Influenza", "Fever→Body_ache→Cough→Fatigue", 0.04, 24, 72, "Medium", "Gradual onset over 1-3 days"),
        (2, "Common Cold", "Runny_nose→Sneezing→Sore_throat→Cough", 0.03, 24, 96, "Low", "Slow progression over 2-4 days"),
        (3, "COVID-19", "Fever→Dry_cough→Loss_of_smell→Breathing_difficulty", 0.02, 48, 120, "High", "Progressive respiratory symptoms"),
        (4, "Dengue Fever", "High_fever→Headache→Body_pain→Rash", 0.05, 24, 96, "High", "Fever spike then drop with rash"),
        (5, "Pneumonia", "Fever→Cough→Chest_pain→Breathing_difficulty", 0.06, 12, 72, "High", "Rapid respiratory deterioration"),
        (6, "Bacterial Meningitis", "Severe_headache→Fever→Stiff_neck→Confusion", 0.4, 2, 12, "Critical", "Rapid onset, life-threatening"),
        (7, "Migraine", "Headache→Nausea→Light_sensitivity→Visual_disturbance", 0.2, 1, 6, "Medium", "Rapid onset, severe headache"),
        (8, "Gastroenteritis", "Nausea→Vomiting→Diarrhea→Abdominal_pain", 0.15, 6, 24, "Medium", "Rapid GI symptoms"),
        (9, "Malaria", "Fever→Chills→Sweating→Headache", 0.08, 12, 48, "High", "Cyclical fever pattern"),
        (10, "Typhoid", "Fever→Headache→Abdominal_pain→Weakness", 0.03, 48, 168, "High", "Gradual onset over days"),
        (11, "Asthma Attack", "Wheezing→Breathing_difficulty→Chest_tightness→Cough", 0.3, 1, 6, "High", "Rapid respiratory distress"),
        (12, "Appendicitis", "Abdominal_pain→Nausea→Vomiting→Fever", 0.1, 6, 48, "Critical", "Progressive abdominal emergency"),
        (13, "Urinary Tract Infection", "Burning_urination→Frequent_urination→Abdominal_pain→Fever", 0.05, 24, 72, "Medium", "Progressive urinary symptoms"),
        (14, "Sinusitis", "Nasal_congestion→Facial_pain→Headache→Fever", 0.04, 24, 96, "Low", "Gradual sinus inflammation"),
        (15, "Bronchitis", "Cough→Mucus_production→Chest_discomfort→Fatigue", 0.05, 24, 72, "Medium", "Progressive respiratory infection"),
    ]
    
    for pattern in patterns:
        cur.execute("""
        INSERT OR IGNORE INTO disease_progression_pattern 
        (disease_id, disease_name, symptom_sequence, typical_velocity, min_hours, max_hours, urgency_level, pattern_description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, pattern)
    
    conn.commit()
    conn.close()
    print("✅ Disease progression patterns inserted successfully")

if __name__ == "__main__":
    create_temporal_tables()
    insert_disease_patterns()
    print("\n🎯 Temporal database setup complete!")
    print("📊 15 disease progression patterns loaded")
    print("✅ Temporal analysis database tables initialized")
