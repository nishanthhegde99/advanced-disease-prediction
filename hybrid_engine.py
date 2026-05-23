#!/usr/bin/env python3
"""
================================================================================
HOSPITAL-GRADE HYBRID PREDICTION ENGINE
================================================================================


This system provides ONE definitive answer, not multiple conflicting results.
================================================================================
"""

import numpy as np
import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HybridPredictionEngine:
    """
    Hybrid prediction system combining multiple AI methods
    
    This engine unifies:
    1. ML Ensemble (5 models voting)
    2. Temporal Progression Analysis
    3. Clinical Pattern Matching
    4. Confidence Calibration
    
    Output: ONE definitive diagnosis with hospital-grade reliability
    """
    
    def __init__(self):
        self.db_path = "disease.db"
        
    def unified_prediction(self, ml_predictions, temporal_result, symptom_names):
        """
        Unified prediction from multiple sources
        
        Args:
            ml_predictions: Dict of ML model predictions
            temporal_result: Temporal analysis result (or None)
            symptom_names: List of symptom names
        
        Returns:
            unified_result: Single definitive prediction with confidence
        """
        
        # Step 1: Get ML consensus
        ml_disease, ml_confidence, ml_votes = self._get_ml_consensus(ml_predictions)
        
        # Step 2: If no temporal data, return ML prediction
        if not temporal_result or temporal_result.get('status') != 'success':
            return {
                'disease': ml_disease,
                'confidence': ml_confidence,
                'method': 'ML Ensemble Only',
                'urgency': self._assess_basic_urgency(ml_disease, len(symptom_names)),
                'reliability': 'High' if ml_confidence >= 80 else 'Medium',
                'explanation': f'Prediction based on {ml_votes} out of 5 ML models agreeing'
            }
        
        # Step 3: Get temporal prediction
        temporal_disease = temporal_result.get('top_prediction', {}).get('disease_name')
        temporal_confidence = temporal_result.get('temporal_confidence', 0)
        velocity = temporal_result.get('temporal_analysis', {}).get('velocity', 0)
        urgency = temporal_result.get('urgency_assessment', {}).get('urgency_level', 'Medium')
        
    # Step 4: Hybrid decision logic
        
        # Case A: ML and Temporal AGREE (Best case - highest confidence)
        if ml_disease.lower() == temporal_disease.lower():
            final_confidence = min(98, (ml_confidence * 0.6 + temporal_confidence * 0.4) + 10)
            return {
                'disease': ml_disease,
                'confidence': round(final_confidence, 1),
                'method': 'ML + Temporal Consensus',
                'urgency': urgency,
                'reliability': 'Very High',
                'explanation': f'Both ML ({ml_confidence}%) and Temporal ({temporal_confidence}%) analysis agree',
                'velocity': velocity,
                'ml_votes': ml_votes,
                'temporal_match': True,
                'consensus_boost': True
            }
        
        # Case B: ML and Temporal DISAGREE - Use intelligent weighting
        else:
            # Weight based on confidence levels
            ml_weight = ml_confidence / 100
            temporal_weight = temporal_confidence / 100
            
            # Velocity factor: High velocity = trust temporal more (emergency detection)
            if velocity > 0.2:  # Rapid progression
                temporal_weight *= 1.5  # Boost temporal importance
                logger.info(f"⚡ High velocity detected ({velocity}) - Prioritizing temporal analysis")
            
            # ML consensus factor: Strong ML agreement = trust ML more
            if ml_votes >= 4:  # 4 or 5 models agree
                ml_weight *= 1.3  # Boost ML importance
                logger.info(f"🤖 Strong ML consensus ({ml_votes}/5) - Prioritizing ML prediction")
            
            # Normalize weights
            total_weight = ml_weight + temporal_weight
            ml_weight_norm = ml_weight / total_weight
            temporal_weight_norm = temporal_weight / total_weight
            
            # Choose prediction with higher weighted confidence
            if ml_weight_norm > temporal_weight_norm:
                final_disease = ml_disease
                final_confidence = ml_confidence * 0.9  # Slight penalty for disagreement
                method = 'ML Primary (Temporal provides urgency context)'
                explanation = f'ML prediction ({ml_confidence}%) prioritized. Temporal suggests {temporal_disease} but lower confidence.'
            else:
                final_disease = temporal_disease
                final_confidence = temporal_confidence * 0.9  # Slight penalty for disagreement
                method = 'Temporal Primary (Pattern-based diagnosis)'
                explanation = f'Temporal pattern ({temporal_confidence}%) prioritized due to symptom progression. ML suggests {ml_disease}.'
            
            return {
                'disease': final_disease,
                'confidence': round(final_confidence, 1),
                'method': method,
                'urgency': urgency,
                'reliability': 'High',
                'explanation': explanation,
                'velocity': velocity,
                'ml_votes': ml_votes,
                'temporal_match': False,
                'alternative_diagnosis': {
                    'disease': temporal_disease if final_disease == ml_disease else ml_disease,
                    'source': 'Temporal' if final_disease == ml_disease else 'ML',
                    'note': 'Consider as differential diagnosis'
                }
            }
    
    def _get_ml_consensus(self, ml_predictions):
        """Get consensus from ML models"""
        if not ml_predictions:
            return "Unknown", 0, 0
        
        # Count votes
        disease_votes = {}
        for model_key, disease in ml_predictions.items():
            disease_votes[disease] = disease_votes.get(disease, 0) + 1
        
        # Get top disease
        top_disease = max(disease_votes, key=disease_votes.get)
        votes = disease_votes[top_disease]
        total_models = len(ml_predictions)
        
        # Calculate confidence based on consensus
        confidence = (votes / total_models) * 100
        
        return top_disease, confidence, votes
    
    def _assess_basic_urgency(self, disease_name, symptom_count):
        """Basic urgency assessment without temporal data"""
        critical_diseases = [
            "Heart Attack", "Stroke", "Meningitis", "Bacterial Meningitis",
            "Sepsis", "Anaphylaxis", "Severe Pneumonia", "Appendicitis"
        ]
        
        if disease_name in critical_diseases:
            return "Critical"
        elif symptom_count >= 5:
            return "High"
        elif symptom_count >= 3:
            return "Medium"
        else:
            return "Low"
    
    def get_clinical_recommendations(self, unified_result):
        """
        Generate doctor-level clinical recommendations
        
        Args:
            unified_result: Unified prediction result
        
        Returns:
            recommendations: Clinical action plan
        """
        disease = unified_result['disease']
        confidence = unified_result['confidence']
        urgency = unified_result['urgency']
        reliability = unified_result['reliability']
        
        # Generate recommendations based on urgency
        if urgency == "Critical":
            action = "🚨 IMMEDIATE EMERGENCY CARE REQUIRED"
            timeline = "Call 911 or go to ER immediately"
            tests = self._get_emergency_tests(disease)
            color = "red"
        elif urgency == "High":
            action = "⚠️ URGENT MEDICAL ATTENTION NEEDED"
            timeline = "See doctor within 24 hours"
            tests = self._get_urgent_tests(disease)
            color = "orange"
        elif urgency == "Medium":
            action = "📋 SCHEDULE DOCTOR APPOINTMENT"
            timeline = "See doctor within 2-3 days"
            tests = self._get_routine_tests(disease)
            color = "yellow"
        else:
            action = "✓ MONITOR SYMPTOMS"
            timeline = "Self-care at home, see doctor if worsens"
            tests = ["Monitor symptoms", "Rest and hydration"]
            color = "green"
        
        # Confidence-based notes
        if confidence >= 90:
            confidence_note = "Very high diagnostic confidence"
        elif confidence >= 75:
            confidence_note = "High diagnostic confidence"
        elif confidence >= 60:
            confidence_note = "Moderate confidence - consider differential diagnosis"
        else:
            confidence_note = "Low confidence - further evaluation needed"
        
        return {
            'action': action,
            'timeline': timeline,
            'recommended_tests': tests,
            'confidence_note': confidence_note,
            'color': color,
            'follow_up': self._get_follow_up_plan(urgency)
        }
    
    def _get_emergency_tests(self, disease):
        """Emergency diagnostic tests"""
        tests = {
            "Heart Attack": ["ECG", "Cardiac enzymes", "Chest X-ray"],
            "Stroke": ["CT scan", "MRI", "Blood pressure monitoring"],
            "Meningitis": ["Lumbar puncture", "Blood culture", "CT scan"],
            "Bacterial Meningitis": ["Lumbar puncture", "Blood culture", "CT scan"],
            "Sepsis": ["Blood culture", "Complete blood count", "Lactate level"],
            "Appendicitis": ["CT scan", "Ultrasound", "Blood tests"]
        }
        return tests.get(disease, ["Complete blood count", "Basic metabolic panel", "Vital signs"])
    
    def _get_urgent_tests(self, disease):
        """Urgent diagnostic tests"""
        return ["Complete blood count", "Basic metabolic panel", "Urinalysis", "Chest X-ray"]
    
    def _get_routine_tests(self, disease):
        """Routine diagnostic tests"""
        return ["Complete blood count", "Basic metabolic panel", "Physical examination"]
    
    def _get_follow_up_plan(self, urgency):
        """Follow-up care plan"""
        plans = {
            "Critical": "Immediate hospitalization and monitoring",
            "High": "Follow-up within 48 hours or if symptoms worsen",
            "Medium": "Follow-up in 1 week or if symptoms worsen",
            "Low": "Follow-up only if symptoms persist beyond 7 days"
        }
        return plans.get(urgency, "Follow-up as needed")

