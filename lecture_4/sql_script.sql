-- Drop existing tables if they exist
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS grades;

-- Create students table
CREATE TABLE students
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name  TEXT NOT NULL,
    birth_year INTEGER CHECK (birth_year >= 1900)
);

-- Insert sample student data
INSERT INTO students (full_name, birth_year)
VALUES ('Alice Johnson', 2005),
       ('Brian Smith', 2004),
       ('Carla Reyes', 2006),
       ('Daniel Kim', 2005),
       ('Eva Thompson', 2003),
       ('Felix Nguyen', 2007),
       ('Grace Patel', 2005),
       ('Henry Lopez', 2004),
       ('Isabella Martinez', 2006);

-- Create grades table with foreign key constraint
CREATE TABLE grades
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject    TEXT NOT NULL,
    grade      INTEGER CHECK (grade >= 1 AND grade <= 100),
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

-- Insert sample grade data
INSERT INTO grades (student_id, subject, grade)
VALUES (1, 'Math', 88),
       (1, 'English', 92),
       (1, 'Science', 85),
       (2, 'Math', 75),
       (2, 'History', 83),
       (2, 'English', 79),
       (3, 'Science', 95),
       (3, 'Math', 91),
       (3, 'Art', 89),
       (4, 'Math', 84),
       (4, 'Science', 88),
       (4, 'Physical Education', 93),
       (5, 'English', 90),
       (5, 'History', 85),
       (5, 'Math', 88),
       (6, 'Science', 72),
       (6, 'Math', 78),
       (6, 'English', 81),
       (7, 'Art', 94),
       (7, 'Science', 87),
       (7, 'Math', 90),
       (8, 'History', 77),
       (8, 'Math', 83),
       (8, 'Science', 80),
       (9, 'English', 96),
       (9, 'Math', 89),
       (9, 'Art', 92);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_grades_student_id ON grades(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_subject ON grades(subject);

-- Query 1: Get all grades for Alice Johnson
SELECT 'Grades for Alice: ' || subject, grade
FROM grades
WHERE student_id = (SELECT id FROM students WHERE full_name = 'Alice Johnson');

-- Query 2: Average grade per student (ordered highest to lowest)
SELECT s.full_name,
       AVG(g.grade) AS average_grade
FROM students s
         JOIN grades g on s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC;

-- Query 3: Students born after 2004
SELECT full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year;

-- Query 4: Average grade per subject
SELECT subject, AVG(grade) as avg_grade
FROM grades
WHERE grade IS NOT NULL
GROUP BY subject
ORDER BY avg_grade DESC;

-- Query 5: Top 3 students by average grade
SELECT s.full_name, AVG(g.grade) AS avg_grade
FROM students s
         JOIN grades g on s.id = g.student_id
WHERE grade IS NOT NULL
GROUP BY s.full_name
ORDER BY avg_grade DESC LIMIT 3;

-- Query 6: Students with low grades (<80) and count of their low grades
SELECT s.full_name,
    s.birth_year,
    g.subject,
    g.grade,
    (SELECT COUNT(*)
     FROM grades
     WHERE student_id = s.id
       AND grade < 80)
FROM students s
         JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY g.grade ASC, s.full_name;
