import unittest
from sqlalchemy import create_engine, select, inspect, exc
from insert_data import users, exercises
from datetime import datetime


# Define a class for our database tests, inheriting from unittest.TestCase
class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This method sets up the class-level fixtures. Here, we establish a connection # noqa
        # to the database that will be used for all tests in this class.
        cls.engine = create_engine("sqlite:///fitness.db")
        cls.connection = cls.engine.connect()
        cls.inspector = inspect(
            cls.engine
        )  # This will help us inspect database metadata.

    def test_tables_exist(self):
        # Test to ensure all necessary tables exist in the database.
        tables = self.inspector.get_table_names()
        # Assert that each table is present.
        self.assertIn("Users", tables)
        self.assertIn("Exercises", tables)
        self.assertIn("Workouts", tables)
        self.assertIn("Nutrition", tables)
        self.assertIn("Sleep", tables)

    def test_data_integrity_positive(self):
        # Positive test for data integrity: Checks if all emails in the Users table are unique. # noqa
        result = self.connection.execute(select(users.c.Email).distinct())
        distinct_emails = result.fetchall()  # Fetch distinct emails
        result = self.connection.execute(select(users.c.Email))
        all_emails = result.fetchall()  # Fetch all emails
        # The number of distinct emails should equal the total number of emails if they are all unique. # noqa
        self.assertEqual(len(distinct_emails), len(all_emails))

    def test_data_integrity_negative(self):
        # Negative test for data integrity: Attempts to insert a user with an existing email. # noqa
        # This should raise an IntegrityError due to the unique constraint on the email field. # noqa
        with self.assertRaises(exc.IntegrityError):
            self.connection.execute(
                users.insert().values(
                    Email="hross@example.net",  # Assuming this email already exists # noqa
                    Username="newuser",
                    DateOfBirth=datetime.strptime(
                        "2000-01-01", "%Y-%m-%d"
                    ).date(),  # noqa
                    Gender="Other",
                    SleepGoal=8,
                    PAL="Moderately active",
                )
            )

    def test_foreign_key_constraints_positive(self):
        # Positive test for foreign key constraints: Checks if FavoriteExerciseID in Users # noqa
        # references an existing ExerciseID in Exercises.
        result = self.connection.execute(select(users.c.FavoriteExerciseID))
        for row in result:
            if row[0] is not None:  # Skip None values
                ex_result = self.connection.execute(
                    select(exercises.c.ExerciseID).where(
                        exercises.c.ExerciseID == row[0]
                    )
                )
                # Assert that a corresponding ExerciseID exists for every FavoriteExerciseID. # noqa
                self.assertIsNotNone(
                    ex_result.fetchone(),
                    f"No matching exercise found for valid FavoriteExerciseID: {row[0]}",  # noqa
                )

    def test_foreign_key_constraints_negative(self):
        # Negative test for foreign key constraints: Checks if a non-existent ExerciseID # noqa
        # (here, 9999) is correctly not found in the Exercises table.
        invalid_exercise_id = 9999  # Assuming this ID does not exist
        result = self.connection.execute(
            select(exercises.c.ExerciseID).where(
                exercises.c.ExerciseID == invalid_exercise_id
            )
        )
        # Assert that no record is found for the invalid ExerciseID.
        self.assertIsNone(
            result.fetchone(),
            f"Unexpectedly found a match for invalid FavoriteExerciseID: {invalid_exercise_id}",  # noqa
        )

    def test_data_types(self):
        # Test to validate the data types of columns in the Users table.
        columns = self.inspector.get_columns("Users")
        for column in columns:
            if column["name"] == "UserID":
                # Check if UserID column is of integer type.
                self.assertEqual(column["type"].python_type, int)
            elif column["name"] == "Email":
                # Check if Email column is of string type.
                self.assertEqual(column["type"].python_type, str)

    def test_queries_positive(self):
        # Positive test for queries: Checks if querying the Users table
        # for 'Sedentary' PAL returns results.
        result = self.connection.execute(
            select(users).where(users.c.PAL == "Sedentary")
        )
        # Assert that the query returns one or more records.
        self.assertGreater(len(result.fetchall()), 0)

    def test_queries_negative(self):
        # Negative test for queries: Checks if querying the Users table
        # for a non-existent PAL value ('NonExistingPAL') returns no results.
        result = self.connection.execute(
            select(users).where(users.c.PAL == "NonExistingPAL")
        )
        # Assert that the query returns no records.
        self.assertEqual(len(result.fetchall()), 0)

    @classmethod
    def tearDownClass(cls):
        # This method is called after all the tests have run. Here, we close the database connection. # noqa
        cls.connection.close()


if __name__ == "__main__":
    unittest.main()
