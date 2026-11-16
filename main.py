import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import sqlite3
import matplotlib.pyplot as plt

df = pd.read_csv("data/bank-additional-full.csv", sep=";")

pd.set_option("display.max_columns", None)

#Cleans the data
df_clean = df.drop_duplicates().copy() #Drops the duplicates
df_clean = df_clean.drop(columns=["duration", "campaign", "pdays"]) #Drops these rows
df_clean["y"] = (df_clean["y"] == "yes").astype(int) #Convert t/f to 1/0

print(df_clean.shape)

#Converts to 0 and 1
X = pd.get_dummies(df_clean.drop(columns=["y"]), drop_first=True)
y = df_clean["y"]

#Splits the data
X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2, train_size=0.8, stratify=y, random_state=42
)

#Logistic Regression
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))
model.fit(X_train, y_train)
preds = model.predict(X_test)
print(classification_report(y_test, preds))
print(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))


#Random Forest
model = make_pipeline(RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42, max_depth=10))
model.fit(X_train, y_train)
preds = model.predict(X_test)
print(classification_report(y_test, preds))
print("ROC AUC:", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))
print("Train vs Test Accuracy: ", model.score(X_train, y_train), model.score(X_test, y_test))

rf_model = model.named_steps["randomforestclassifier"]

#Check the importance of everything
importances = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": rf_model.feature_importances_
}).sort_values(by="Importance", ascending=False)
    
print("10 Most Important Features:")
print(importances.head(10).to_string(index=False))

#Set up the db
conn = sqlite3.connect("bank.db")
df_clean.to_sql("customers", conn, index=False, if_exists="replace")

#Get the yes rate
job_query = """
SELECT job, COUNT(*) AS n, ROUND(AVG(y) * 100, 1) AS yes_rate_pct
FROM customers
GROUP BY job
ORDER BY yes_rate_pct DESC
"""

month_query = """
SELECT month, COUNT(*) AS n, ROUND(AVG(y) * 100, 1) AS yes_rate_pct
FROM customers
GROUP BY month
ORDER BY yes_rate_pct DESC
"""

poutcome_query = """
SELECT poutcome, COUNT(*) AS n, ROUND(AVG(y) * 100, 1) AS yes_rate_pct
FROM customers
GROUP BY poutcome
ORDER BY yes_rate_pct DESC
"""

age_group_query = """
SELECT
  CASE
    WHEN age < 25 THEN 'under 25'
    WHEN age < 35 THEN '25-34'
    WHEN age < 50 THEN '35-49'
    WHEN age < 65 THEN '50-64'
    ELSE '65+'
  END AS age_group,
  COUNT(*) AS n,
  ROUND(AVG(y) * 100, 1) AS yes_rate_pct
FROM customers
GROUP BY age_group
ORDER BY yes_rate_pct DESC
"""

#print(pd.read_sql(age_group_query, conn))

#Make the charts

#Rate by month
month_df = pd.read_sql(month_query, conn)
plt.figure(figsize=(8,4))
plt.bar(month_df["month"], month_df["yes_rate_pct"])
plt.axhline(11.3, linestyle="--", color="gray")
plt.title("Subscription rate by month")
plt.ylabel("Yes-rate (%)")
plt.tight_layout()
plt.savefig("charts/yes_rate_by_month.png")
plt.close()

#Model Comparison
results = pd.DataFrame({
    "model": ["Baseline", "Logistic (balanced)", "Forest (depth 10)"],
    "recall": [0, 0.65, 0.64],
    "precision": [0, 0.36, 0.41],
    "auc": [0, 0.8007, 0.8118],
})

graph = results.set_index("model").plot(kind="bar")
graph.set_title("Model comparison (class 1 = subscribed)")
graph.set_ylabel("Score")
graph.set_ylim(0, 1)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/model_comparison.png")
plt.close()

#Top 10 features
top = importances.head(10)
plt.barh(top["Feature"], top["Importance"])
plt.gca().invert_yaxis()
plt.title("Top 10 Features")
plt.tight_layout()
plt.savefig("charts/top_features.png")

conn.close()