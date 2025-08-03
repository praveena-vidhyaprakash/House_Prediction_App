
from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)
model_path = "model/house_price_lasso_model.pkl"

if os.path.exists(model_path):
    model, scaler, columns = joblib.load(model_path)
else:
    model = scaler = columns = None

@app.route("/", methods=["GET", "POST"])
def index():
    print("Serving the homepage...")  # Debug line
    result = None
    if request.method == "POST" and model:
        try:
            size = float(request.form["size"])
            bedrooms = int(request.form["bedrooms"])
            location = request.form["location"]
            input_data = {
                "size": size,
                "bedrooms": bedrooms,
                f"location_{location}": 1
            }

            # Fill missing columns with 0
            row = {col: 0 for col in columns}
            row.update(input_data)
            df = pd.DataFrame([row])
            df_scaled = scaler.transform(df)
            prediction = model.predict(df_scaled)[0]
            result = f"Predicted House Price: ₹{prediction:,.2f}"
        except Exception as e:
            result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)