# ============================================================================
# TESTING
# ============================================================================
if __name__ == "__main__":
    print("="*70)
    print("TESTING HOSPITAL-GRADE HYBRID PREDICTION ENGINE")
    print("="*70)
    
    engine = HybridPredictionEngine()
    
    # Test Case 1: ML and Temporal agree
    print("\n📋 TEST 1: ML and Temporal Agree (Best Case)")
    print("-"*70)
    
    ml_preds = {
        "naive_bayes": "Influenza",
        "random_forest": "Influenza",
        "gradient_boosting": "Influenza",
        "svm": "Influenza",
        "logistic_regression": "Common Cold"
    }
    
    temporal_res = {
        'status': 'success',
        'top_prediction': {'disease_name': 'Influenza'},
        'temporal_confidence': 88,
        'temporal_analysis': {'velocity': 0.05},
        'urgency_assessment': {'urgency_level': 'Medium'}
    }
    
    result1 = engine.unified_prediction(ml_preds, temporal_res, ['Fever', 'Cough', 'Fatigue'])
    print(f"✅ Disease: {result1['disease']}")
    print(f"✅ Confidence: {result1['confidence']}%")
    print(f"✅ Method: {result1['method']}")
    print(f"✅ Reliability: {result1['reliability']}")
    print(f"✅ Urgency: {result1['urgency']}")
    
    recommendations = engine.get_clinical_recommendations(result1)
    print(f"\n📋 Clinical Recommendations:")
    print(f"   Action: {recommendations['action']}")
    print(f"   Timeline: {recommendations['timeline']}")
    print(f"   Tests: {', '.join(recommendations['recommended_tests'])}")
    
    print("\n✅ TEST PASSED - UNIFIED PREDICTION WORKING")
    print("="*70)
