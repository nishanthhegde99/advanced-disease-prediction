#!/usr/bin/env python3
"""
Expand the local disease prediction dataset.

This dataset is for clinical decision-support demos only. It stores common
symptom associations and medicine options with OTC/Rx flags, not dosing or
patient-specific treatment instructions.
"""

import sqlite3


DB_PATH = "disease.db"


SYMPTOMS = [
    "Jaundice",
    "Dark Urine",
    "Pale Stool",
    "Burning Urination",
    "Pelvic Pain",
    "Blood in Urine",
    "Flank Pain",
    "Leg Swelling",
    "Calf Pain",
    "Red Eye",
    "Eye Discharge",
    "Photophobia",
    "Facial Pain",
    "Nasal Congestion",
    "Postnasal Drip",
    "Loss of Consciousness",
    "Seizure",
    "Tremor",
    "Memory Loss",
    "Speech Difficulty",
    "Facial Droop",
    "Severe Headache",
    "Stiff Neck",
    "Palpitations",
    "Syncope",
    "Orthopnea",
    "Productive Cough",
    "Bloody Sputum",
    "Burning Chest Pain",
    "Regurgitation",
    "Bloating",
    "Blood in Stool",
    "Rectal Pain",
    "Rectal Bleeding",
    "Painful Defecation",
    "Yellow Sputum",
    "Ear Discharge",
    "Hearing Loss",
    "Tooth Pain",
    "Gum Swelling",
    "Mouth Ulcers",
    "Vaginal Discharge",
    "Vaginal Itching",
    "Irregular Periods",
    "Heavy Menstrual Bleeding",
    "Testicular Pain",
    "Erectile Dysfunction",
    "Snoring",
    "Daytime Sleepiness",
    "Loud Breathing During Sleep",
    "High Blood Sugar",
    "Low Blood Sugar",
    "Cold Intolerance",
    "Heat Intolerance",
    "Hair Loss",
    "Dry Skin",
    "Weight Gain",
    "Trembling",
    "Panic Attacks",
    "Hallucinations",
    "Mood Swings",
    "Suicidal Thoughts",
    "Poor Concentration",
    "Left Arm Pain",
    "Severe Pain",
    "Back Stiffness",
    "Morning Stiffness",
    "Photosensitivity",
    "Malar Rash",
    "Pustules",
    "Skin Peeling",
    "Burning Skin Pain",
    "Wound Drainage",
    "Swollen Lymph Nodes",
    "Joint Swelling",
    "Limited Range of Motion",
    "Easy Bruising",
    "Bleeding Gums",
    "Nosebleed",
    "Dehydration",
    "Rapid Breathing",
    "Blue Lips",
    "Poor Feeding",
    "Chest Tightness",
    "Exercise Intolerance",
    "Right Upper Abdominal Pain",
    "Left Lower Abdominal Pain",
]


