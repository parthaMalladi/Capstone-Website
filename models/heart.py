import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression

# load data
data = pd.read_csv("../data/heart.csv")

# look at columns
print(data.info())
print()

# split into X and y
y = data['HeartDisease']
X = data.drop("HeartDisease", axis=1)

# split into numerical and categorical
cols = X.columns
numerical = data[cols].select_dtypes(include=np.number)
categorical = data[cols].select_dtypes(include='object')

# print the seperated columns
print(numerical.columns)
print(categorical.columns)
print()

# define the categories
categories = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]

# Convert categorical to numerical columns
encoders = {} 

for col in categories:
    le = LabelEncoder()
    le.fit(X[col])
    X[col] = le.transform(X[col])    
    encoders[col] = le

# train test split on the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Logistic Regression
lr = LogisticRegression(random_state=42, max_iter=10000)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)

# metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
y_pred_prob = lr.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred_prob)

# print results
print("Accuracy:", '{0:.3%}'.format(accuracy))
print("Precision:", '{0:.3%}'.format(precision))
print("Recall:", '{0:.3%}'.format(recall))
print("F1-Score:", '{0:.3%}'.format(f1))
print("AUC:", '{0:.3%}'.format(auc))

# save trained model for export
import joblib
joblib.dump(lr, 'HeartModel.pkl')
joblib.dump(encoders, 'HeartEncoders.pkl')