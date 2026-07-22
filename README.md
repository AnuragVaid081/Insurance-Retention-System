# Insurance Retention Intelligence System

An AI-powered insurance renewal analytics platform built using **Python**, **Streamlit**, **TensorFlow**, and **Ollama (Qwen2.5)** to help renewal managers identify at-risk policies, analyze intermediary performance, and improve customer retention.

This project was developed during my Research Internship at **Go Digit General Insurance** to explore how Machine Learning and Generative AI can assist renewal teams in making data-driven decisions.

---

## Features

### Renewal Prediction
- LSTM-based renewal probability prediction
- Batch prediction from uploaded policy data
- Customer risk segmentation
- Renewal probability scoring

### Interactive Dashboard
- Branch-level renewal analytics
- IMD (Insurance Marketing Department) performance dashboard
- Renewal trends
- Premium analysis
- Claim analysis
- Customer retention metrics

### AI Policy Analysis
- Individual policy explanation using **Qwen2.5**
- Explains why a customer is likely or unlikely to renew
- Uses historical policy information and renewal remarks
- Suggests actionable renewal strategies

### AI Channel Analysis
- AI-powered comparison of IMD performance
- Identifies why some IMDs outperform others
- Detects common behavioural patterns
- Analyses historical renewal remarks
- Provides business recommendations for renewal managers

### Synthetic Dataset Generator
- Generates realistic Indian motor insurance datasets
- Customer master
- Policy history
- Vehicle master
- Channel master
- Claims history

---

# Tech Stack

### Machine Learning
- TensorFlow / Keras
- LSTM
- Scikit-learn
- Pandas
- NumPy

### Dashboard
- Streamlit
- Plotly

### AI
- Ollama
- Qwen2.5

### Development
- Python
- Git
- VS Code

---

# Dashboard Modules

## Renewal Prediction

Predicts the likelihood of policy renewal using a trained LSTM model.

Includes:

- Renewal probability
- Risk categorization
- Customer prioritization
- AI explanation for each prediction

---

## Channel Analysis

Provides insights into intermediary (IMD) performance.

Metrics include:

- Portfolio size
- Renewal rate
- Average premium
- Claim count
- Average NCB
- Policy tenure

The AI Channel Analysis feature compares IMDs, identifies recurring remark patterns, explains high and low renewal performance, and recommends actions for renewal managers.

---

# AI Features

## Policy AI Analysis

Uses Qwen2.5 running locally through Ollama to explain individual renewal predictions.

The AI analyses:

- Policy history
- Previous renewal remarks
- Claims
- Customer behaviour
- Historical renewals

---

## Channel AI Analysis

Analyses all IMDs within a branch and provides:

- Executive summary
- Best-performing IMDs
- Struggling IMDs
- Behavioural patterns
- Remark analysis
- Operational recommendations

---

# Installation

Clone the repository

```bash
git clone https://github.com/AnuragVaid081/Insurance-Retention-System.git
```

Move into the project

```bash
cd Insurance-Retention-System
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Running Ollama

Install Ollama.

Pull the Qwen model:

```bash
ollama pull qwen2.5:7b
```

Run Ollama

```bash
ollama serve
```

The application connects to

```
http://localhost:11434
```

---

# Future Improvements

- XGBoost comparison model
- Real-time renewal recommendations
- SHAP explainability
- Geospatial renewal heatmaps
- Automated renewal manager reports
- CRM integration
- MLOps deployment pipeline
- Continuous model retraining

---

# Disclaimer

This project was developed for educational and research purposes.

The datasets included in this repository are **synthetically generated** and do not contain any confidential customer information.

---

# Author

**Anurag Vaid**

Research Intern – Go Digit General Insurance

LinkedIn: https://www.linkedin.com/in/anurag-vaid-24a149325/

GitHub: https://github.com/AnuragVaid081