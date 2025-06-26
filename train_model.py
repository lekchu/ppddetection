import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

# ✅ 1. Create a sample/fake dataset
data = {
    'Age': [23, 30, 35, 28, 40],
    'FamilySupport': ['High', 'Medium', 'Low', 'Medium', 'High'],
    'Q1': [0, 1, 2, 1, 0],
    'Q2': [1, 0, 2, 1, 0],
    'Q3': [3, 2, 1, 1, 0],
    'Q4': [0, 1, 2, 2, 1],
    'Q5': [1, 2, 3, 1, 0],
    'Q6': [0, 1, 3, 2, 0],
    'Q7': [1, 2, 3, 2, 1],
    'Q8': [1, 2, 3, 2, 0],
    'Q9': [0, 1, 2, 3, 1],
    'Q10': [0, 1, 2, 2, 1],
    'Risk': ['Mild', 'Moderate', 'Severe', 'Moderate', 'Mild']
}

df = pd.DataFrame(data)

# ✅ 2. Encode FamilySupport
df['FamilySupport'] = df['FamilySupport'].map({'Low': 0, 'Medium': 1, 'High': 2})

# ✅ 3. Encode Risk labels
label_encoder = LabelEncoder()
df["RiskEncoded"] = label_encoder.fit_transform(df["Risk"])

# ✅ 4. Features and label
features = ['Age', 'FamilySupport', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
X = df[features]
y = df["RiskEncoded"]

# ✅ 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# ✅ 6. Build model
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(random_state=42))
])

pipeline.fit(X_train, y_train)

# ✅ 7. Save model and encoder
joblib.dump(pipeline, "ppd_model_pipeline.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("✅ Done! Sample model and label encoder saved.")
