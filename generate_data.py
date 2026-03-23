import pandas as pd
import numpy as np
import os

np.random.seed(42)
num_samples = 500

print(f"Generating synthetic student data with {num_samples} records...")

study_hours_before = np.random.randint(0, 10, num_samples) 
study_hours_after = np.random.randint(0, 10, num_samples)
attendance = np.random.randint(20, 101, num_samples)
previous_score = np.random.randint(40, 96, num_samples)

# Calculating true momentum based on difference in study habits natively!
delta_hours = study_hours_after - study_hours_before

# If they study MORE than they did previously, they gain points. 
# If they study LESS than they did previously, they lose points.
study_hours_impact = delta_hours * 5.0 

attendance_delta = (attendance - 75) * 0.05
noise = np.random.normal(0, 2.0, num_samples) 

final_score = previous_score + study_hours_impact + attendance_delta + noise
final_score = np.clip(final_score, 0, 100).round().astype(int)

df = pd.DataFrame({
    'study_hours_before': study_hours_before,
    'study_hours_after': study_hours_after,
    'attendance': attendance,
    'previous_score': previous_score,
    'final_score': final_score
})

os.makedirs('data', exist_ok=True)
df.to_csv('data/student_data.csv', index=False)

print("\nSample Data:")
print(df.head())
