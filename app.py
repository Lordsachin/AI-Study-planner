from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from models import db, User, StudyRecord
from ml_model import predict_score
import bcrypt
import os

app = Flask(__name__)
# A strong secret key is required for Flask sessions (can be an ENV var in production)
app.config['SECRET_KEY'] = 'ai_study_planner_secure_session_key_!@#'
# Use SQLite database in the root folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure tables are built upon startup
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    """ Render the main dashboard if logged in, otherwise redirect to login. """
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handle user authentication to dashboard. """
    if request.method == 'POST':
        data = request.json
        user = User.query.filter_by(username=data.get('username')).first()
        if user and bcrypt.checkpw(data.get('password').encode('utf-8'), user.password_hash):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True, 'message': 'Logged in successfully'})
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    """ Handle new user registration and password hashing. """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password_hash=hashed_pwd)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/logout')
def logout():
    """ Destroy session and safely sign out user. """
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """ Handle incoming student stats, run the ML prediction, and construct/save the data record. """
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
    data = request.json
    subject = data.get('subject_name')
    hours_before = int(data.get('study_hours_before', 0))
    hours_after = int(data.get('study_hours_after', 0))
    attn = int(data.get('attendance', 0))
    prev_score = int(data.get('previous_score', 0))
    
    # Machine Learning Prediction natively tracking effort momentum
    pred_score, priority, suggestion = predict_score(hours_before, hours_after, attn, prev_score)
    
    # Commit the result using hours_after as the main tracking stat for dashboard history
    record = StudyRecord(
        user_id=session['user_id'],
        subject_name=subject,
        study_hours=hours_after,
        attendance=attn,
        previous_score=prev_score,
        predicted_score=pred_score,
        priority=priority,
        suggestion=suggestion
    )
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'prediction': pred_score,
        'priority': priority,
        'suggestion': suggestion
    })

@app.route('/api/records', methods=['GET'])
def get_records():
    """ Retrieve current user performance records for charting display. """
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
    records = StudyRecord.query.filter_by(user_id=session['user_id']).all()
    records_data = []
    for r in records:
        records_data.append({
            'id': r.id,
            'subject_name': r.subject_name,
            'study_hours': r.study_hours,
            'attendance': r.attendance,
            'previous_score': r.previous_score,
            'predicted_score': r.predicted_score,
            'priority': r.priority,
            'suggestion': r.suggestion,
            'date_added': r.date_added.strftime('%Y-%m-%d')
        })
    return jsonify({'success': True, 'records': records_data})

if __name__ == '__main__':
    # Used for testing via pure execution directly locally
    app.run(debug=True, port=5000)
