#!/usr/bin/env python3
"""
AI Integration Module
- Google Generative AI (Gemini) for disease explanations
- Fallback to local knowledge base
- Patient-friendly explanations
"""

import os
from dotenv import load_dotenv
import json

load_dotenv()

class AIHealthAdvisor:
    """AI-powered health advisor for disease explanations and recommendations"""
    
    def __init__(self):
        self.use_google_api = False
        self.use_openai = False
        
        # Try to initialize Google API
        try:
            import google.generativeai as genai
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.google_model = genai.GenerativeModel('gemini-pro')
                self.use_google_api = True
                print("✅ Google Generative AI initialized")
        except Exception as e:
            print(f"⚠️ Google API not available: {e}")
        
        # Try to initialize OpenAI
        try:
            import openai
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self.use_openai = True
                print("✅ OpenAI API initialized")
        except Exception as e:
            print(f"⚠️ OpenAI API not available: {e}")
        
        # Load local knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load local disease knowledge base"""
        return {
            "Common Cold": {
                "explanation": "A viral infection affecting the upper respiratory tract, causing mild symptoms.",
                "precautions": [
                    "Get adequate rest (7-9 hours sleep)",
                    "Stay hydrated - drink water, warm tea, or soup",
                    "Use saline nasal drops for congestion",
                    "Avoid smoking and secondhand smoke",
                    "Wash hands frequently"
                ],
                "diet": [
                    "Vitamin C rich foods: oranges, kiwi, strawberries",
                    "Warm liquids: chicken soup, herbal tea",
                    "Honey and ginger for throat soothing",
                    "Avoid dairy if congested"
                ],
                "severity": "Low"
            },
            "Influenza": {
                "explanation": "A contagious respiratory illness caused by influenza virus, more severe than common cold.",
                "precautions": [
                    "Get flu vaccination annually",
                    "Maintain distance from infected persons",
                    "Wear masks in crowded places",
                    "Practice respiratory hygiene",
                    "Seek medical attention if symptoms worsen"
                ],
                "diet": [
                    "Protein-rich foods for immune support",
                    "Fruits and vegetables with antioxidants",
                    "Warm broths and soups",
                    "Avoid alcohol and caffeine"
                ],
                "severity": "Medium"
            },
            "Migraine": {
                "explanation": "A neurological condition characterized by intense, debilitating headaches often with visual disturbances.",
                "precautions": [
                    "Identify and avoid triggers (stress, certain foods, lack of sleep)",
                    "Maintain regular sleep schedule",
                    "Stay hydrated throughout the day",
                    "Practice stress management techniques",
                    "Limit screen time"
                ],
                "diet": [
                    "Avoid trigger foods: chocolate, aged cheese, processed meats",
                    "Magnesium-rich foods: almonds, spinach, pumpkin seeds",
                    "Regular meal timing to avoid skipping meals",
                    "Limit caffeine intake"
                ],
                "severity": "Medium"
            },
            "Diabetes Type 2": {
                "explanation": "A metabolic disorder where the body cannot effectively use insulin, leading to high blood sugar.",
                "precautions": [
                    "Monitor blood sugar regularly",
                    "Exercise 150 minutes per week",
                    "Maintain healthy weight",
                    "Manage stress levels",
                    "Regular medical check-ups"
                ],
                "diet": [
                    "Low glycemic index foods",
                    "Whole grains instead of refined carbs",
                    "Lean proteins: fish, chicken, legumes",
                    "Plenty of vegetables and limited fruits",
                    "Avoid sugary drinks and processed foods"
                ],
                "severity": "High"
            },
            "Hypertension": {
                "explanation": "High blood pressure that can lead to serious complications if not managed.",
                "precautions": [
                    "Monitor blood pressure regularly",
                    "Reduce sodium intake",
                    "Exercise regularly",
                    "Maintain healthy weight",
                    "Limit alcohol consumption",
                    "Manage stress"
                ],
                "diet": [
                    "DASH diet: fruits, vegetables, whole grains",
                    "Low sodium foods",
                    "Potassium-rich foods: bananas, sweet potatoes",
                    "Lean proteins",
                    "Limit processed foods"
                ],
                "severity": "High"
            },
            "Anxiety Disorder": {
                "explanation": "A mental health condition characterized by persistent worry and fear affecting daily life.",
                "precautions": [
                    "Practice meditation and mindfulness",
                    "Regular exercise (30 minutes daily)",
                    "Maintain consistent sleep schedule",
                    "Limit caffeine and alcohol",
                    "Seek professional counseling",
                    "Build strong social connections"
                ],
                "diet": [
                    "Omega-3 rich foods: salmon, walnuts",
                    "Complex carbohydrates for serotonin",
                    "Magnesium-rich foods",
                    "Avoid excessive caffeine",
                    "Stay hydrated"
                ],
                "severity": "Medium"
            },
            "Arthritis": {
                "explanation": "Inflammation of joints causing pain, stiffness, and reduced mobility.",
                "precautions": [
                    "Maintain healthy weight to reduce joint stress",
                    "Regular low-impact exercise: swimming, walking",
                    "Apply heat/cold therapy as needed",
                    "Use proper ergonomics",
                    "Avoid repetitive strain"
                ],
                "diet": [
                    "Anti-inflammatory foods: fatty fish, berries",
                    "Turmeric and ginger for inflammation",
                    "Whole grains and legumes",
                    "Avoid processed foods and excess sugar",
                    "Stay hydrated"
                ],
                "severity": "Medium"
            }
        }
    
    def get_disease_explanation(self, disease_name):
        """Get patient-friendly disease explanation"""
        
        # Try API first if available
        if self.use_google_api:
            try:
                prompt = f"""Provide a simple, patient-friendly explanation of {disease_name} in 2-3 sentences. 
                Avoid medical jargon. Focus on what the patient needs to know."""
                response = self.google_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"API error: {e}")
        
        # Fallback to knowledge base
        if disease_name in self.knowledge_base:
            return self.knowledge_base[disease_name]["explanation"]
        
        return f"{disease_name} is a medical condition. Please consult a healthcare professional for detailed information."
    
    def get_precautions(self, disease_name):
        """Get precautions and preventive measures"""
        
        # Try API first
        if self.use_google_api:
            try:
                prompt = f"""List 5 practical precautions and preventive measures for {disease_name}. 
                Format as bullet points. Keep language simple and actionable."""
                response = self.google_model.generate_content(prompt)
                return response.text.split('\n')
            except Exception as e:
                print(f"API error: {e}")
        
        # Fallback to knowledge base
        if disease_name in self.knowledge_base:
            precautions = self.knowledge_base[disease_name]["precautions"]
            return [f"• {p}" for p in precautions]
        
        return ["• Consult a healthcare professional", "• Follow medical advice", "• Regular check-ups"]
    
    def get_diet_recommendations(self, disease_name):
        """Get diet recommendations"""
        
        # Try API first
        if self.use_google_api:
            try:
                prompt = f"""Provide 5 diet recommendations for someone with {disease_name}. 
                Include foods to eat and foods to avoid. Keep it practical and simple."""
                response = self.google_model.generate_content(prompt)
                return response.text.split('\n')
            except Exception as e:
                print(f"API error: {e}")
        
        # Fallback to knowledge base
        if disease_name in self.knowledge_base:
            diet = self.knowledge_base[disease_name]["diet"]
            return [f"• {d}" for d in diet]
        
        return ["• Eat balanced meals", "• Stay hydrated", "• Consult a nutritionist"]
    
    def get_lifestyle_changes(self, disease_name):
        """Get lifestyle change recommendations"""
        
        # Try API first
        if self.use_google_api:
            try:
                prompt = f"""Suggest 5 lifestyle changes that can help manage {disease_name}. 
                Include exercise, sleep, stress management, and daily habits."""
                response = self.google_model.generate_content(prompt)
                return response.text.split('\n')
            except Exception as e:
                print(f"API error: {e}")
        
        # Fallback recommendations
        return [
            "• Exercise regularly (30 minutes daily)",
            "• Maintain consistent sleep schedule (7-9 hours)",
            "• Practice stress management techniques",
            "• Avoid smoking and limit alcohol",
            "• Regular medical check-ups"
        ]
    
    def get_severity_alert(self, disease_name, symptoms_count):
        """Determine if immediate medical attention is needed"""
        
        critical_diseases = [
            "Heart Attack", "Stroke", "Meningitis", "Sepsis", 
            "Pulmonary Embolism", "Acute Kidney Injury", "Rabies"
        ]
        
        severe_diseases = [
            "Pneumonia", "Tuberculosis", "Encephalitis", "Appendicitis",
            "Deep Vein Thrombosis", "Severe Asthma"
        ]
        
        if disease_name in critical_diseases:
            return {
                "level": "CRITICAL",
                "message": "🚨 IMMEDIATE MEDICAL ATTENTION REQUIRED - Call emergency services immediately!",
                "action": "Go to nearest hospital emergency room"
            }
        elif disease_name in severe_diseases:
            return {
                "level": "SEVERE",
                "message": "⚠️ Urgent medical attention recommended - Seek doctor immediately",
                "action": "Visit hospital or urgent care center today"
            }
        elif symptoms_count >= 4:
            return {
                "level": "MODERATE",
                "message": "⚠️ Multiple symptoms detected - Schedule doctor appointment soon",
                "action": "Contact your doctor within 24-48 hours"
            }
        else:
            return {
                "level": "LOW",
                "message": "ℹ️ Monitor symptoms - Consult doctor if symptoms persist",
                "action": "Schedule routine appointment if needed"
            }

# Initialize global advisor
advisor = AIHealthAdvisor()

def get_ai_insights(disease_name, symptoms_count=1):
    """Get comprehensive AI insights for a disease"""
    return {
        "explanation": advisor.get_disease_explanation(disease_name),
        "precautions": advisor.get_precautions(disease_name),
        "diet": advisor.get_diet_recommendations(disease_name),
        "lifestyle": advisor.get_lifestyle_changes(disease_name),
        "severity": advisor.get_severity_alert(disease_name, symptoms_count)
    }
