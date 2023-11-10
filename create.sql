-- Check and create Users Table
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Users]') AND type in (N'U'))
BEGIN
    -- If the Users table does not exist, create it
    CREATE TABLE dbo.Users
    (
        UserID INT PRIMARY KEY IDENTITY(1,1),
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
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Workouts]') AND type in (N'U'))
BEGIN
    -- If the Workouts table does not exist, create it
    CREATE TABLE dbo.Workouts
    (
        WorkoutID INT PRIMARY KEY IDENTITY(1,1),
        UserID INT NOT NULL,
        Date DATE NOT NULL,
        ExerciseName NVARCHAR(255),
        Duration INT,
        Intensity NVARCHAR(50),
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
    );
END;

-- Check and create Nutrition Table
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Nutrition]') AND type in (N'U'))
BEGIN
    -- If the Nutrition table does not exist, create it
    CREATE TABLE dbo.Nutrition
    (
        NutritionID INT PRIMARY KEY IDENTITY(1,1),
        UserID INT NOT NULL,
        Date DATE NOT NULL,
        Calories INT,
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
    );
END;

-- Check and create Sleep Table
IF NOT EXISTS (SELECT *
FROM sys.objects
WHERE object_id = OBJECT_ID(N'[dbo].[Sleep]') AND type in (N'U'))
BEGIN
    -- If the Sleep table does not exist, create it
    CREATE TABLE dbo.Sleep
    (
        SleepID INT PRIMARY KEY IDENTITY(1,1),
        UserID INT NOT NULL,
        Date DATE NOT NULL,
        SleepDuration INT,
        SleepQuality NVARCHAR(50) CHECK (SleepQuality IN ('Good', 'Fair', 'Poor')),
        FOREIGN KEY (UserID) REFERENCES dbo.Users(UserID)
    );
END;
