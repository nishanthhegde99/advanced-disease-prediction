import sqlite3
import requests
import json
import time

DB_PATH = 'disease.db'
API_URL = 'http://127.0.0.1:5001/predict'

def run_validation():
    print("🚀 Starting Advanced Hybrid System Validation...")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("SELECT id, name FROM disease")
    diseases = cur.fetchall()
    
    total_diseases = len(diseases)
    passed = 0
    failed = 0
    unknowns = 0
    
    results_log = []
    
    for d_id, d_name in diseases:
        cur.execute("SELECT symptom_id FROM disease_symptom WHERE disease_id=?", (d_id,))
        symptom_ids = [row[0] for row in cur.fetchall()]
        
        if not symptom_ids:
            continue
        
        # Prepare POST data (like a form submission)
        payload = [('symptom', str(sid)) for sid in symptom_ids]
        
        try:
            response = requests.post(API_URL, data=payload)
            result = response.json()
            
            if result.get("status") == "success":
                pred_disease = result["top_prediction"]["disease"]
                confidence = result["top_prediction"]["confidence"]
                trust = result.get("xai_validation", {}).get("trust_level", "Unknown")
                
                if pred_disease == d_name:
                    passed += 1
                    status = "✅ PASS"
                else:
                    failed += 1
                    status = f"❌ FAIL (Predicted: {pred_disease})"
                    
                results_log.append({
                    "disease": d_name,
                    "status": status,
                    "confidence": f"{confidence}%",
                    "trust": trust
                })
                
            elif result.get("status") == "unknown_case":
                unknowns += 1
                results_log.append({
                    "disease": d_name,
                    "status": "⚠️ UNKNOWN",
                    "confidence": "N/A (<30%)",
                    "trust": "N/A"
                })
            else:
                failed += 1
                results_log.append({
                    "disease": d_name,
                    "status": "❌ ERROR",
                    "confidence": "N/A",
                    "trust": "N/A"
                })
                
        except Exception as e:
            print(f"Error testing {d_name}: {e}")
            
    conn.close()
    
    # Save the output to a markdown artifact format
    with open('validation_results.json', 'w') as f:
        json.dump({
            "total": total_diseases,
            "passed": passed,
            "failed": failed,
            "unknowns": unknowns,
            "details": results_log
        }, f)
        
    print(f"\n📊 Validation Complete!")
    print(f"Total Tested: {total_diseases}")
    print(f"Passed: {passed} ({passed/total_diseases*100:.1f}%)")
    print(f"Failed: {failed}")
    print(f"Unknowns (Safe fallbacks): {unknowns}")

if __name__ == "__main__":
    run_validation()
