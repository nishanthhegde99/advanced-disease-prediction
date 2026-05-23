#!/usr/bin/env python3
"""
================================================================================
🤖 ENHANCED MODEL TRAINING SCRIPT
================================================================================
Trains 5 ML models with detailed metrics for medical reliability:
- Naive Bayes
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)
- Logistic Regression

Extracts: Accuracy, Precision, Recall, F1-Score
================================================================================
"""

import sqlite3
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import json
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================
DATABASE = "disease.db"
MODEL_FILE = "disease_model.pkl"
METRICS_FILE = "model_metrics.json"

# ============================================================================
# DATA LOADING
# ============================================================================
def load_training_data():
    """Load disease-symptom data from database"""
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    # Get all symptoms
    cur.execute("SELECT id FROM symptom ORDER BY id")
    symptom_ids = [row[0] for row in cur.fetchall()]
    
    # Get all diseases
    cur.execute("SELECT id, name FROM disease ORDER BY id")
    diseases = cur.fetchall()
    
    # Create training data
    X = []
    y = []
    disease_names = {}
    
    for disease_id, disease_name in diseases:
        disease_names[disease_id] = disease_name
        
        # Get symptoms for this disease
        cur.execute("SELECT symptom_id FROM disease_symptom WHERE disease_id=?", (disease_id,))
        disease_symptoms = [row[0] for row in cur.fetchall()]
        
        # Create binary feature vector
        features = [1 if sid in disease_symptoms else 0 for sid in symptom_ids]
        for _ in range(10):  # Duplicate 10 times to allow train_test_split
            X.append(features)
            y.append(disease_id)
    
    conn.close()
    
    return np.array(X), np.array(y), symptom_ids, disease_names

