from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

app = Flask(__name__)

# Connect to PostgreSQL
DATABASE_URL = ""
engine = create_engine(DATABASE_URL)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Define User table
class User(Base):
    __tablename__ = 'users'
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('username', 'email'),
    )

# Create the table (run once)
Base.metadata.create_all(engine)

# Keep track of logged-in user
diganosisClicked = False
loggedIn = False
user = ""

@app.route('/')
def index():
    return render_template('index.html', user=user, loggedIn=loggedIn, diganosisClicked=diganosisClicked)

@app.route('/login', methods=["GET", "POST"])
def login():
    global loggedIn, user
    return redirect(url_for("index"))

@app.route('/signUp', methods=["GET", "POST"])
def signUp():
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():
    return render_template('about.html')

@app.route('/diagnosis', methods=["POST"])
def diagnosis():
    global diganosisClicked

    if loggedIn == False:
        diganosisClicked = True
        return redirect(url_for("index")) 

    action = request.form.get('action')
    print(action)
    if diganosisClicked == True:
        diganosisClicked = False
    return render_template('diagnosis.html')

@app.route('/signOut')
def signOut():
    global loggedIn, user
    loggedIn = False
    user = ""
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

