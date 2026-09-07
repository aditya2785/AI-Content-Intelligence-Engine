🎬 AI Content Intelligence Engine
Personalized Discovery • Engagement Prediction • Creator Intelligence

An end-to-end Data Science platform that transforms user–content interactions into actionable product insights, engagement predictions, and personalized recommendations.

The project brings together data engineering, SQL analytics, machine learning, recommendation systems, experimentation, and product analytics into one complete workflow.

🚀 What I Built

A content intelligence engine capable of answering:

What is happening? → What drives engagement? → What should we recommend? → Does personalization work better?

🔹 Product Analytics
PostgreSQL-based platform analytics
User, content, creator and engagement analysis
DAU/WAU, CTR, watch time, completion and engagement metrics
Genre, duration, freshness and creator-performance analysis
🔹 Engagement Prediction

Built a point-in-time-safe ML pipeline to predict meaningful user engagement.

Compared:

Logistic Regression
Random Forest
XGBoost

Final model: Random Forest

Validation ROC-AUC: 0.5840
Validation PR-AUC: 0.4419

🔹 Personalized Recommendation Engine

Built a multi-stage recommender:

Candidate Generation
        ↓
Seen-Content Filtering
        ↓
Point-in-Time Features
        ↓
ML Engagement Ranking
        ↓
Freshness + Exploration
        ↓
Diversity
        ↓
Explainable Recommendations

The recommender uses 53 validated features derived from:

User history
User–content behavior
User–genre preferences
Content performance
Creator performance
Freshness
Context and timing

It also handles cold-start users and new content.

📊 Recommendation Evaluation

Compared:

Global Popularity
Recent Popularity
Content-Based
Personalized ML
Strategy	Precision@10	Recall@10	MAP@10	NDCG@10
Global Popularity	0.0002	0.0007	0.0002	0.0005
Recent Popularity	0.0014	0.0047	0.0018	0.0032
Content-Based	0.0005	0.0016	0.0005	0.0010
Personalized ML	0.0014	0.0055	0.0019	0.0035

The Personalized ML approach improved Recall@10 by ~17% over Recent Popularity in the offline evaluation.

The system was also evaluated for catalog coverage, diversity and novelty, rather than optimizing relevance alone.

💡 Key Product Insights

The analysis showed that:

Freshness is strongly associated with engagement, making it a useful ranking signal.
Medium-length content performed better than extremely short or very long content in the synthetic environment.
Larger creators showed higher engagement, highlighting the risk of popularity reinforcement.
Content-based similarity and ML ranking captured different signals, resulting in substantial re-ranking.
Recommendation quality requires balancing relevance, discovery and diversity.
🖥️ Interactive Dashboard

The final system is exposed through a Streamlit dashboard with:

Overview — platform KPIs and trends
Content Intelligence — content performance analysis
Creator Intelligence — creator-level analytics
Recommendations — live personalized feed generation
Experiments — recommendation strategy evaluation
Model — model performance and feature intelligence

Each recommendation includes a human-readable explanation such as:

Strong history with Animation content • recent content • matches patterns in previously interacted content

🏗️ Architecture
Synthetic Data
      ↓
Data Quality
      ↓
PostgreSQL Analytics
      ↓
EDA & Product Insights
      ↓
Feature Engineering
      ↓
Engagement Model
      ↓
Recommendation Engine
      ↓
Evaluation & Experimentation
      ↓
Streamlit Dashboard
📦 Dataset

The project uses a synthetically generated content-platform dataset:

5,000 users
500 creators
10,000 content items
250,000 interactions

The data is designed to reproduce realistic challenges such as sparse interactions, skewed popularity, temporal behavior, repeated interactions and cold-start scenarios.

Disclaimer: This is an independent synthetic project. It does not use AICines proprietary data, internal algorithms, private systems, or confidential information.

🛠️ Tech Stack

Python · Pandas · NumPy · PostgreSQL · SQL · scikit-learn · XGBoost · TF-IDF · Plotly · Streamlit · Joblib

📁 Project Structure
aicines-content-intelligence/
├── api/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_interaction_generation.ipynb
│   ├── 03_data_quality.ipynb
│   ├── 04_eda_and_insights.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_engagement_model.ipynb
│   └── 07_recommendation_engine.ipynb
├── sql/
├── src/
│   ├── analytics/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── recommender/
├── tests/
├── requirements.txt
└── README.md
▶️ Run Locally
pip install -r requirements.txt
python -m streamlit run dashboard/app.py

Then open:

http://localhost:8501
⚠️ Important Limitation

You can visit:
https://ai-content-intelligence-engine.streamlit.app/

The recommendation and engagement results are based on synthetic data and offline evaluation.

The observed metric improvements should therefore not be interpreted as causal online product impact.

A production implementation would require real user data, online experimentation, real-time features, stronger retrieval/ranking models, monitoring and continuous model evaluation.

🎯 Project Outcome

This project demonstrates an end-to-end approach to a real product Data Science problem:

Data → Insights → Prediction → Recommendation → Experimentation → Product

Rather than treating ML as the final output, the system connects modeling decisions to user experience, platform health, creator discovery, and measurable product outcomes.

👤 Author

Aditya Jha
