import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Step 1: Load Excel file
data = pd.read_excel("house_data.xlsx")

# Step 2: Select features and target
X = data.iloc[:, 0:5]  # First 5 columns: Avg. Area Income to Area Population
y = data['Price']      # Target column

# Step 3: Train the model
model = LinearRegression()
model.fit(X, y)

# Step 4: Save the model
joblib.dump(model, "HousePrediction.joblib")
print("✅ Model trained and saved as HousePrediction.joblib")