MEDICINES = [
    ("Acetaminophen", "OTC pain/fever reliever. Avoid overdose and use caution with liver disease.", 0),
    ("Oral Rehydration Salts", "OTC fluid and electrolyte replacement for dehydration risk.", 0),
    ("Normal Saline IV", "Hospital-administered fluid therapy when clinically indicated.", 1),
    ("Ondansetron", "Prescription antiemetic; use only under clinician guidance.", 1),
    ("Oseltamivir", "Prescription antiviral; most useful when started early for influenza.", 1),
    ("Nirmatrelvir/Ritonavir", "Prescription antiviral for eligible COVID-19 patients; interaction screening required.", 1),
    ("Remdesivir", "Hospital prescription antiviral for selected patients.", 1),
    ("Dexamethasone", "Prescription corticosteroid; used only for specific indications.", 1),
    ("Budesonide/Formoterol Inhaler", "Prescription controller/reliever inhaler for selected asthma/COPD plans.", 1),
    ("Tiotropium", "Prescription inhaled bronchodilator for COPD/asthma maintenance.", 1),
    ("Benzonatate", "Prescription cough suppressant; swallow capsules whole.", 1),
    ("Guaifenesin", "OTC expectorant; maintain hydration.", 0),
    ("Pseudoephedrine", "OTC/behind-counter decongestant; avoid in uncontrolled hypertension unless approved.", 0),
    ("Saline Nasal Spray", "OTC nasal moisture and congestion support.", 0),
    ("Fluticasone Nasal Spray", "OTC/Rx nasal steroid for allergic rhinitis/sinus inflammation.", 0),
    ("Loratadine", "OTC antihistamine for allergy symptoms.", 0),
    ("Fexofenadine", "OTC antihistamine for allergy symptoms.", 0),
    ("Ketotifen Eye Drops", "OTC allergy eye drops.", 0),
    ("Artificial Tears", "OTC lubricating eye drops.", 0),
    ("Trimethoprim/Sulfamethoxazole", "Prescription antibiotic; allergy and resistance review required.", 1),
    ("Nitrofurantoin", "Prescription antibiotic commonly used for uncomplicated UTI when appropriate.", 1),
    ("Fosfomycin", "Prescription antibiotic option for selected uncomplicated UTI cases.", 1),
    ("Ceftriaxone", "Prescription injectable antibiotic; clinician-administered.", 1),
    ("Metronidazole", "Prescription antimicrobial; avoid alcohol during therapy and shortly after.", 1),
    ("Fluconazole", "Prescription antifungal; pregnancy and interaction review required.", 1),
    ("Clotrimazole Cream", "OTC antifungal for selected superficial fungal infections.", 0),
    ("Terbinafine Cream", "OTC antifungal for athlete's foot/ringworm.", 0),
    ("Acyclovir", "Prescription antiviral for herpes-family infections when indicated.", 1),
    ("Valacyclovir", "Prescription antiviral for herpes-family infections when indicated.", 1),
    ("Permethrin Cream", "Prescription/OTC scabicide depending on region; household contact management needed.", 1),
    ("Benzoyl Peroxide", "OTC acne treatment; may bleach fabrics and irritate skin.", 0),
    ("Clindamycin Gel", "Prescription topical antibiotic for acne/skin infection plans.", 1),
    ("Doxycycline Acne Course", "Prescription antibiotic for selected acne; avoid in pregnancy/young children.", 1),
    ("Isotretinoin", "Strictly controlled prescription acne medicine; pregnancy prevention program required.", 1),
    ("Mupirocin Ointment", "Prescription topical antibiotic for selected bacterial skin infections.", 1),
    ("Vancomycin", "Hospital prescription antibiotic for serious resistant infections.", 1),
    ("Piperacillin/Tazobactam", "Hospital prescription broad-spectrum antibiotic.", 1),
    ("Meropenem", "Hospital prescription broad-spectrum antibiotic.", 1),
    ("Epinephrine Auto-Injector", "Prescription emergency treatment for anaphylaxis; call emergency services after use.", 1),
    ("Naloxone", "Emergency opioid reversal medicine; seek urgent medical care after use.", 1),
    ("Compression Stockings", "Compression support for selected leg swelling/venous disease; fit and contraindications should be reviewed.", 0),
    ("Aspirin Emergency Use", "Emergency antiplatelet for suspected heart attack only if medically appropriate.", 0),
    ("Nitroglycerin", "Prescription medicine for angina; avoid with PDE5 inhibitors.", 1),
    ("Metoprolol", "Prescription beta blocker; monitor heart rate and blood pressure.", 1),
    ("Apixaban", "Prescription anticoagulant; bleeding risk and renal dosing review required.", 1),
    ("Rivaroxaban", "Prescription anticoagulant; bleeding risk and renal dosing review required.", 1),
    ("Heparin", "Hospital prescription anticoagulant.", 1),
    ("Alteplase", "Hospital thrombolytic for selected stroke/PE/MI cases.", 1),
    ("Levetiracetam", "Prescription antiseizure medicine.", 1),
    ("Lamotrigine", "Prescription antiseizure/mood stabilizing medicine; rash monitoring required.", 1),
    ("Carbidopa/Levodopa", "Prescription Parkinson's therapy.", 1),
    ("Donepezil", "Prescription cognitive symptom therapy for selected dementia patients.", 1),
    ("Sertraline", "Prescription antidepressant; monitor mood changes.", 1),
    ("Fluoxetine", "Prescription antidepressant; monitor mood changes.", 1),
    ("Escitalopram", "Prescription antidepressant/anxiety medicine.", 1),
    ("Lorazepam", "Prescription sedative; dependence and sedation risk.", 1),
    ("Lithium", "Prescription mood stabilizer; blood level and kidney/thyroid monitoring required.", 1),
    ("Risperidone", "Prescription antipsychotic; metabolic and movement side effect monitoring required.", 1),
    ("Melatonin", "OTC sleep support; use cautiously with sedating medicines.", 0),
    ("CPAP Therapy", "Device therapy requiring sleep evaluation and prescription setup.", 1),
    ("Tamsulosin", "Prescription medicine for BPH/urinary stone symptom management.", 1),
    ("Finasteride", "Prescription medicine for BPH; pregnancy handling precautions.", 1),
    ("Sildenafil", "Prescription ED medicine; avoid with nitrates.", 1),
    ("Allopurinol", "Prescription urate-lowering medicine; not for sudden pain relief.", 1),
    ("Colchicine", "Prescription gout flare medicine; interaction and kidney dosing review required.", 1),
    ("Calcium/Vitamin D", "OTC bone health supplement when appropriate.", 0),
    ("Alendronate", "Prescription osteoporosis medicine; administration instructions are important.", 1),
    ("Hydroxychloroquine", "Prescription autoimmune disease medicine; eye monitoring required.", 1),
    ("Adalimumab", "Prescription biologic; infection screening required.", 1),
    ("Insulin Glargine", "Prescription long-acting insulin; glucose monitoring required.", 1),
    ("Glucagon", "Prescription emergency treatment for severe hypoglycemia.", 1),
    ("Empagliflozin", "Prescription diabetes/heart-kidney medicine; dehydration and ketoacidosis risk review.", 1),
    ("Semaglutide", "Prescription GLP-1 therapy; contraindication screening required.", 1),
    ("Methimazole", "Prescription antithyroid medicine; urgent review for fever/sore throat.", 1),
    ("Hydrocortisone", "Prescription steroid replacement/stress dosing may be lifesaving in adrenal insufficiency.", 1),
    ("Ursodeoxycholic Acid", "Prescription bile acid therapy for selected hepatobiliary disease.", 1),
    ("Lactulose", "Prescription/OTC depending on region; used for constipation or hepatic encephalopathy plans.", 1),
    ("Polyethylene Glycol", "OTC laxative for constipation.", 0),
    ("Loperamide", "OTC antidiarrheal; avoid with bloody diarrhea or high fever unless clinician approves.", 0),
    ("Mesalamine", "Prescription inflammatory bowel disease therapy.", 1),
    ("Pancreatic Enzymes", "Prescription enzyme replacement when indicated.", 1),
    ("Topical Lidocaine", "OTC/Rx local pain relief depending on strength.", 0),
    ("Hydrocortisone Rectal Cream", "OTC/Rx hemorrhoid symptom relief depending on strength.", 0),
    ("Psyllium Fiber", "OTC fiber supplement.", 0),
]


