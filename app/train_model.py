"""import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# ✅ Sample dummy training data
df = pd.DataFrame({
    "Pregnancies": [1, 2, 3, 4],
    "Glucose": [100, 150, 120, 170],
    "BloodPressure": [70, 80, 60, 90],
    "Outcome": [0, 1, 0, 1]
})

# ✅ Features and target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# ✅ Train a basic model
model = LogisticRegression()
model.fit(X, y)

# ✅ Save the model to a .pkl file
with open("diabetes_model.pkl", "wb") as f:
    pickle.dump(model, f) """

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

# Load dataset
df = pd.read_csv("sample_diabetes_dataset.csv")

# Features (X) and Label (y)
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the model to a .pkl file
with open("diabetes_model.pkl", "wb") as f:
    pickle.dump(model, f)