# ============================================================================
# MODEL TRAINING & EVALUATION
# ============================================================================
def train_models(X, y):
    """Train all 5 models and compute metrics"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    models_info = {}
    
    print("\n" + "="*70)
    print("🤖 TRAINING 5 MACHINE LEARNING MODELS")
    print("="*70 + "\n")
    
    # ====== 1. NAIVE BAYES ======
    print("1️⃣  Training Naive Bayes Classifier...")
    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    
    nb_pred = nb_model.predict(X_test)
    nb_accuracy = accuracy_score(y_test, nb_pred) * 100
    nb_precision = precision_score(y_test, nb_pred, average='weighted', zero_division=0) * 100
    nb_recall = recall_score(y_test, nb_pred, average='weighted', zero_division=0) * 100
    nb_f1 = f1_score(y_test, nb_pred, average='weighted', zero_division=0) * 100
    
    nb_cv_scores = cross_val_score(nb_model, X, y, cv=5, scoring='accuracy')
    
    models_info['naive_bayes'] = {
        'model': nb_model,
        'accuracy': nb_accuracy,
        'precision': nb_precision,
        'recall': nb_recall,
        'f1_score': nb_f1,
        'cv_mean': nb_cv_scores.mean() * 100,
        'cv_std': nb_cv_scores.std() * 100
    }
    
    print(f"   ✓ Accuracy: {nb_accuracy:.2f}%")
    print(f"   ✓ Precision: {nb_precision:.2f}%")
    print(f"   ✓ Recall: {nb_recall:.2f}%")
    print(f"   ✓ F1-Score: {nb_f1:.2f}%")
    print(f"   ✓ Cross-Validation: {nb_cv_scores.mean()*100:.2f}% ± {nb_cv_scores.std()*100:.2f}%\n")
    
    # ====== 2. RANDOM FOREST ======
    print("2️⃣  Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        random_state=42,
        n_jobs=-1,
        min_samples_split=5,
        min_samples_leaf=2
    )
    rf_model.fit(X_train, y_train)
    
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred) * 100
    rf_precision = precision_score(y_test, rf_pred, average='weighted', zero_division=0) * 100
    rf_recall = recall_score(y_test, rf_pred, average='weighted', zero_division=0) * 100
    rf_f1 = f1_score(y_test, rf_pred, average='weighted', zero_division=0) * 100
    
    rf_cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='accuracy')
    
    models_info['random_forest'] = {
        'model': rf_model,
        'accuracy': rf_accuracy,
        'precision': rf_precision,
        'recall': rf_recall,
        'f1_score': rf_f1,
        'cv_mean': rf_cv_scores.mean() * 100,
        'cv_std': rf_cv_scores.std() * 100
    }
    
    print(f"   ✓ Accuracy: {rf_accuracy:.2f}%")
    print(f"   ✓ Precision: {rf_precision:.2f}%")
    print(f"   ✓ Recall: {rf_recall:.2f}%")
    print(f"   ✓ F1-Score: {rf_f1:.2f}%")
    print(f"   ✓ Cross-Validation: {rf_cv_scores.mean()*100:.2f}% ± {rf_cv_scores.std()*100:.2f}%\n")
    
    # ====== 3. GRADIENT BOOSTING ======
    print("3️⃣  Training Gradient Boosting Classifier...")
    gb_model = GradientBoostingClassifier(
        n_estimators=150,
        learning_rate=0.1,
        max_depth=7,
        random_state=42,
        subsample=0.8
    )
    gb_model.fit(X_train, y_train)
    
    gb_pred = gb_model.predict(X_test)
    gb_accuracy = accuracy_score(y_test, gb_pred) * 100
    gb_precision = precision_score(y_test, gb_pred, average='weighted', zero_division=0) * 100
    gb_recall = recall_score(y_test, gb_pred, average='weighted', zero_division=0) * 100
    gb_f1 = f1_score(y_test, gb_pred, average='weighted', zero_division=0) * 100
    
    gb_cv_scores = cross_val_score(gb_model, X, y, cv=5, scoring='accuracy')
    
    models_info['gradient_boosting'] = {
        'model': gb_model,
        'accuracy': gb_accuracy,
        'precision': gb_precision,
        'recall': gb_recall,
        'f1_score': gb_f1,
        'cv_mean': gb_cv_scores.mean() * 100,
        'cv_std': gb_cv_scores.std() * 100
    }
    
    print(f"   ✓ Accuracy: {gb_accuracy:.2f}%")
    print(f"   ✓ Precision: {gb_precision:.2f}%")
    print(f"   ✓ Recall: {gb_recall:.2f}%")
    print(f"   ✓ F1-Score: {gb_f1:.2f}%")
    print(f"   ✓ Cross-Validation: {gb_cv_scores.mean()*100:.2f}% ± {gb_cv_scores.std()*100:.2f}%\n")
    
    # ====== 4. SUPPORT VECTOR MACHINE ======
    print("4️⃣  Training Support Vector Machine (SVM)...")
    svm_model = SVC(
        kernel='rbf',
        C=1.0,
        gamma='scale',
        probability=True,
        random_state=42
    )
    svm_model.fit(X_train, y_train)
    
    svm_pred = svm_model.predict(X_test)
    svm_accuracy = accuracy_score(y_test, svm_pred) * 100
    svm_precision = precision_score(y_test, svm_pred, average='weighted', zero_division=0) * 100
    svm_recall = recall_score(y_test, svm_pred, average='weighted', zero_division=0) * 100
    svm_f1 = f1_score(y_test, svm_pred, average='weighted', zero_division=0) * 100
    
    svm_cv_scores = cross_val_score(svm_model, X, y, cv=5, scoring='accuracy')
    
    models_info['svm'] = {
        'model': svm_model,
        'accuracy': svm_accuracy,
        'precision': svm_precision,
        'recall': svm_recall,
        'f1_score': svm_f1,
        'cv_mean': svm_cv_scores.mean() * 100,
        'cv_std': svm_cv_scores.std() * 100
    }
    
    print(f"   ✓ Accuracy: {svm_accuracy:.2f}%")
    print(f"   ✓ Precision: {svm_precision:.2f}%")
    print(f"   ✓ Recall: {svm_recall:.2f}%")
    print(f"   ✓ F1-Score: {svm_f1:.2f}%")
    print(f"   ✓ Cross-Validation: {svm_cv_scores.mean()*100:.2f}% ± {svm_cv_scores.std()*100:.2f}%\n")
    
    # ====== 5. LOGISTIC REGRESSION ======
    print("5️⃣  Training Logistic Regression...")
    lr_model = LogisticRegression(
        max_iter=1000,
        random_state=42,
        solver='lbfgs',
        multi_class='multinomial'
    )
    lr_model.fit(X_train, y_train)
    
    lr_pred = lr_model.predict(X_test)
    lr_accuracy = accuracy_score(y_test, lr_pred) * 100
    lr_precision = precision_score(y_test, lr_pred, average='weighted', zero_division=0) * 100
    lr_recall = recall_score(y_test, lr_pred, average='weighted', zero_division=0) * 100
    lr_f1 = f1_score(y_test, lr_pred, average='weighted', zero_division=0) * 100
    
    lr_cv_scores = cross_val_score(lr_model, X, y, cv=5, scoring='accuracy')
    
    models_info['logistic_regression'] = {
        'model': lr_model,
        'accuracy': lr_accuracy,
        'precision': lr_precision,
        'recall': lr_recall,
        'f1_score': lr_f1,
        'cv_mean': lr_cv_scores.mean() * 100,
        'cv_std': lr_cv_scores.std() * 100
    }
    
    print(f"   ✓ Accuracy: {lr_accuracy:.2f}%")
    print(f"   ✓ Precision: {lr_precision:.2f}%")
    print(f"   ✓ Recall: {lr_recall:.2f}%")
    print(f"   ✓ F1-Score: {lr_f1:.2f}%")
    print(f"   ✓ Cross-Validation: {lr_cv_scores.mean()*100:.2f}% ± {lr_cv_scores.std()*100:.2f}%\n")
    
    return models_info

# ============================================================================
# BEST MODEL SELECTION
# ============================================================================
def get_best_model(models_info):
    """Determine best model based on F1-score"""
    best_model_key = max(models_info, key=lambda k: models_info[k]['f1_score'])
    return best_model_key, models_info[best_model_key]['f1_score']

# ============================================================================
# SAVE MODELS
# ============================================================================
def save_models(models_info, symptom_ids, best_model_key):
    """Save all trained models and metadata"""
    
    # Prepare data for pickling
    data_to_save = {
        'naive_bayes': {
            'model': models_info['naive_bayes']['model'],
            'accuracy': models_info['naive_bayes']['accuracy'],
            'precision': models_info['naive_bayes']['precision'],
            'recall': models_info['naive_bayes']['recall'],
            'f1_score': models_info['naive_bayes']['f1_score'],
        },
        'random_forest': {
            'model': models_info['random_forest']['model'],
            'accuracy': models_info['random_forest']['accuracy'],
            'precision': models_info['random_forest']['precision'],
            'recall': models_info['random_forest']['recall'],
            'f1_score': models_info['random_forest']['f1_score'],
        },
        'gradient_boosting': {
            'model': models_info['gradient_boosting']['model'],
            'accuracy': models_info['gradient_boosting']['accuracy'],
            'precision': models_info['gradient_boosting']['precision'],
            'recall': models_info['gradient_boosting']['recall'],
            'f1_score': models_info['gradient_boosting']['f1_score'],
        },
        'svm': {
            'model': models_info['svm']['model'],
            'accuracy': models_info['svm']['accuracy'],
            'precision': models_info['svm']['precision'],
            'recall': models_info['svm']['recall'],
            'f1_score': models_info['svm']['f1_score'],
        },
        'logistic_regression': {
            'model': models_info['logistic_regression']['model'],
            'accuracy': models_info['logistic_regression']['accuracy'],
            'precision': models_info['logistic_regression']['precision'],
            'recall': models_info['logistic_regression']['recall'],
            'f1_score': models_info['logistic_regression']['f1_score'],
        },
        'symptom_ids': symptom_ids,
        'best_model': best_model_key.replace('_', ' ').title(),
        'trained_at': datetime.now().isoformat()
    }
    
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(data_to_save, f)
    
    print(f"✅ Models saved to {MODEL_FILE}")

# ============================================================================
# GENERATE REPORT
# ============================================================================
def generate_metrics_report(models_info, best_model_key):
    """Generate detailed metrics report"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'models': {},
        'comparison': {
            'best_model': best_model_key.replace('_', ' ').title(),
            'best_f1_score': models_info[best_model_key]['f1_score']
        }
    }
    
    print("\n" + "="*70)
    print("📊 MODEL PERFORMANCE COMPARISON")
    print("="*70 + "\n")
    
    print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
    print("-"*70)
    
    for model_key, model_data in models_info.items():
        model_name = model_key.replace('_', ' ').title()
        accuracy = model_data['accuracy']
        precision = model_data['precision']
        recall = model_data['recall']
        f1 = model_data['f1_score']
        
        print(f"{model_name:<25} {accuracy:<11.2f}% {precision:<11.2f}% {recall:<11.2f}% {f1:<11.2f}%")
        
        report['models'][model_key] = {
            'name': model_name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': model_data['cv_mean'],
            'cv_std': model_data['cv_std']
        }
    
    print("-"*70)
    print(f"\n🏆 Best Model: {report['comparison']['best_model']} (F1-Score: {report['comparison']['best_f1_score']:.2f}%)")
    
    # Save report
    with open(METRICS_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Metrics report saved to {METRICS_FILE}\n")
    
    return report

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("\n🚀 ENHANCED MODEL TRAINING SYSTEM\n")
    
    try:
        # Load data
        print("📁 Loading training data from database...")
        X, y, symptom_ids, disease_names = load_training_data()
        print(f"✅ Loaded {len(X)} training samples with {len(symptom_ids)} symptoms")
        print(f"✅ Total diseases: {len(disease_names)}\n")
        
        # Train models
        models_info = train_models(X, y)
        
        # Determine best model
        best_model_key, best_f1 = get_best_model(models_info)
        
        # Save models
        save_models(models_info, symptom_ids, best_model_key)
        
        # Generate report
        report = generate_metrics_report(models_info, best_model_key)
        
        print("✅ Training Complete!\n")
        
    except Exception as e:
        print(f"❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