DISEASES = {
    "COVID-19": {
        "symptoms": ["Fever", "Cough", "Fatigue", "Shortness of Breath", "Loss of Smell", "Loss of Taste", "Sore Throat", "Nasal Congestion", "Body Ache"],
        "medicines": ["Acetaminophen", "Oral Rehydration Salts", "Nirmatrelvir/Ritonavir", "Remdesivir", "Dexamethasone", "Saline Nasal Spray"],
    },
    "RSV Infection": {
        "symptoms": ["Cough", "Runny Nose", "Wheezing", "Fever", "Poor Feeding", "Rapid Breathing", "Blue Lips"],
        "medicines": ["Acetaminophen", "Oral Rehydration Salts", "Normal Saline IV"],
    },
    "Strep Throat": {
        "symptoms": ["Fever", "Sore Throat", "Difficulty Swallowing", "Swollen Lymph Nodes", "Headache"],
        "medicines": ["Acetaminophen", "Throat Lozenges", "Amoxicillin", "Cephalexin", "Azithromycin"],
    },
    "Acute Otitis Externa": {
        "symptoms": ["Ear Pain", "Ear Discharge", "Itching", "Hearing Loss"],
        "medicines": ["Acetaminophen", "Ciprofloxacin", "Hydrocortisone"],
    },
    "Dental Abscess": {
        "symptoms": ["Tooth Pain", "Gum Swelling", "Fever", "Facial Pain", "Swollen Lymph Nodes"],
        "medicines": ["Acetaminophen", "Ibuprofen", "Amoxicillin", "Metronidazole"],
    },
    "Bacterial Vaginosis": {
        "symptoms": ["Vaginal Discharge", "Vaginal Itching", "Pelvic Pain"],
        "medicines": ["Metronidazole", "Clindamycin Gel"],
    },
    "Vaginal Candidiasis": {
        "symptoms": ["Vaginal Itching", "Vaginal Discharge", "Burning Urination"],
        "medicines": ["Clotrimazole Cream", "Fluconazole"],
    },
    "Chlamydia": {
        "symptoms": ["Burning Urination", "Pelvic Pain", "Vaginal Discharge", "Testicular Pain"],
        "medicines": ["Doxycycline", "Azithromycin"],
    },
    "Gonorrhea": {
        "symptoms": ["Burning Urination", "Pelvic Pain", "Vaginal Discharge", "Testicular Pain"],
        "medicines": ["Ceftriaxone", "Doxycycline"],
    },
    "Syphilis": {
        "symptoms": ["Rash", "Swollen Lymph Nodes", "Mouth Ulcers", "Fatigue"],
        "medicines": ["Ceftriaxone", "Doxycycline"],
    },
    "Pelvic Inflammatory Disease": {
        "symptoms": ["Pelvic Pain", "Fever", "Vaginal Discharge", "Abdominal Pain", "Nausea"],
        "medicines": ["Ceftriaxone", "Doxycycline", "Metronidazole"],
    },
    "Pyelonephritis": {
        "symptoms": ["Fever", "Flank Pain", "Burning Urination", "Nausea", "Vomiting", "Chills"],
        "medicines": ["Ceftriaxone", "Ciprofloxacin", "Trimethoprim/Sulfamethoxazole", "Oral Rehydration Salts"],
    },
    "Benign Prostatic Hyperplasia": {
        "symptoms": ["Frequent Urination", "Burning Urination", "Weakness", "Insomnia"],
        "medicines": ["Tamsulosin", "Finasteride"],
    },
    "Erectile Dysfunction": {
        "symptoms": ["Erectile Dysfunction", "Anxiety", "Depression"],
        "medicines": ["Sildenafil"],
    },
    "Sleep Apnea": {
        "symptoms": ["Snoring", "Daytime Sleepiness", "Loud Breathing During Sleep", "Fatigue", "Headache"],
        "medicines": ["CPAP Therapy"],
    },
    "Hyperlipidemia": {
        "symptoms": ["Chest Pain", "Dizziness", "Fatigue"],
        "medicines": ["Atorvastatin", "Simvastatin", "Omega-3 Supplements"],
    },
    "Hypoglycemia": {
        "symptoms": ["Sweating", "Trembling", "Anxiety", "Dizziness", "Confusion", "Low Blood Sugar"],
        "medicines": ["Oral Rehydration Salts", "Glucagon"],
    },
    "Diabetic Ketoacidosis": {
        "symptoms": ["High Blood Sugar", "Excessive Thirst", "Frequent Urination", "Vomiting", "Abdominal Pain", "Confusion", "Rapid Breathing"],
        "medicines": ["Insulin", "Normal Saline IV", "Electrolyte Solution"],
    },
    "Gallstones": {
        "symptoms": ["Right Upper Abdominal Pain", "Nausea", "Vomiting", "Back Pain", "Jaundice"],
        "medicines": ["Acetaminophen", "Ibuprofen", "Ursodeoxycholic Acid"],
    },
    "Acute Pancreatitis": {
        "symptoms": ["Abdominal Pain", "Nausea", "Vomiting", "Fever", "Rapid Heartbeat", "Back Pain"],
        "medicines": ["Normal Saline IV", "Ondansetron", "Morphine"],
    },
    "Diverticulitis": {
        "symptoms": ["Left Lower Abdominal Pain", "Fever", "Nausea", "Constipation", "Diarrhea"],
        "medicines": ["Acetaminophen", "Amoxicillin", "Metronidazole", "Ondansetron"],
    },
    "Hemorrhoids": {
        "symptoms": ["Rectal Pain", "Rectal Bleeding", "Itching", "Painful Defecation"],
        "medicines": ["Hydrocortisone Rectal Cream", "Psyllium Fiber", "Topical Lidocaine"],
    },
    "Constipation Disorder": {
        "symptoms": ["Constipation", "Bloating", "Abdominal Pain", "Painful Defecation"],
        "medicines": ["Polyethylene Glycol", "Psyllium Fiber"],
    },
    "Anaphylaxis": {
        "symptoms": ["Shortness of Breath", "Wheezing", "Swelling", "Rash", "Dizziness", "Rapid Heartbeat"],
        "medicines": ["Epinephrine Auto-Injector", "Normal Saline IV", "Dexamethasone"],
    },
    "Opioid Overdose": {
        "symptoms": ["Loss of Consciousness", "Confusion", "Blue Lips", "Rapid Breathing"],
        "medicines": ["Naloxone"],
    },
    "Acute Coronary Syndrome": {
        "symptoms": ["Chest Pain", "Shortness of Breath", "Sweating", "Nausea", "Left Arm Pain", "Dizziness"],
        "medicines": ["Aspirin Emergency Use", "Nitroglycerin", "Heparin", "Atorvastatin", "Metoprolol"],
    },
    "Transient Ischemic Attack": {
        "symptoms": ["Speech Difficulty", "Facial Droop", "Weakness", "Numbness", "Dizziness", "Blurred Vision"],
        "medicines": ["Aspirin Emergency Use", "Clopidogrel", "Atorvastatin"],
    },
    "Atrial Fibrillation": {
        "symptoms": ["Palpitations", "Dizziness", "Shortness of Breath", "Fatigue", "Syncope"],
        "medicines": ["Metoprolol", "Apixaban", "Rivaroxaban", "Warfarin"],
    },
    "Venous Insufficiency": {
        "symptoms": ["Leg Swelling", "Skin Discoloration", "Itching", "Calf Pain"],
        "medicines": ["Compression Stockings", "Moisturizer"],
    },
    "Major Depressive Disorder": {
        "symptoms": ["Depression", "Insomnia", "Fatigue", "Poor Concentration", "Suicidal Thoughts", "Loss of Appetite"],
        "medicines": ["Sertraline", "Fluoxetine", "Escitalopram"],
    },
    "Panic Disorder": {
        "symptoms": ["Panic Attacks", "Anxiety", "Rapid Heartbeat", "Sweating", "Shortness of Breath", "Chest Pain"],
        "medicines": ["Sertraline", "Escitalopram", "Lorazepam"],
    },
    "Bipolar Disorder": {
        "symptoms": ["Mood Swings", "Insomnia", "Anxiety", "Poor Concentration", "Depression"],
        "medicines": ["Lithium", "Lamotrigine", "Risperidone"],
    },
    "Schizophrenia": {
        "symptoms": ["Hallucinations", "Confusion", "Anxiety", "Insomnia", "Poor Concentration"],
        "medicines": ["Risperidone"],
    },
    "Insomnia Disorder": {
        "symptoms": ["Insomnia", "Fatigue", "Anxiety", "Poor Concentration"],
        "medicines": ["Melatonin"],
    },
    "Herpes Simplex": {
        "symptoms": ["Mouth Ulcers", "Burning Skin Pain", "Swollen Lymph Nodes", "Fever"],
        "medicines": ["Acyclovir", "Valacyclovir", "Topical Lidocaine"],
    },
    "Impetigo": {
        "symptoms": ["Rash", "Itching", "Wound Drainage", "Skin Peeling"],
        "medicines": ["Mupirocin Ointment", "Cephalexin"],
    },
    "Seborrheic Dermatitis": {
        "symptoms": ["Itching", "Skin Peeling", "Rash"],
        "medicines": ["Coal Tar Shampoo", "Hydrocortisone Cream"],
    },
    "Severe Allergic Rhinitis": {
        "symptoms": ["Sneezing", "Runny Nose", "Nasal Congestion", "Watery Eyes", "Itching"],
        "medicines": ["Loratadine", "Fexofenadine", "Fluticasone Nasal Spray", "Ketotifen Eye Drops"],
    },
    "Scleroderma": {
        "symptoms": ["Skin Discoloration", "Joint Pain", "Shortness of Breath", "Difficulty Swallowing", "Cold Intolerance"],
        "medicines": ["Hydroxychloroquine", "Methotrexate"],
    },
    "Sickle Cell Crisis": {
        "symptoms": ["Severe Pain", "Chest Pain", "Shortness of Breath", "Fever", "Swelling", "Fatigue"],
        "medicines": ["Acetaminophen", "Morphine", "Normal Saline IV", "Folic Acid"],
    },
}


