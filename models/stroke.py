import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression

# load data
data = pd.read_csv("../data/stroke.csv")
data = data.drop("id", axis=1)

# check for null values
null_columns = data.columns[data.isnull().any()]
print(null_columns)
print()

# impute null column with mean
data['bmi'] = data['bmi'].fillna(data['bmi'].mean())
print(data.info())
print()

# split into X and y
y = data['stroke']
X = data.drop("stroke", axis=1)

# split into numerical and categorical
cols = X.columns
numerical = data[cols].select_dtypes(include=np.number)
categorical = data[cols].select_dtypes(include='object')

# Convert categorical to numerical columns
encoders = {}
categories = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']

for col in categories:
    le = LabelEncoder()
    le.fit(X[col])
    X[col] = le.transform(X[col])    
    encoders[col] = le

# train test split on the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# distribution of target variable
print("No rebalance:", sorted(Counter(y_train).items()))

# random under-sampling
rus = RandomUnderSampler(random_state=42)
X_train_under, y_train_under = rus.fit_resample(X_train, y_train)
print("Undersampled:", sorted(Counter(y_train_under).items()))

# random over-sampling
ros = RandomOverSampler(random_state=42)
X_train_over, y_train_over = ros.fit_resample(X_train, y_train)
print("Oversampled:", sorted(Counter(y_train_over).items()))
print()

# Logistic Regression (over-sample)
lr = LogisticRegression(random_state=42, solver = "liblinear")
lr.fit(X_train_over, y_train_over)
y_pred = lr.predict(X_test)
y_pred_prob = lr.predict_proba(X_test)[:, 1]

# metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_prob)

# print results
print("Accuracy:", '{0:.3%}'.format(accuracy))
print("Precision:", '{0:.3%}'.format(precision))
print("Recall:", '{0:.3%}'.format(recall))
print("F1-Score:", '{0:.3%}'.format(f1))
print("AUC:", '{0:.3%}'.format(auc))
print()

# save trained model for export
import joblib
joblib.dump(lr, 'StrokeModel.pkl')
joblib.dump(encoders, 'StrokeEncoders.pkl')