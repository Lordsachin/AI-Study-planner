# AI Study Planner

AI Study Planner is a Flask-based web application that leverages Machine Learning to predict student exam scores and provide personalized study recommendations. By tracking study hours, attendance, and previous performance, the app helps students manage their academic effort effectively.

## Features

- **User Authentication**: Secure sign-up and login system using `bcrypt`.
- **Score Prediction**: Utilizes a Scikit-Learn Linear Regression model to predict final scores based on:
  - Previous Score
  - Study Hours (Before & After)
  - Attendance
- **Personalized Recommendations**: Provides priority levels (High, Medium, Low) and actionable suggestions based on predicted performance and effort momentum.
- **Progress Tracking**: Saves and displays a history of study records and predictions on a tailored user dashboard.

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Machine Learning**: Scikit-Learn, Pandas, NumPy
- **Database**: SQLite
- **Authentication**: bcrypt
- **Frontend**: HTML/CSS/JS (Jinja2 Templates)

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Lordsachin/AI-Study-planner.git
   cd AI-Study-planner
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate Data and Train the Model**:
   Run the data generation script (if applicable) and train the ML model.
   ```bash
   python ml_model.py
   ```
   *(This will create the `data/study_planner_model.pkl` file required for predictions.)*

5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the App**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Project Structure

- `app.py`: Main Flask application handling routes, user sessions, and API endpoints.
- `ml_model.py`: Script to train and save the Scikit-Learn Linear Regression model.
- `models.py`: SQLAlchemy database models (`User` and `StudyRecord`).
- `generate_data.py`: Script for generating synthetic student training data.
- `requirements.txt`: Python package dependencies.
- `templates/` & `static/`: Frontend HTML templates and static assets.

## License
This project is open-source and available under the [MIT License](LICENSE).