EXTRA_EXISTING_MAPPINGS = {
    "Common Cold": {
        "add_symptoms": ["Nasal Congestion", "Postnasal Drip"],
        "remove_medicines": ["Doxycycline", "Amoxicillin", "Azithromycin", "Ciprofloxacin"],
        "add_medicines": ["Acetaminophen", "Saline Nasal Spray", "Guaifenesin", "Honey", "Throat Lozenges"],
    },
    "Influenza": {
        "add_symptoms": ["Nasal Congestion", "Productive Cough"],
        "add_medicines": ["Oseltamivir", "Acetaminophen", "Guaifenesin"],
    },
    "Dengue Fever": {
        "remove_medicines": ["Ibuprofen", "Aspirin", "Naproxen", "Diclofenac"],
        "add_symptoms": ["Bleeding Gums", "Nosebleed", "Severe Headache"],
        "add_medicines": ["Acetaminophen", "Oral Rehydration Salts"],
    },
    "Hypotension": {
        "remove_medicines": ["Amlodipine", "Atenolol", "Lisinopril", "Losartan"],
        "add_symptoms": ["Syncope", "Dehydration"],
        "add_medicines": ["Oral Rehydration Salts", "Normal Saline IV"],
    },
    "Urinary Tract Infection": {
        "add_symptoms": ["Burning Urination", "Pelvic Pain", "Blood in Urine", "Frequent Urination"],
        "add_medicines": ["Nitrofurantoin", "Fosfomycin", "Trimethoprim/Sulfamethoxazole"],
    },
    "Kidney Stones": {
        "add_symptoms": ["Flank Pain", "Blood in Urine", "Burning Urination"],
        "add_medicines": ["Acetaminophen", "Ibuprofen", "Tamsulosin", "Ondansetron"],
    },
    "GERD": {
        "add_symptoms": ["Burning Chest Pain", "Regurgitation", "Bloating"],
        "add_medicines": ["Pantoprazole", "Omeprazole", "Antacid Tablet"],
    },
    "COPD": {
        "add_symptoms": ["Productive Cough", "Wheezing", "Chest Tightness", "Exercise Intolerance"],
        "add_medicines": ["Tiotropium", "Budesonide/Formoterol Inhaler", "Albuterol", "Guaifenesin"],
    },
    "Heart Failure": {
        "add_symptoms": ["Leg Swelling", "Orthopnea", "Exercise Intolerance"],
        "add_medicines": ["Furosemide", "Spironolactone", "Carvedilol", "Lisinopril", "Empagliflozin"],
    },
    "Stroke": {
        "add_symptoms": ["Speech Difficulty", "Facial Droop", "Loss of Consciousness", "Severe Headache"],
        "add_medicines": ["Alteplase", "Aspirin Emergency Use", "Atorvastatin"],
    },
    "Epilepsy": {
        "add_symptoms": ["Seizure", "Loss of Consciousness", "Confusion"],
        "add_medicines": ["Levetiracetam", "Lamotrigine"],
    },
    "Parkinsons Disease": {
        "add_symptoms": ["Tremor", "Back Stiffness", "Weakness"],
        "add_medicines": ["Carbidopa/Levodopa"],
    },
    "Alzheimers Disease": {
        "add_symptoms": ["Memory Loss", "Confusion", "Poor Concentration"],
        "add_medicines": ["Donepezil"],
    },
    "Rheumatoid Arthritis": {
        "add_symptoms": ["Joint Swelling", "Morning Stiffness", "Limited Range of Motion"],
        "add_medicines": ["Methotrexate", "Hydroxychloroquine", "Adalimumab"],
    },
    "Lupus": {
        "add_symptoms": ["Photosensitivity", "Malar Rash", "Joint Pain", "Fatigue"],
        "add_medicines": ["Hydroxychloroquine", "Prednisone", "Methotrexate"],
    },
    "Osteoporosis": {
        "remove_medicines": ["Ibuprofen"],
        "add_medicines": ["Calcium/Vitamin D", "Alendronate"],
    },
    "Gout": {
        "add_symptoms": ["Joint Swelling", "Severe Pain"],
        "add_medicines": ["Colchicine", "Allopurinol", "Naproxen"],
    },
    "Diabetes Type 2": {
        "add_symptoms": ["High Blood Sugar"],
        "add_medicines": ["Empagliflozin", "Semaglutide"],
    },
    "Hyperthyroidism": {
        "add_symptoms": ["Heat Intolerance", "Tremor", "Weight Loss", "Palpitations"],
        "add_medicines": ["Methimazole", "Propranolol"],
    },
    "Hypothyroidism": {
        "add_symptoms": ["Cold Intolerance", "Weight Gain", "Hair Loss", "Dry Skin"],
        "add_medicines": ["Levothyroxine"],
    },
    "Addisons Disease": {
        "add_symptoms": ["Dizziness", "Weight Loss", "Fatigue", "Dark Urine"],
        "add_medicines": ["Hydrocortisone", "Normal Saline IV"],
    },
    "Sepsis": {
        "add_symptoms": ["Fever", "Confusion", "Rapid Heartbeat", "Rapid Breathing", "Dehydration"],
        "add_medicines": ["Normal Saline IV", "Vancomycin", "Piperacillin/Tazobactam", "Meropenem"],
    },
}


