# Advanced Disease Prediction

Flask-based AI disease prediction app with:

- 5-model ML ensemble prediction
- temporal symptom analysis
- disease-specific medicine recommendations
- OTC and Rx Required medicine labels
- PDF report generation
- medical safety disclaimer

Current dataset size:

- 140 diseases
- 137 symptoms
- 183 medicines
- 700 disease-symptom links
- 402 disease-medicine links

## Project Files

```text
advanced_system.py        Main Flask application
hybrid_engine.py          Final prediction and urgency logic
temporal_analyzer.py      Temporal symptom progression analysis
database.py               Database table setup
expand_medical_dataset.py Adds expanded diseases, symptoms, medicines, and Rx flags
train_advanced_models.py  Model training script
test_system.py            Temporal analysis smoke tests
disease.db                SQLite disease/medicine database
disease_model.pkl         Trained ML model bundle
model_metrics.json        Model metrics
requirements.txt          Python dependencies
templates/temporal_system.html
```

## Setup

```bash
pip3 install -r requirements.txt
```

## Run

```bash
python3 advanced_system.py
```

Default URL:

```text
http://127.0.0.1:5050
```

If port `5050` is busy, run:

```bash
python3 -c "from advanced_system import app; app.run(debug=False, host='127.0.0.1', port=5051, use_reloader=False)"
```

## Test

```bash
python3 test_system.py
```

## Expand and Retrain Dataset

```bash
python3 expand_medical_dataset.py
python3 train_advanced_models.py
```

## Important

This app is for educational/informational use only. It is not a replacement for professional medical diagnosis or treatment. Rx medicines require doctor approval.
