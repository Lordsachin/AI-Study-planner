import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os
import warnings
import random

warnings.filterwarnings("ignore", category=UserWarning)

print("Loading data...")
try:
    data = pd.read_csv("data/student_data.csv")
except FileNotFoundError:
    print("Error: data/student_data.csv not found.")
    exit(1)

# Training purely on 4 core dynamic metric features!
X = data[['study_hours_before', 'study_hours_after', 'attendance', 'previous_score']]
y = data['final_score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Linear Regression model...")
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Model Evaluation - MSE: {mse:.2f}")

final_model = LinearRegression()
final_model.fit(X, y)

os.makedirs('data', exist_ok=True)
with open('data/study_planner_model.pkl', 'wb') as f:
    pickle.dump(final_model, f)
print("Model saved to data/study_planner_model.pkl")

def get_priority_and_recommendation(predicted_score, attendance, delta_hours):
    if predicted_score < 60:
        if delta_hours <= 0:
            priority, suggestion = "High", "Your effort dropped. Suggest adding +3 hours/day. Highly recommend peer tutoring to grasp foundations."
        else:
            priority, suggestion = "High", "Good progress. Suggest adding +1 more hour/day and creating a structured schedule."
    elif predicted_score <= 75:
        priority, suggestion = "Medium", "Suggest adding +1 hour/day to clear concepts."
    else:
        priority, suggestion = "Low", "Great job! Maintain this upward momentum."
        
    if attendance < 60:
        suggestion += " WARNING: Attendance rate is low! Even medical history can't save you!!"
    elif attendance < 75:
        suggestion += " WARNING: Attendance rate is low! You might get detained."
        
    return priority, suggestion

def predict_score(study_hours_before, study_hours_after, attendance, previous_score):
    with open('data/study_planner_model.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
    
    prediction = loaded_model.predict([[study_hours_before, study_hours_after, attendance, previous_score]])
    variance = random.randint(-2, 2)
    score = max(0, min(100, int(round(prediction[0])) + variance))
    
    delta_hours = study_hours_after - study_hours_before
    priority, suggestion = get_priority_and_recommendation(score, attendance, delta_hours)
    return score, priority, suggestion
