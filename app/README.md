# 🩺 Diabetes Prediction Web App (FastAPI + Streamlit)

This is a full-stack machine learning web application that predicts whether a patient is diabetic based on health parameters provided via CSV upload.

It is built using:
- ✅ FastAPI (Backend REST API)
- ✅ Streamlit (Frontend UI)
- ✅ SQLite + SQLAlchemy (Database)
- ✅ Scikit-learn (ML Model)

---

## 🔧 Features

- 🔐 User registration and login (JWT Authentication)
- 📤 Upload CSV files to get predictions
- 📊 View prediction results in tabular form
- 🕘 Access prediction history
- 🧹 Option to clear prediction history
- 📥 Download prediction results as CSV
- 🧠 ML model trained using logistic regression

---

## 📁 Folder Structure

```
project/
│
├── app/
│   ├── routes/              # API routes (user_routes, ml_routes)
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # DB connection setup
│   └── JWTUtilities.py      # Password hashing & JWT logic
│
├── diabetes_model.pkl       # Trained ML model
├── train_model.py           # Script to train & save the model
├── sample_diabetes_dataset.csv  # Sample training/testing data
├── app_ui.py                # Streamlit UI
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🚀 How to Run the Project

### ✅ 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### ✅ 2. Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Access docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### ✅ 3. Run Streamlit UI

```bash
streamlit run app_ui.py
```

App opens at: [http://localhost:8501](http://localhost:8501)

---

## 🧠 Machine Learning Model

The model is trained using Logistic Regression on a synthetic diabetes dataset. You can retrain the model using:

```bash
python train_model.py
```

---

## 📤 Deployment

- ✅ Upload your code to GitHub
- ✅ Deploy the frontend on [Streamlit Cloud](https://streamlit.io/cloud)
- (Optional) Containerize backend with Docker for deployment to Render/Railway

---

## 🏁 What's Next?

- Add prediction charts and analytics
- Deploy backend with Docker
- Add user roles (admin/user)
- Improve model with real-world dataset

---

## 🧑‍🎓 Ideal For:

- MS in AI/ML application portfolios
- Resume projects
- Learning backend + ML integration