def get_or_create(cur, table, name, extra_values=None):
    cur.execute(f"SELECT id FROM {table} WHERE lower(name)=lower(?)", (name,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(f"SELECT COALESCE(MAX(id), 0) + 1 FROM {table}")
    next_id = cur.fetchone()[0]

    if table == "medicine":
        warning, requires_prescription = extra_values
        cur.execute(
            "INSERT INTO medicine (id, name, warning, requires_prescription) VALUES (?, ?, ?, ?)",
            (next_id, name, warning, requires_prescription),
        )
    else:
        cur.execute(f"INSERT INTO {table} (id, name) VALUES (?, ?)", (next_id, name))

    return next_id


def link_once(cur, table, left_col, left_id, right_col, right_id):
    cur.execute(
        f"SELECT 1 FROM {table} WHERE {left_col}=? AND {right_col}=?",
        (left_id, right_id),
    )
    if not cur.fetchone():
        cur.execute(
            f"INSERT INTO {table} ({left_col}, {right_col}) VALUES (?, ?)",
            (left_id, right_id),
        )


def unlink(cur, table, left_col, left_id, right_col, right_id):
    cur.execute(
        f"DELETE FROM {table} WHERE {left_col}=? AND {right_col}=?",
        (left_id, right_id),
    )


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for symptom in SYMPTOMS:
        get_or_create(cur, "symptom", symptom)

    for name, warning, requires_prescription in MEDICINES:
        get_or_create(cur, "medicine", name, (warning, requires_prescription))

    for disease_name, payload in DISEASES.items():
        disease_id = get_or_create(cur, "disease", disease_name)
        for symptom_name in payload["symptoms"]:
            symptom_id = get_or_create(cur, "symptom", symptom_name)
            link_once(cur, "disease_symptom", "disease_id", disease_id, "symptom_id", symptom_id)
        for medicine_name in payload["medicines"]:
            medicine_id = get_or_create(cur, "medicine", medicine_name, ("Use only as directed.", 1))
            link_once(cur, "disease_medicine", "disease_id", disease_id, "medicine_id", medicine_id)

    for disease_name, payload in EXTRA_EXISTING_MAPPINGS.items():
        cur.execute("SELECT id FROM disease WHERE lower(name)=lower(?)", (disease_name,))
        row = cur.fetchone()
        if not row:
            continue
        disease_id = row[0]

        for symptom_name in payload.get("add_symptoms", []):
            symptom_id = get_or_create(cur, "symptom", symptom_name)
            link_once(cur, "disease_symptom", "disease_id", disease_id, "symptom_id", symptom_id)

        for medicine_name in payload.get("remove_medicines", []):
            cur.execute("SELECT id FROM medicine WHERE lower(name)=lower(?)", (medicine_name,))
            med_row = cur.fetchone()
            if med_row:
                unlink(cur, "disease_medicine", "disease_id", disease_id, "medicine_id", med_row[0])

        for medicine_name in payload.get("add_medicines", []):
            medicine_id = get_or_create(cur, "medicine", medicine_name, ("Use only as directed.", 1))
            link_once(cur, "disease_medicine", "disease_id", disease_id, "medicine_id", medicine_id)

    conn.commit()

    for table in ["disease", "symptom", "medicine", "disease_symptom", "disease_medicine"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cur.fetchone()[0]}")

    conn.close()


if __name__ == "__main__":
    main()
