from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

app = Flask(__name__)

# Connect to PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:Partha#2004@localhost/HealthFinder"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define User table
class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

# Create the table (run once)
Base.metadata.create_all(engine)

# Keep track of logged-in user
diagnosisClicked = False
loggedIn = False
user = ""

@app.route('/')
def index():
    return render_template('index.html', user=user, loggedIn=loggedIn, diagnosisClicked=diagnosisClicked)

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():
    return render_template('about.html')

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

@app.route('/result', methods=["POST"])
def result():
    diagnosisType = request.form.get('diagnosisType')
    return render_template('result.html', diagnosisType=diagnosisType)

@app.route('/signOut')
def signOut():
    global loggedIn, user
    loggedIn = False
    user = ""
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

