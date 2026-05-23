#!/usr/bin/env python3
"""
Smart Local AI Verification System
Uses medical knowledge to verify ML predictions without external APIs
"""

# COMPREHENSIVE MEDICAL KNOWLEDGE BASE
DISEASE_VERIFICATION_RULES = {
    # Respiratory Diseases
    "Common Cold": {
        "key_symptoms": ["Sore Throat", "Cough", "Runny Nose"],
        "required_count": 2,
        "incompatible": ["Fever > 38.5C", "Severe Chest Pain"],
        "confidence": 0.85
    },
    "Pneumonia": {
        "key_symptoms": ["Cough", "Fever", "Shortness of Breath", "Chest Pain"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.9
    },
    "Bronchitis": {
        "key_symptoms": ["Cough", "Sore Throat", "Shortness of Breath"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.85
    },
    "Asthma": {
        "key_symptoms": ["Shortness of Breath", "Wheezing", "Chest Pain"],
        "required_count": 2,
        "incompatible": ["High Fever"],
        "confidence": 0.88
    },
    "Whooping Cough": {
        "key_symptoms": ["Cough", "Fever", "Sore Throat"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.82
    },
    
    # GI Diseases
    "Peptic Ulcer": {
        "key_symptoms": ["Abdominal Pain", "Nausea", "Vomiting"],
        "required_count": 2,
        "incompatible": ["Diarrhea"],
        "confidence": 0.8
    },
    "Gastroenteritis": {
        "key_symptoms": ["Abdominal Pain", "Diarrhea", "Nausea", "Fever"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.87
    },
    "Appendicitis": {
        "key_symptoms": ["Abdominal Pain", "Nausea", "Fever"],
        "required_count": 3,
        "incompatible": ["Diarrhea"],
        "confidence": 0.85
    },
    
    # Joint/Rheumatologic
    "Arthritis": {
        "key_symptoms": ["Joint Pain", "Body Ache", "Back Pain"],
        "required_count": 2,
        "incompatible": ["High Fever", "Cough"],
        "confidence": 0.9
    },
    "Rheumatoid Arthritis": {
        "key_symptoms": ["Joint Pain", "Body Ache", "Fever"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.88
    },
    "Gout": {
        "key_symptoms": ["Joint Pain", "Fever"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.85
    },
    "Osteoporosis": {
        "key_symptoms": ["Joint Pain", "Back Pain"],
        "required_count": 2,
        "incompatible": ["Fever"],
        "confidence": 0.82
    },
    
    # Neurological
    "Migraine": {
        "key_symptoms": ["Headache", "Dizziness", "Blurred Vision"],
        "required_count": 2,
        "incompatible": ["High Fever"],
        "confidence": 0.88
    },
    "Epilepsy": {
        "key_symptoms": ["Seizure", "Loss of Consciousness"],
        "required_count": 1,
        "incompatible": [],
        "confidence": 0.92
    },
    "Stroke": {
        "key_symptoms": ["Headache", "Dizziness", "Confusion", "Weakness"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.9
    },
    
    # Infection
    "Urinary Tract Infection": {
        "key_symptoms": ["Abdominal Pain", "Burning Urination"],
        "required_count": 1,
        "incompatible": ["Cough"],
        "confidence": 0.87
    },
    "Malaria": {
        "key_symptoms": ["Fever", "Chills", "Body Ache"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.89
    },
    "Typhoid": {
        "key_symptoms": ["Fever", "Abdominal Pain", "Body Ache"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.88
    },
    
    # Skin
    "Chickenpox": {
        "key_symptoms": ["Rash", "Fever", "Chills"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.9
    },
    "Measles": {
        "key_symptoms": ["Rash", "Fever", "Cough", "Sore Throat"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.91
    },
    "Psoriasis": {
        "key_symptoms": ["Rash", "Itching"],
        "required_count": 2,
        "incompatible": ["High Fever"],
        "confidence": 0.85
    },
    "Eczema": {
        "key_symptoms": ["Rash", "Itching"],
        "required_count": 2,
        "incompatible": ["High Fever"],
        "confidence": 0.83
    },
    
    # Circulatory
    "Heart Failure": {
        "key_symptoms": ["Chest Pain", "Shortness of Breath", "Dizziness"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.9
    },
    "High Blood Pressure": {
        "key_symptoms": ["Headache", "Dizziness"],
        "required_count": 1,
        "incompatible": [],
        "confidence": 0.75
    },
    "Anemia": {
        "key_symptoms": ["Dizziness", "Weakness", "Fatigue"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.82
    },
    "Leukemia": {
        "key_symptoms": ["Fever", "Body Ache", "Weakness"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.88
    },
    
    # Endocrine
    "Diabetes": {
        "key_symptoms": ["Weakness", "Frequent Urination", "Increased Thirst"],
        "required_count": 2,
        "incompatible": ["High Fever"],
        "confidence": 0.85
    },
    "Hyperthyroidism": {
        "key_symptoms": ["Weakness", "Dizziness", "Fever"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.8
    },
    "Hypothyroidism": {
        "key_symptoms": ["Weakness", "Dizziness", "Body Ache"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.78
    },
    
    # Mental Health
    "Depression": {
        "key_symptoms": ["Depression", "Weakness"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.75
    },
    "Anxiety": {
        "key_symptoms": ["Anxiety", "Dizziness"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.8
    },
    
    # Lyme & Vector
    "Lyme Disease": {
        "key_symptoms": ["Body Ache", "Rash", "Fever"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.87
    },
    "Dengue": {
        "key_symptoms": ["Fever", "Body Ache", "Chills"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.88
    },
    
    # Other
    "Pulmonary Embolism": {
        "key_symptoms": ["Chest Pain", "Shortness of Breath", "Dizziness"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.9
    },
    "Kidney Disease": {
        "key_symptoms": ["Abdominal Pain", "Fever"],
        "required_count": 2,
        "incompatible": [],
        "confidence": 0.8
    },
    "Liver Disease": {
        "key_symptoms": ["Fever", "Nausea", "Abdominal Pain"],
        "required_count": 3,
        "incompatible": [],
        "confidence": 0.85
    },
}

def verify_prediction_with_ai(disease_name: str, symptoms_list: list, ml_confidence: float) -> dict:
    """
    Smart local AI verification without external APIs
    
    Args:
        disease_name: Predicted disease name
        symptoms_list: List of symptom names from patient
        ml_confidence: Confidence score from ML models (0-100)
    
    Returns:
        dict with verification result
    """
    
    symptoms_lower = [s.lower() for s in symptoms_list]
    
    # If disease not in our knowledge base, allow but with lower confidence
    if disease_name not in DISEASE_VERIFICATION_RULES:
        return {
            "verified": True,
            "confidence": min(0.7, ml_confidence / 100),
            "explanation": f"Disease recognized but limited knowledge base data available",
            "missing_symptoms": [],
            "ai_approved": False,
            "reason": "Limited database"
        }
    
    rules = DISEASE_VERIFICATION_RULES[disease_name]
    key_symptoms = [s.lower() for s in rules["key_symptoms"]]
    required_count = rules["required_count"]
    incompatible_list = rules["incompatible"]
    base_confidence = rules["confidence"]
    
    # Check for key symptoms
    matching_symptoms = sum(1 for ks in key_symptoms if ks in symptoms_lower)
    
    # Check for incompatible symptoms
    incompatible_found = [s for s in incompatible_list if s.lower() in symptoms_lower]
    
    # Calculate verification
    verification_result = {
        "disease": disease_name,
        "symptoms_provided": len(symptoms_list),
        "key_symptoms_matched": matching_symptoms,
        "key_symptoms_required": required_count,
        "incompatible_symptoms": incompatible_found,
        "ml_confidence": ml_confidence
    }
    
    # AI Verification Logic
    if incompatible_found:
        # Incompatible symptoms detected - REJECT
        verification_result.update({
            "verified": False,
            "ai_approved": False,
            "confidence": 0.3,
            "explanation": f"Disease {disease_name} is INCOMPATIBLE with patient symptoms: {', '.join(incompatible_found)}",
            "reason": "Incompatible symptoms detected",
            "missing_symptoms": [s for s in rules["key_symptoms"] if s.lower() not in symptoms_lower]
        })
    elif matching_symptoms >= required_count:
        # All required symptoms present - APPROVE
        confidence = min(0.99, (base_confidence + (ml_confidence / 100)) / 2)
        verification_result.update({
            "verified": True,
            "ai_approved": True,
            "confidence": confidence,
            "explanation": f"✅ VERIFIED: {disease_name} matches patient symptoms. {matching_symptoms}/{required_count} key symptoms present.",
            "reason": "All required symptoms verified",
            "missing_symptoms": []
        })
    else:
        # Not enough key symptoms - PARTIAL or REJECT
        missing_count = required_count - matching_symptoms
        if matching_symptoms >= required_count - 1:
            # Close match - PARTIAL APPROVE
            confidence = min(0.85, (base_confidence * 0.8 + (ml_confidence / 100) * 0.2))
            verification_result.update({
                "verified": True,
                "ai_approved": True,
                "confidence": confidence,
                "explanation": f"⚠️ PARTIAL MATCH: {disease_name} likely, but missing {missing_count} key symptom(s): {', '.join([s for s in rules['key_symptoms'] if s.lower() not in symptoms_lower])}",
                "reason": f"Close match but missing {missing_count} key symptom(s)",
                "missing_symptoms": [s for s in rules["key_symptoms"] if s.lower() not in symptoms_lower]
            })
        else:
            # Poor match - REJECT
            missing_symptoms = [s for s in rules["key_symptoms"] if s.lower() not in symptoms_lower]
            verification_result.update({
                "verified": False,
                "ai_approved": False,
                "confidence": 0.4,
                "explanation": f"❌ REJECTED: {disease_name} does not match symptoms well. Missing {missing_count} key symptoms: {', '.join(missing_symptoms[:3])}",
                "reason": f"Missing {missing_count} required symptoms",
                "missing_symptoms": missing_symptoms
            })
    
    return verification_result


def get_alternate_predictions(disease_predictions: list, symptoms_list: list) -> list:
    """
    Try alternate predictions if first one is rejected
    Returns verified predictions sorted by confidence
    """
    verified_predictions = []
    
    for prediction in disease_predictions:
        disease_name = prediction.get("disease")
        ml_confidence = prediction.get("confidence", 50)
        
        verification = verify_prediction_with_ai(disease_name, symptoms_list, ml_confidence)
        
        if verification["verified"]:
            prediction_with_verification = {
                **prediction,
                "ai_verification": verification,
                "final_confidence": verification["confidence"],
                "ai_approved": verification["ai_approved"]
            }
            verified_predictions.append(prediction_with_verification)
    
    # Sort by final confidence
    verified_predictions.sort(key=lambda x: x["final_confidence"], reverse=True)
    return verified_predictions


if __name__ == "__main__":
    # Test the verification system
    print("Testing Smart AI Verification System\n")
    
    # Test 1: Good arthritis prediction
    result = verify_prediction_with_ai(
        "Arthritis",
        ["Joint Pain", "Body Ache", "Back Pain"],
        85
    )
    print(f"Test 1 - Arthritis with joint pain, body ache, back pain:")
    print(f"  Verified: {result['verified']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Reason: {result['reason']}\n")
    
    # Test 2: Bad prediction (heart failure for joint pain)
    result = verify_prediction_with_ai(
        "Heart Failure",
        ["Joint Pain"],
        70
    )
    print(f"Test 2 - Heart Failure with only joint pain:")
    print(f"  Verified: {result['verified']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Reason: {result['reason']}\n")
    
    # Test 3: Partial match (pneumonia with some symptoms)
    result = verify_prediction_with_ai(
        "Pneumonia",
        ["Cough", "Fever"],
        75
    )
    print(f"Test 3 - Pneumonia with cough and fever (missing chest pain):")
    print(f"  Verified: {result['verified']}")
    print(f"  Confidence: {result['confidence']:.2%}")
    print(f"  Reason: {result['reason']}\n")
