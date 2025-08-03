
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
import joblib
import os

df = pd.read_csv("data/processed/house_data.csv")

df = pd.get_dummies(df, columns=["location"], drop_first=True)

X = df.drop("price", axis=1)
y = df["price"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

model = Lasso(alpha=0.1)
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
joblib.dump((model, scaler, X.columns.tolist()), "model/house_price_lasso_model.pkl")

print("✅ Lasso Regression model trained and saved.")





















