from faker import Faker
import random
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    MetaData,
    ForeignKey,
    Date,
    Float,
    String,
    insert,
)
from sqlalchemy.exc import IntegrityError

# Creating a Faker instance to generate fake data
fake = Faker()

# Establishing a connection to the SQLite database named 'fitness.db'
# The 'echo=True' flag is set to log all the generated SQL statements
engine = create_engine("sqlite:///fitness.db", echo=True)

# Creating an instance of MetaData, a container object that keeps together different features of a database# noqa
metadata = MetaData()

# Define the structure of the 'Users' table reflecting the existing database schema # noqa
# This table includes various user attributes such as username, email, etc.
users = Table(
    "Users",
    metadata,
    Column(
        "UserID", Integer, primary_key=True
    ),  # The use of primary keys automatically creates indices in the database. # noqa
    Column("Username", String(255), nullable=False),
    Column("Email", String(255), nullable=False, unique=True),
    Column("DateOfBirth", Date, nullable=False),
    Column("Gender", String(50), nullable=False),
    Column("Height", Float),
    Column("Weight", Float),
    Column("SleepGoal", Integer, nullable=False),
    Column("PAL", String(50), nullable=False),  # Physical Activity Level
    Column("BMR", Float),  # Basal Metabolic Rate
    Column("FavoriteExerciseID", Integer, ForeignKey("Exercises.ExerciseID")),
)

# Similarly defining the structure for other tables: 'Exercises', 'Workouts', 'Nutrition', and 'Sleep' # noqa
exercises = Table(
    "Exercises",
    metadata,
    Column("ExerciseID", Integer, primary_key=True),
    Column("Name", String(255), nullable=False),
    Column("Intensity", String(50), nullable=False),
)

workouts = Table(
    "Workouts",
    metadata,
    Column("WorkoutID", Integer, primary_key=True),
    Column("UserID", Integer, ForeignKey("Users.UserID"), nullable=False),
    Column("Date", Date, nullable=False),
    Column("ExerciseName", String(255)),  # Name of the exercise
    Column("Duration", Integer),  # Duration of the workout
    Column("Intensity", String(50)),  # Intensity of the workout
)

nutrition_logs = Table(
    "Nutrition",
    metadata,
    Column("NutritionID", Integer, primary_key=True),
    Column("UserID", Integer, ForeignKey("Users.UserID"), nullable=False),
    Column("Date", Date, nullable=False),
    Column("Calories", Integer),  # Number of calories consumed
)

sleep_records = Table(
    "Sleep",
    metadata,
    Column("SleepID", Integer, primary_key=True),
    Column("UserID", Integer, ForeignKey("Users.UserID"), nullable=False),
    Column("Date", Date, nullable=False),
    Column("SleepDuration", Integer),  # Duration of sleep
    Column("SleepQuality", String(50), nullable=False),  # Quality of sleep
)

# Create the tables in the database if they don't already exist
metadata.create_all(engine)

# Start a new transaction to insert data into the database
with engine.connect() as connection:
    try:
        user_ids = (
            []
        )  # List to keep track of user IDs for reference in other tables # noqa

        # Inserting fake data into the database
        for _ in range(10):  # Looping to create a set number of records
            # Inserting fake user data
            for i in range(10):
                fake_user = insert(users).values(
                    Username=fake.user_name(),
                    Email=fake.unique.email(),  # Generating a unique email
                    DateOfBirth=fake.date_of_birth(
                        minimum_age=18, maximum_age=90
                    ),  # noqa
                    Gender=random.choice(["Male", "Female", "Other"]),
                    Height=round(random.uniform(150, 200), 2),
                    Weight=round(random.uniform(50, 120), 2),
                    SleepGoal=random.randint(6, 12),
                    PAL=random.choice(
                        [
                            "Sedentary",
                            "Lightly active",
                            "Moderately active",
                            "Very active",
                            "Super active",
                        ]
                    ),
                    BMR=round(random.uniform(1200, 2500), 2),
                )
                result = connection.execute(fake_user)  # insertion transaction
                user_id = result.inserted_primary_key[0]
                user_ids.append(user_id)

                # Updating the favorite exercise for each user
                connection.execute(
                    users.update()
                    .values(FavoriteExerciseID=random.randint(1, 11))
                    .where(users.c.UserID == user_id)
                )  # insertion transaction

            # Inserting fake exercise data
            exercise_ids = []
            fake_exercise = insert(exercises).values(
                Name=[
                    "Run 5K",
                    "Weight Lifting",
                    "Crossfit",
                    "Stretching",
                    "Run 10K",
                    "Swimming",
                    "Boxing",
                    "Jogging",
                    "Yoga",
                    "Cycling",
                ][_],
                Intensity=random.choice(
                    ["Light", "Moderate", "Hard", "Very Hard"]
                ),  # noqa
            )
            result = connection.execute(fake_exercise)  # insertion transaction
            exercise_ids.append(result.inserted_primary_key[0])

            # Inserting fake workout data for each user
            for _ in range(10):
                fake_workout = insert(workouts).values(
                    UserID=random.randint(user_ids[0], user_ids[-1]),
                    Date=fake.date_between(start_date="-30d", end_date="today"),  # noqa
                    ExerciseName=random.choice(
                        ["Run 5K", "Weight Lifting", "Crossfit", "Stretching"]
                    ),
                    Duration=random.randint(20, 120),
                    Intensity=random.choice(
                        ["Light", "Moderate", "Hard", "Very Hard"]
                    ),  # noqa
                )
                connection.execute(fake_workout)  # insertion transaction

            # Inserting fake sleep record data for each user
            for _ in range(10):
                fake_sleep_record = insert(sleep_records).values(
                    UserID=random.randint(user_ids[0], user_ids[-1]),
                    Date=fake.date_between(start_date="-30d", end_date="today"),  # noqa
                    SleepDuration=random.randint(4, 12),
                    SleepQuality=random.choice(["Good", "Fair", "Poor"]),
                )
                connection.execute(fake_sleep_record)  # insertion transaction

            # Inserting fake nutrition log data for each user
            for _ in range(3):  # Assuming three meals a day
                fake_nutrition_log = insert(nutrition_logs).values(
                    UserID=user_id,
                    Date=fake.date_between(start_date="-30d", end_date="today"),  # noqa
                    Calories=random.randint(1200, 3500),
                )
                connection.execute(fake_nutrition_log)  # insertion transaction

        # Commit the transaction if no errors occur
        connection.commit()
    except IntegrityError as e:
        # Handle any integrity errors encountered during data insertion
        print(f"An integrity error occurred: {e}")
        connection.rollback()  # Rollback the transaction in case of an error
