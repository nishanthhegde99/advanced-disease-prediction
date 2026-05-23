#!/usr/bin/env python3
"""
================================================================================
TEMPORAL SYMPTOM PROGRESSION ANALYZER
================================================================================
Method for disease prediction using temporal symptom progression analysis with
velocity calculation and pattern matching.
================================================================================
"""

import numpy as np
import sqlite3
from datetime import datetime
import math
import json

class TemporalSymptomAnalyzer:
    """
    Analyzes symptom progression over time.
    
    This class predicts diseases by analyzing when symptoms appeared in addition
    to which symptoms are present.
    """
    
    def __init__(self):
        self.db_path = "disease.db"
        self.decay_rate = 0.02  # Temporal decay constant
        
    def calculate_symptom_velocity(self, symptom_timeline):
        """
        Calculates symptom progression velocity.
        
        Velocity = Number of symptoms / Time span
        Higher velocity = More urgent condition
        
        Args:
            symptom_timeline: List of {symptom, started_hours_ago}
        
        Returns:
            velocity: Symptoms per hour (float)
        """
        if not symptom_timeline or len(symptom_timeline) == 0:
            return 0.0
        
        # Get time span (earliest to most recent symptom)
        hours_list = [s['started_hours_ago'] for s in symptom_timeline]
        time_span = max(hours_list) - min(hours_list)
        
        # Avoid division by zero
        if time_span == 0:
            time_span = 1.0
        
        # Calculate velocity
        velocity = len(symptom_timeline) / time_span
        
        return velocity
    
    def apply_temporal_weighting(self, symptom_timeline):
        """
        Applies temporal weighting function.
        
        Recent symptoms are weighted higher than older symptoms
        Weight = e^(-decay_rate × hours_ago)
        
        Args:
            symptom_timeline: List of symptoms with timestamps
        
        Returns:
            weighted_symptoms: List with temporal weights
        """
        weighted_symptoms = []
        
        for symptom in symptom_timeline:
            hours_ago = symptom['started_hours_ago']
            
            # Exponential decay formula
            weight = math.exp(-self.decay_rate * hours_ago)
            
            weighted_symptoms.append({
                'symptom': symptom['symptom'],
                'symptom_id': symptom.get('symptom_id'),
                'hours_ago': hours_ago,
                'weight': weight,
                'importance': int(weight * 100)  # Convert to percentage
            })
        
        return weighted_symptoms
    
    def match_disease_patterns(self, symptom_timeline, velocity, ml_predicted_disease=None):
        """
        Matches patient symptom progression against known disease patterns.
        
        If ML prediction provided, it gets priority boost for consistency.
        
        Args:
            symptom_timeline: Patient's symptom timeline
            velocity: Calculated symptom velocity
            ml_predicted_disease: ML model's prediction (for consistency)
        
        Returns:
            pattern_matches: List of diseases with match scores
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        
        # Get all disease patterns
        cur.execute("""
            SELECT disease_id, disease_name, symptom_sequence, 
                   typical_velocity, min_hours, max_hours, urgency_level, pattern_description
            FROM disease_progression_pattern
        """)
        patterns = cur.fetchall()
        
        pattern_matches = []
        
        # Get patient symptom names
        patient_symptoms = set([s['symptom'].lower().replace(' ', '_') for s in symptom_timeline])
        
        for pattern in patterns:
            disease_id, disease_name, symptom_seq, typical_vel, min_h, max_h, urgency, description = pattern
            
            # Parse symptom sequence
            pattern_symptoms = set([s.lower() for s in symptom_seq.split('→')])
            
            # Calculate symptom overlap
            overlap = len(patient_symptoms.intersection(pattern_symptoms))
            total_pattern_symptoms = len(pattern_symptoms)
            
            if total_pattern_symptoms > 0:
                symptom_match_score = (overlap / total_pattern_symptoms) * 100
            else:
                symptom_match_score = 0
            
            # Calculate velocity match
            velocity_difference = abs(velocity - typical_vel)
            velocity_match_score = max(0, 100 - (velocity_difference * 100))
            
            # Calculate time span match
            patient_time_span = max([s['started_hours_ago'] for s in symptom_timeline]) if symptom_timeline else 0
            time_in_range = min_h <= patient_time_span <= max_h
            time_match_score = 100 if time_in_range else 50
            
            # CONSISTENCY BOOST: If this matches ML prediction, boost score by 20%
            ml_consistency_boost = 0
            if ml_predicted_disease and disease_name.lower() == ml_predicted_disease.lower():
                ml_consistency_boost = 20
            
            # Combined pattern match score with ML consistency
            pattern_match_score = (
                symptom_match_score * 0.5 +
                velocity_match_score * 0.3 +
                time_match_score * 0.2 +
                ml_consistency_boost
            )
            
            if pattern_match_score > 30:  # Threshold for relevance
                pattern_matches.append({
                    'disease_id': disease_id,
                    'disease_name': disease_name,
                    'pattern_match_score': round(pattern_match_score, 2),
                    'symptom_match': round(symptom_match_score, 2),
                    'velocity_match': round(velocity_match_score, 2),
                    'urgency_level': urgency,
                    'pattern_description': description,
                    'typical_velocity': typical_vel,
                    'ml_consistent': ml_predicted_disease and disease_name.lower() == ml_predicted_disease.lower()
                })
        
        conn.close()
        
        # Sort by pattern match score
        pattern_matches.sort(key=lambda x: x['pattern_match_score'], reverse=True)
        
        return pattern_matches
    
    def assess_urgency(self, velocity, pattern_matches):
        """
        Determines urgency level based on symptom velocity and pattern matches.
        
        Args:
            velocity: Symptom progression velocity
            pattern_matches: Matched disease patterns
        
        Returns:
            urgency_info: Dictionary with urgency level and recommendations
        """
        # Velocity-based urgency
        if velocity > 0.3:
            velocity_urgency = "Critical"
            velocity_message = "🚨 RAPID SYMPTOM PROGRESSION - SEEK IMMEDIATE MEDICAL ATTENTION"
        elif velocity > 0.1:
            velocity_urgency = "High"
            velocity_message = "⚠️ Fast symptom progression - Medical evaluation recommended soon"
        elif velocity > 0.05:
            velocity_urgency = "Medium"
            velocity_message = "⚠️ Moderate progression - Schedule doctor appointment"
        else:
            velocity_urgency = "Low"
            velocity_message = "✓ Gradual onset - Monitor symptoms and consult if worsening"
        
        # Pattern-based urgency
        pattern_urgency = "Low"
        if pattern_matches:
            top_pattern = pattern_matches[0]
            pattern_urgency = top_pattern['urgency_level']
        
        # Combined urgency (take the higher urgency level)
        urgency_levels = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        final_urgency_value = max(
            urgency_levels.get(velocity_urgency, 1),
            urgency_levels.get(pattern_urgency, 1)
        )
        
        urgency_map = {1: "Low", 2: "Medium", 3: "High", 4: "Critical"}
        final_urgency = urgency_map[final_urgency_value]
        
        return {
            'urgency_level': final_urgency,
            'velocity_urgency': velocity_urgency,
            'pattern_urgency': pattern_urgency,
            'message': velocity_message,
            'requires_immediate_attention': final_urgency in ["High", "Critical"]
        }
    
    def analyze(self, symptom_timeline, ml_predicted_disease=None):
        """
        Performs complete temporal symptom analysis.
        
        This method combines symptom progression velocity, temporal weighting,
        pattern matching, and urgency assessment.
        
        Args:
            symptom_timeline: List of {symptom, symptom_id, started_hours_ago}
            ml_predicted_disease: ML model's prediction for consistency
        
        Returns:
            analysis_result: Complete temporal analysis with predictions
        """
        if not symptom_timeline or len(symptom_timeline) == 0:
            return {
                'status': 'error',
                'message': 'No symptom timeline provided'
            }
        
        # Step 1: Calculate symptom velocity
        velocity = self.calculate_symptom_velocity(symptom_timeline)
        
        # Step 2: Apply temporal weighting
        weighted_symptoms = self.apply_temporal_weighting(symptom_timeline)
        
        # Step 3: Match disease patterns with ML consistency
        pattern_matches = self.match_disease_patterns(symptom_timeline, velocity, ml_predicted_disease)
        
        # Step 4: Assess urgency
        urgency_info = self.assess_urgency(velocity, pattern_matches)
        
        # Step 5: Generate temporal confidence score
        if pattern_matches:
            top_match = pattern_matches[0]
            temporal_confidence = min(95, top_match['pattern_match_score'])
        else:
            temporal_confidence = 0
        
        # Calculate time span
        hours_list = [s['started_hours_ago'] for s in symptom_timeline]
        time_span_hours = max(hours_list) - min(hours_list) if len(hours_list) > 1 else max(hours_list)
        
        # Format time span for display
        if time_span_hours < 24:
            time_span_display = f"{int(time_span_hours)} hours"
        else:
            time_span_display = f"{int(time_span_hours / 24)} days"
        
        return {
            'status': 'success',
            'temporal_analysis': {
                'velocity': round(velocity, 4),
                'velocity_description': self._get_velocity_description(velocity),
                'time_span': time_span_display,
                'time_span_hours': time_span_hours,
                'symptom_count': len(symptom_timeline)
            },
            'weighted_symptoms': weighted_symptoms,
            'pattern_matches': pattern_matches[:5],  # Top 5 matches
            'top_prediction': pattern_matches[0] if pattern_matches else None,
            'temporal_confidence': round(temporal_confidence, 2),
            'urgency_assessment': urgency_info,
            'ml_consistent': pattern_matches[0]['ml_consistent'] if pattern_matches else False,
            'algorithm_version': '1.0',
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_velocity_description(self, velocity):
        """Helper method to describe velocity"""
        if velocity > 0.3:
            return "Very Rapid (Emergency)"
        elif velocity > 0.1:
            return "Rapid (Urgent)"
        elif velocity > 0.05:
            return "Moderate"
        elif velocity > 0.02:
            return "Gradual"
        else:
            return "Slow"
    
    def save_temporal_prediction(self, session_id, analysis_result):
        """Save temporal prediction to database for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            
            top_pred = analysis_result.get('top_prediction')
            if top_pred:
                cur.execute("""
                    INSERT INTO temporal_prediction 
                    (session_id, predicted_disease, temporal_confidence, velocity_score, 
                     pattern_match_score, urgency_level, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id,
                    top_pred['disease_name'],
                    analysis_result['temporal_confidence'],
                    analysis_result['temporal_analysis']['velocity'],
                    top_pred['pattern_match_score'],
                    analysis_result['urgency_assessment']['urgency_level'],
                    datetime.now().isoformat()
                ))
                
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving temporal prediction: {e}")

# ============================================================================
# TESTING FUNCTION
# ============================================================================
def test_temporal_analyzer():
    """Test the temporal analyzer with sample data"""
    analyzer = TemporalSymptomAnalyzer()
    
    # Test Case 1: Rapid onset (Emergency)
    print("\n" + "="*70)
    print("TEST CASE 1: Bacterial Meningitis (Rapid Onset)")
    print("="*70)
    
    timeline1 = [
        {'symptom': 'Severe headache', 'symptom_id': 1, 'started_hours_ago': 6},
        {'symptom': 'Fever', 'symptom_id': 2, 'started_hours_ago': 4},
        {'symptom': 'Stiff neck', 'symptom_id': 3, 'started_hours_ago': 2},
    ]
    
    result1 = analyzer.analyze(timeline1)
    print(f"Velocity: {result1['temporal_analysis']['velocity']} symptoms/hour")
    print(f"Description: {result1['temporal_analysis']['velocity_description']}")
    print(f"Urgency: {result1['urgency_assessment']['urgency_level']}")
    if result1['top_prediction']:
        print(f"Top Prediction: {result1['top_prediction']['disease_name']}")
        print(f"Confidence: {result1['temporal_confidence']}%")
    
    # Test Case 2: Gradual onset (Non-urgent)
    print("\n" + "="*70)
    print("TEST CASE 2: Common Cold (Gradual Onset)")
    print("="*70)
    
    timeline2 = [
        {'symptom': 'Runny nose', 'symptom_id': 4, 'started_hours_ago': 72},
        {'symptom': 'Sneezing', 'symptom_id': 5, 'started_hours_ago': 48},
        {'symptom': 'Sore throat', 'symptom_id': 6, 'started_hours_ago': 24},
    ]
    
    result2 = analyzer.analyze(timeline2)
    print(f"Velocity: {result2['temporal_analysis']['velocity']} symptoms/hour")
    print(f"Description: {result2['temporal_analysis']['velocity_description']}")
    print(f"Urgency: {result2['urgency_assessment']['urgency_level']}")
    if result2['top_prediction']:
        print(f"Top Prediction: {result2['top_prediction']['disease_name']}")
        print(f"Confidence: {result2['temporal_confidence']}%")
    
    print("\n✅ Temporal Analyzer Test Complete!")

if __name__ == "__main__":
    test_temporal_analyzer()
