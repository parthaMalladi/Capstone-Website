import os
from flask import Flask, render_template, request, url_for, redirect
from db import db_session, Base, engine
from schemas import User, Diagnostic, DiabetesDiagnostic, StrokeDiagnostic, HeartDiseaseDiagnostic, DiabetesStats, StrokeStats, HeartDiseaseStats
from sqlalchemy import inspect
import joblib
import numpy as np
import pandas as pd
from insert_stats import getInfo, insertStats

app = Flask(__name__)

# creates database tables
Base.metadata.create_all(engine)

# Keep track of logged-in user and predictions
diagnosisClicked = False
loggedIn = False
user = ""
currPredict = ""
currID = 0

# for the homepage
@app.route('/')
def index():
    if loggedIn:
        curr = db_session.query(User).filter_by(username=user).first()
        if curr.consent == False:
            return redirect(url_for("consent"))

    return render_template('index.html', user=user, loggedIn=loggedIn, diagnosisClicked=diagnosisClicked)

# for the consent and HIPAA compliance page
@app.route('/consent', methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        answer = request.form["action"]
        curr = db_session.query(User).filter_by(username=user).first()

        if answer == "disagree":
            curr.consent = False
            db_session.commit()
            return redirect(url_for("signOut"))
        else:
            curr = db_session.query(User).filter_by(username=user).first()
            curr.consent = True
            db_session.commit()
            return redirect(url_for("index"))  

    return render_template('consent.html')

# for the login page
@app.route('/login', methods=["GET", "POST"])
def login():
    loginFeedback = "DNE"
    global loggedIn, user, diagnosisClicked

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # SQL query to get user info
        user_obj = db_session.query(User).filter_by(username=username).first()

        # Check if user exists
        if user_obj:
            storedPassword = user_obj.password
            if password == storedPassword:
                loggedIn = True
                user = username
                diagnosisClicked = False
                return redirect(url_for("index"))
            else:
                loginFeedback = "passwordDNE"
        else:
            loginFeedback = "userDNE"

    return render_template('login.html', loginFeedback=loginFeedback)

# for the sign-up page
@app.route('/signUp', methods=["GET", "POST"])
def signUp():
    accountStatus = "DNE"

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if user already exists by username
        existing_user = db_session.query(User).filter_by(username=username).first()

        if existing_user:
            return render_template("signUp.html", accountStatus="Exists")

        # Create and insert new user
        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db_session.add(new_user)
        db_session.commit()
        accountStatus = "Created"

    return render_template('signUp.html', accountStatus=accountStatus)

# for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# for the user profile page where they can see their past queries
@app.route('/profile')
def profile():
    currAccount = db_session.query(User).filter_by(username=user).first()
    diagnostics = currAccount.diagnostics

    # arrays to store the various diagnostic history
    heart_diagnostics = []
    stroke_diagnostics = []
    diabetes_diagnostics = []

    # Fetch each specific diagnostic subtype
    for d in diagnostics:
        detail = None

        if d.diagnostic_type == "heart":
            detail = db_session.query(HeartDiseaseDiagnostic).filter_by(diagnostic_id=d.diagnostic_id).first()
        elif d.diagnostic_type == "stroke":
            detail = db_session.query(StrokeDiagnostic).filter_by(diagnostic_id=d.diagnostic_id).first()
        elif d.diagnostic_type == "diabetes":
            detail = db_session.query(DiabetesDiagnostic).filter_by(diagnostic_id=d.diagnostic_id).first()

        # inspect all the columns of each user diagnosis
        temp = []
        mapper = inspect(detail.__class__)
        for column in mapper.attrs:
            value = getattr(detail, column.key)
            temp.append((column.key, value))

        if d.diagnostic_type == "heart":
           heart_diagnostics.append(temp)
        elif d.diagnostic_type == "stroke":
            stroke_diagnostics.append(temp)
        elif d.diagnostic_type == "diabetes":
            diabetes_diagnostics.append(temp)

    return render_template('profile.html', heart=heart_diagnostics, stroke=stroke_diagnostics, diabetes=diabetes_diagnostics)

# for the diagnosis page where user can enter their health metrics
@app.route('/diagnosis', methods=["POST"])
def diagnosis():
    global diagnosisClicked

    if loggedIn == False:
        diagnosisClicked = True
        return redirect(url_for("index")) 

    action = request.form.get('action')
    print(action)
    diagnosisClicked = False
    return render_template('diagnosis.html', action=action)

# not a page but stores the user's inputs from the diagnosis page
@app.route('/result', methods=["POST"])
def result():
    global currPredict, currID
    diagnosisType = request.form.get('diagnosisType')
    username = user

    # Step 1: Add to Diagnostics table
    diagnostic = Diagnostic(
        username=username,
        diagnostic_type=diagnosisType
    )
    db_session.add(diagnostic)
    db_session.commit()

    # Step 2: Add to the corresponding table
    if diagnosisType == 'diabetes':
        diag = DiabetesDiagnostic(
            diagnostic_id=diagnostic.diagnostic_id,
            pregnancies=request.form.get('pregnancies'),
            glucose=request.form.get('glucose'),
            blood_pressure=request.form.get('bloodPressure'),
            skin_thickness=request.form.get('skinThickness'),
            insulin=request.form.get('insulin'),
            bmi=request.form.get('bmi'),
            diabetes_pedigree_function=request.form.get('diabetesPedigreeFunction'),
            age=request.form.get('age')
        )
    elif diagnosisType == 'stroke':
        diag = StrokeDiagnostic(
            diagnostic_id=diagnostic.diagnostic_id,
            gender=request.form.get('gender'),
            age=request.form.get('age'),
            hypertension=request.form.get('hypertension'),
            heart_disease=request.form.get('heart_disease'),
            ever_married=request.form.get('ever_married'),
            work_type=request.form.get('work_type'),
            residence_type=request.form.get('residence_type'),
            avg_glucose_level=request.form.get('avg_glucose_level'),
            bmi=request.form.get('bmi'),
            smoking_status=request.form.get('smoking_status')
        )
    elif diagnosisType == 'heart':
        diag = HeartDiseaseDiagnostic(
            diagnostic_id=diagnostic.diagnostic_id,
            age=request.form.get('age'),
            sex=request.form.get('sex'),
            chest_pain_type=request.form.get('chestPainType'),
            resting_bp=request.form.get('restingBP'),
            cholesterol=request.form.get('cholesterol'),
            fasting_bs=request.form.get('fastingBS'),
            resting_ecg=request.form.get('restingECG'),
            max_hr=request.form.get('maxHR'),
            exercise_angina=request.form.get('exerciseAngina'),
            oldpeak=request.form.get('oldpeak'),
            st_slope=request.form.get('st_slope')
        )
    else:
        return "Invalid diagnosis type", 400

    db_session.add(diag)
    db_session.commit()
    currPredict = diagnosisType
    currID = diagnostic.diagnostic_id

    return redirect(url_for('predict'))

# based on the user's inputs, uses a ML model to predict the risk of stroke, diabetes, or heart disease
@app.route('/predict', methods=['GET'])
def predict():
    prediction = -1

    if currPredict == 'diabetes':
        # load ML models
        model = joblib.load(os.path.join('pickles', 'DiabetesModel.pkl'))

        # column names
        colNames = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

        # get user query from database
        info = db_session.query(DiabetesDiagnostic).filter_by(diagnostic_id=currID).first()

        # create a sample dataframe and predict
        userSample = pd.DataFrame([[np.int64(info.pregnancies), 
                                    np.int64(info.glucose), 
                                    np.int64(info.blood_pressure), 
                                    np.int64(info.skin_thickness), 
                                    np.int64(info.insulin), 
                                    np.float64(info.bmi), 
                                    np.float64(info.diabetes_pedigree_function), 
                                    np.int64(info.age)]], columns=colNames)
        prediction = model.predict(userSample)

    elif currPredict == "stroke":
        # load ML models
        model = joblib.load(os.path.join('pickles', 'StrokeModel.pkl'))
        encoders = joblib.load(os.path.join('pickles', 'StrokeEncoders.pkl'))

        # column names
        categories = ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
        colNames = ['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status']

        # get user query from database
        info = db_session.query(StrokeDiagnostic).filter_by(diagnostic_id=currID).first()

        # create a sample dataframe
        userSample = pd.DataFrame([[info.gender, 
                                    np.float64(info.age), 
                                    np.int64(info.hypertension), 
                                    np.int64(info.heart_disease), 
                                    info.ever_married, 
                                    info.work_type, 
                                    info.residence_type, 
                                    np.float64(info.avg_glucose_level), 
                                    np.float64(info.bmi), 
                                    info.smoking_status]], columns=colNames)
        
        # encode categorical columns to numerical and predict
        for col in categories:
            le = encoders[col]
            userSample[col] = le.transform(userSample[col])

        prediction = model.predict(userSample)

    elif currPredict == "heart":
        # load ML models
        model = joblib.load(os.path.join('pickles', 'HeartModel.pkl'))
        encoders = joblib.load(os.path.join('pickles', 'HeartEncoders.pkl'))

        # column names
        categories = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
        colNames = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope']

        # get user query from database
        info = db_session.query(HeartDiseaseDiagnostic).filter_by(diagnostic_id=currID).first()

        # create a sample dataframe
        userSample = pd.DataFrame([[np.int64(info.age), 
                                    info.sex, 
                                    info.chest_pain_type, 
                                    np.int64(info.resting_bp), 
                                    np.int64(info.cholesterol), 
                                    np.int64(info.fasting_bs), 
                                    info.resting_ecg, 
                                    np.int64(info.max_hr), 
                                    info.exercise_angina, 
                                    np.float64(info.oldpeak), 
                                    info.st_slope]], columns=colNames)
        
        # encode categorical columns to numerical and predict
        for col in categories:
            le = encoders[col]
            userSample[col] = le.transform(userSample[col])
            
        prediction = model.predict(userSample)

    else:
        return "Invalid Query", 400
    
    # get advice and citations
    temp = []

    if currPredict == 'diabetes':
        temp = getInfo(DiabetesDiagnostic, DiabetesStats, currID)
    elif currPredict == "stroke":
        temp = getInfo(StrokeDiagnostic, StrokeStats, currID)
    elif currPredict == "heart":
        temp = getInfo(HeartDiseaseDiagnostic, HeartDiseaseStats, currID)

    return render_template('result.html', type=currPredict, result=prediction, advice=temp[0], cite=temp[1])

# signs out the user
@app.route('/signOut')
def signOut():
    global loggedIn, user
    loggedIn = False
    user = ""
    return redirect(url_for("index"))

# runs the application
if __name__ == '__main__':
    app.run(debug=True)

