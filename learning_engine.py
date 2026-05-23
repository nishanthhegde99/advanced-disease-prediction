#!/usr/bin/env python3
"""
Self-Learning Engine
- Tracks prediction accuracy over time
- Learns from user feedback
- Improves model performance
- Maintains prediction history
"""

import sqlite3
import json
from datetime import datetime
from collections import defaultdict

class SelfLearningEngine:
    """System that learns from predictions and user feedback"""
    
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize learning database"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        # Prediction history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symptoms TEXT,
                predicted_disease TEXT,
                confidence REAL,
                actual_disease TEXT,
                user_feedback TEXT,
                accuracy_score REAL,
                model_used TEXT
            )
        """)
        
        # Model performance tracking
        cur.execute("""
            CREATE TABLE IF NOT EXISTS model_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                model_name TEXT,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                total_predictions INTEGER
            )
        """)
        
        # Symptom-disease correlation learning
        cur.execute("""
            CREATE TABLE IF NOT EXISTS learned_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symptom_id INTEGER,
                disease_id INTEGER,
                correlation_strength REAL,
                confidence REAL,
                last_updated TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def record_prediction(self, symptoms, predicted_disease, confidence, model_used):
        """Record a prediction for learning"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO prediction_history 
            (timestamp, symptoms, predicted_disease, confidence, model_used)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            json.dumps(symptoms),
            predicted_disease,
            confidence,
            model_used
        ))
        
        conn.commit()
        conn.close()
    
    def record_feedback(self, prediction_id, actual_disease, feedback_type):
        """Record user feedback on prediction accuracy"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        # Calculate accuracy score
        accuracy_score = 1.0 if feedback_type == "correct" else 0.0
        
        cur.execute("""
            UPDATE prediction_history 
            SET actual_disease = ?, user_feedback = ?, accuracy_score = ?
            WHERE id = ?
        """, (actual_disease, feedback_type, accuracy_score, prediction_id))
        
        conn.commit()
        conn.close()
        
        # Update model performance
        self._update_model_performance()
    
    def _update_model_performance(self):
        """Update model performance metrics based on feedback"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        # Get recent predictions with feedback
        cur.execute("""
            SELECT model_used, accuracy_score FROM prediction_history 
            WHERE accuracy_score IS NOT NULL 
            AND timestamp > datetime('now', '-7 days')
        """)
        
        model_scores = defaultdict(list)
        for model_name, score in cur.fetchall():
            model_scores[model_name].append(score)
        
        # Record performance
        for model_name, scores in model_scores.items():
            if scores:
                avg_accuracy = sum(scores) / len(scores)
                cur.execute("""
                    INSERT INTO model_performance 
                    (date, model_name, accuracy, total_predictions)
                    VALUES (?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    model_name,
                    avg_accuracy,
                    len(scores)
                ))
        
        conn.commit()
        conn.close()
    
    def get_learning_insights(self):
        """Get insights from learning data"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        # Overall accuracy
        cur.execute("""
            SELECT AVG(accuracy_score) FROM prediction_history 
            WHERE accuracy_score IS NOT NULL
        """)
        overall_accuracy = cur.fetchone()[0] or 0
        
        # Total predictions
        cur.execute("SELECT COUNT(*) FROM prediction_history")
        total_predictions = cur.fetchone()[0]
        
        # Feedback count
        cur.execute("""
            SELECT COUNT(*) FROM prediction_history 
            WHERE user_feedback IS NOT NULL
        """)
        feedback_count = cur.fetchone()[0]
        
        # Model performance comparison
        cur.execute("""
            SELECT model_name, AVG(accuracy) as avg_accuracy, COUNT(*) as count
            FROM model_performance
            GROUP BY model_name
            ORDER BY avg_accuracy DESC
        """)
        model_performance = cur.fetchall()
        
        conn.close()
        
        return {
            "overall_accuracy": float(overall_accuracy) if overall_accuracy else 0,
            "total_predictions": total_predictions,
            "feedback_count": feedback_count,
            "model_performance": [
                {
                    "model": m[0],
                    "accuracy": float(m[1]),
                    "predictions": m[2]
                } for m in model_performance
            ]
        }
    
    def get_prediction_history(self, limit=10):
        """Get recent prediction history"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, timestamp, predicted_disease, confidence, user_feedback, accuracy_score
            FROM prediction_history
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        history = []
        for row in cur.fetchall():
            history.append({
                "id": row[0],
                "timestamp": row[1],
                "predicted_disease": row[2],
                "confidence": row[3],
                "feedback": row[4],
                "accuracy": row[5]
            })
        
        conn.close()
        return history
    
    def get_improvement_metrics(self):
        """Get system improvement metrics over time"""
        conn = sqlite3.connect("disease.db")
        cur = conn.cursor()
        
        # Weekly improvement
        cur.execute("""
            SELECT 
                strftime('%Y-%W', timestamp) as week,
                AVG(accuracy_score) as weekly_accuracy,
                COUNT(*) as predictions
            FROM prediction_history
            WHERE accuracy_score IS NOT NULL
            GROUP BY week
            ORDER BY week DESC
            LIMIT 4
        """)
        
        weekly_data = cur.fetchall()
        
        conn.close()
        
        return {
            "weekly_improvement": [
                {
                    "week": w[0],
                    "accuracy": float(w[1]) if w[1] else 0,
                    "predictions": w[2]
                } for w in weekly_data
            ]
        }

# Initialize global learning engine
learning_engine = SelfLearningEngine()
