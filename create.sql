/*
Third Normal Form
*/


-- Check and create Users Table 
/*
Captures user-specific data, which is fundamental for personalizing the app experience and tailoring health and fitness recommendations.
*/

IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Users]') AND type in (N'U'))
BEGIN
    -- If the Users table does not exist, create it
    CREATE TABLE dbo.Users
    (
        UserID INT PRIMARY KEY IDENTITY(1,1),
        --- primary key
        Username NVARCHAR(255) NOT NULL,
        Email NVARCHAR(255) NOT NULL UNIQUE,
        DateOfBirth DATE NOT NULL,
        Gender NVARCHAR(50) CHECK (Gender IN ('Male', 'Female', 'Other')),
        Height FLOAT,
        Weight FLOAT,
        SleepGoal FLOAT NOT NULL,
        PAL NVARCHAR(50) CHECK (PAL IN ('Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Super active')),
        BMR FLOAT,
        FavoriteExerciseID INT,
        FOREIGN KEY (FavoriteExerciseID) REFERENCES dbo.Exercises(ExerciseID)
    );
END;

/*
Facilitates tracking of various exercises, helping users and the app to monitor and suggest workouts based on intensity levels.
*/
-- Check and create Exercises Table
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Exercises]') AND type in (N'U'))
BEGIN
    -- If the Exercises table does not exist, create it
    CREATE TABLE dbo.Exercises
    (
        ExerciseID INT PRIMARY KEY IDENTITY(1,1),
        Name NVARCHAR(255) NOT NULL,
        Intensity NVARCHAR(50) CHECK (Intensity IN ('Light', 'Moderate', 'Hard', 'Very Hard'))
    );
END;

-- Check and create Workouts Table
/*
Essential for tracking the frequency, duration, and intensity of workouts, crucial for assessing fitness progress and adjusting goals.
*/
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Workouts]') AND type in (N'U'))
BEGIN
    -- If the Workouts table does not exist, create it
    CREATE TABLE dbo.Workouts
    (
        WorkoutID INT PRIMARY KEY IDENTITY(1,1),
        --- primary key
        UserID INT NOT NULL,
        Date DATE NOT NULL,
        ExerciseName NVARCHAR(255),
        Duration INT,
        Intensity NVARCHAR(50),
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
        --- foreign key
    );
END;

-- Check and create Nutrition Table
/*
Critical for monitoring caloric intake, a key component in weight management and overall health.
*/
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Nutrition]') AND type in (N'U'))
BEGIN
    -- If the Nutrition table does not exist, create it
    CREATE TABLE dbo.Nutrition
    (
        NutritionID INT PRIMARY KEY IDENTITY(1,1),
        --- primary key
        UserID INT NOT NULL,
        Date DATE NOT NULL,
        Calories INT,
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
        --- foreign key
    );
END;

-- Check and create Sleep Table
/*
Sleep is a vital part of health; tracking duration and quality aids in understanding its impact on physical and mental well-being.
*/
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Sleep]') AND type in (N'U'))
BEGIN
    -- If the Sleep table does not exist, create it
    CREATE TABLE dbo.Sleep
    (
        SleepID INT PRIMARY KEY IDENTITY(1,1),
        --- primary key
        UserID INT NOT NULL,
        Date DATE NOT NULL,
        SleepDuration INT,
        SleepQuality NVARCHAR(50) CHECK (SleepQuality IN ('Good', 'Fair', 'Poor')),
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
        --- foreign key
    );
END;


/*
The relational structure, 
especially foreign keys linking user activities to their profile, 
facilitates data integrity and relevant associations, essential for accurate analysis and recommendations.
*/