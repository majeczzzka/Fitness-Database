import sqlite3
from tabulate import tabulate

# Create a connection to the SQLite database
conn = sqlite3.connect("fitness.db")
cursor = conn.cursor()

# Query to calculate if users are meeting their sleep goals based on available records # noqa
sleep_goal_query = """
SELECT
    u.UserID,
    u.Username,
    u.SleepGoal,
    AVG(s.SleepDuration) AS AverageSleepHours,
    CASE
        WHEN AVG(s.SleepDuration) >= u.SleepGoal THEN 'Yes'
        ELSE 'No'
    END AS MeetingSleepGoal
FROM
    Users u
INNER JOIN
    Sleep s ON u.UserID = s.UserID
WHERE
    s.Date > DATE('now', '-30 day')
GROUP BY
    u.UserID;
"""

# Execute the sleep goal query
cursor.execute(sleep_goal_query)  # transaction
sleep_goal_results = cursor.fetchall()

# Print the sleep goal results in a formatted table
print("Are users meeting their sleep goals based on available records?")
print(
    tabulate(
        sleep_goal_results,
        headers=[
            "UserID",
            "Username",
            "Sleep Goal",
            "Average Sleep Hours",
            "Meeting Sleep Goal",
        ],
        tablefmt="fancy_grid",
    )
)

# Query to find the minimum sleep duration for each user when their sleep quality was 'Good' # noqa
min_sleep_quality_query = """
SELECT
    u.UserID,
    u.Username,
    MIN(s.SleepDuration) AS MinSleepDurationForGoodQuality
FROM
    Users u
INNER JOIN
    Sleep s ON u.UserID = s.UserID
WHERE
    s.SleepQuality = 'Good'
    AND s.Date > DATE('now', '-30 day')
GROUP BY
    u.UserID;
"""

# Execute the sleep quality query and fetch the results
cursor.execute(min_sleep_quality_query)  # transaction
min_sleep_for_good_quality_results = cursor.fetchall()

# Print the minimum sleep duration for good quality results in a formatted table # noqa
print("\nMinimum sleep duration when users felt the sleep quality was 'Good':")
print(
    tabulate(
        min_sleep_for_good_quality_results,
        headers=[
            "UserID",
            "Username",
            "Min Sleep Duration For Good Quality",
        ],
        tablefmt="fancy_grid",
    )
)

# Query to calculate BMI for each user and categorize it
bmi_query = """
SELECT
    u.UserID,
    u.Username,
    (u.Weight / ((u.Height / 100.0) * (u.Height / 100.0))) AS BMI,
    CASE
        WHEN (u.Weight / ((u.Height / 100.0) * (u.Height / 100.0))) < 18.5 THEN 'Underweight' 
        WHEN (u.Weight / ((u.Height / 100.0) * (u.Height / 100.0))) BETWEEN 18.5 AND 24.9 THEN 'Healthy weight'
        WHEN (u.Weight / ((u.Height / 100.0) * (u.Height / 100.0))) BETWEEN 25 AND 29.9 THEN 'Overweight'
        ELSE 'Obese'
    END AS BMICategory
FROM
    Users u;
"""  # noqa

# Execute the BMI query and fetch the results
cursor.execute(bmi_query)  # transaction
bmi_results = cursor.fetchall()

# Print the BMI results in a formatted table
print("\nBMI for each user:")
print(
    tabulate(
        bmi_results,
        headers=[
            "UserID",
            "Username",
            "BMI",
            "BMI Category",
        ],
        tablefmt="fancy_grid",
    )
)

# Query to find the best and worst performance for each exercise per user
performance_query = """
SELECT
    u.UserID,
    u.Username,
    MAX(w.Duration) AS BestPerformance,
    MIN(w.Duration) AS WorstPerformance
FROM
    Users u
JOIN
    Workouts w ON u.UserID = w.UserID
WHERE
    w.ExerciseName = 'Run 5K'
GROUP BY
    u.UserID, w.ExerciseName;
"""

# Execute the performance query and fetch the results
cursor.execute(performance_query)  # transaction
performance_results = cursor.fetchall()

# Print the performance results in a formatted table
print("\nBest and Worst Performance for each 5K run per user:")
print(
    tabulate(
        performance_results,
        headers=[
            "UserID",
            "Username",
            "Best Performance",
            "Worst Performance",
        ],
        tablefmt="fancy_grid",
    )
)

# Define the query to calculate TDEE for each user
tdee_query = """
SELECT
    sub.Username,
    sub.AvgCalories,
    sub.TDEE,
    CASE
        WHEN sub.AvgCalories > sub.TDEE + 200 THEN 'Decrease caloric intake'
        WHEN sub.AvgCalories < sub.TDEE - 200 THEN 'Increase caloric intake'
        ELSE 'Maintain caloric intake'
    END AS Recommendation
FROM
    (SELECT
        u.UserID,
        u.Username,
        AVG(n.Calories) AS AvgCalories,
        CASE
            WHEN u.PAL = 'Sedentary' THEN u.BMR * 1.2
            WHEN u.PAL = 'Lightly active' THEN u.BMR * 1.375
            WHEN u.PAL = 'Moderately active' THEN u.BMR * 1.55
            WHEN u.PAL = 'Very active' THEN u.BMR * 1.725
            WHEN u.PAL = 'Super active' THEN u.BMR * 1.9
        END AS TDEE
    FROM
        Users u
    JOIN
        Nutrition n ON u.UserID = n.UserID
    GROUP BY
        u.UserID, u.Username, u.PAL, u.BMR
    ) sub
"""

# Execute the TDEE query and fetch the results
cursor.execute(tdee_query)  # transaction
tdee_results = cursor.fetchall()

# Print the TDEE results in a formatted table
print("\nTotal Daily Energy Expenditure (TDEE) for each user:")
print(
    tabulate(
        tdee_results,
        headers=["Username", "Average Calories", "TDEE", "Recommendation"],
        tablefmt="fancy_grid",
    )
)

# Define and execute the query to find the favorite exercise for users
fav_query = """
SELECT
    e.Name AS FavoriteExercise,
    COUNT(u.UserID) AS NumberOfUsers
FROM
    Users u
JOIN
    Exercises e ON u.FavoriteExerciseID = e.ExerciseID
GROUP BY
    e.Name;
"""
cursor.execute(fav_query)  # transaction
fav_results = cursor.fetchall()

# Print the favorite exercise results in a formatted table
print("\nNumber of people who claims each exercise as their favorite:")
print(
    tabulate(
        fav_results,
        headers=["Exercise", "Number of Users"],
        tablefmt="fancy_grid",
    )
)
# Close the database connection
conn.close()
