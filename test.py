from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.schema import PrimaryKeyConstraint

DATABASE_URL = "postgresql+psycopg2://postgres:Partha#2004@localhost/HealthFinder"

# Connect to the database
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define the User table with a composite primary key
class User(Base):
    __tablename__ = 'users'
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('username', 'email'),
    )

# Create the table in the database
Base.metadata.create_all(engine)

# Optional: insert a user
Session = sessionmaker(bind=engine)
session = Session()

new_user = User(username='alice', email='alice@example.com', password='securepass123')
session.add(new_user)
session.commit()
session.close()

print("User added and table created.")