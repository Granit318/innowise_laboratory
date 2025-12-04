"""
Student Grade Analyzer
A simple program to manage student records and their academic performance.
"""

students: list[dict] = []


def user_input(msg: str) -> str:
    """
    Get user input with error handling for KeyboardInterrupt and Value errors.

    Args:
        msg (str): The message to display as input prompt

    Returns:
        str: User input text in capitalized format
    """
    try:
        text: str = input(msg).capitalize()
    except ValueError:
        print("Invalid input")
        return user_input(msg)
    except KeyboardInterrupt:
        print("Use menu for exit")
        return user_input(msg)

    return text


def input_grades() -> list[int]:
    """
    Collect grades from user input with validation.

    Returns:
        list[int]: List of valid grades between 0-100

    Notes:
        - Type 'done' to finish entering grades
        - Only accepts integers between 0-100
    """
    grades: list[int] = []
    while True:
        grade_input = user_input("Enter a grade (or 'done' to finish): ")
        if grade_input.lower() == "done":
            return grades
        try:
            grade = int(grade_input)
            if 0 <= grade <= 100:
                grades.append(grade)
            else:
                print("Grade must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid grade. Please enter a number 0-100 or 'done'")


def is_student_exists(name):
    """
    Check if a student with given name already exists.

    Args:
        name (str): Student name to check

    Returns:
        bool: True if student exists, False otherwise
    """
    if name.capitalize() in [i["name"] for i in students]:
        return True
    return False


def add_new_student(name: str) -> None:
    """
    Add a new student to the system.

    Args:
        name (str): Name of the student to add
    """
    global students
    if is_student_exists(name):
        print("Student already exists")
        return None

    student = {"name": name, "grades": []}
    students.append(student)


def add_grades(name: str, grades: list[int]) -> None:
    """
    Add grades to an existing student's record.

    Args:
        name (str): Student name
        grades (list[int]): List of grades to add

    Raises:
        ValueError: If student doesn't exist
    """
    global students
    for student in students:
        if name == student["name"]:
            student["grades"] = grades
            return None
    raise ValueError("Student does not exist")


def show_report() -> None:
    """
    Display a comprehensive report of all students and their performance.

    Shows:
        - Individual student averages
        - Overall statistics (min, max, average)
    """
    global students
    all_grades, all_average_grades = [], []
    for student in students:
        try:
            average = sum(student["grades"]) / len(student["grades"])
            all_average_grades.append(average)
            print(f"{student['name']}'s average grade is {average:.1f}")
        except ZeroDivisionError:
            print(f"{student['name']}'s average grade is N/A")
        all_grades += student["grades"]

    if all_grades:
        min_grade = min(all_grades)
        max_grade = max(all_grades)
        print(f"Max average: {max_grade:.1f}")
        print(f"Min average: {min_grade:.1f}")

    if all_average_grades:
        average = sum(all_average_grades) / len(all_average_grades)
        print(f"Overall average: {average:.1f}")


def find_top_performer() -> None:
    """
    Find and display the student with the highest average grade.

    Features:
        - Excludes students with no grades
        - Handles empty data gracefully
        - Uses lambda function for efficient comparison
    """
    global students

    # Filter out students with no grades or invalid data
    valid_students = []
    for student in students:
        if student["grades"]:  # Only consider students with grades
            try:
                average = sum(student["grades"]) / len(student["grades"])
                valid_students.append((student["name"], average))
            except (ZeroDivisionError, TypeError):
                # Skip students with empty grades or invalid data
                continue

    if not valid_students:
        print("No top student found. Either no students added or no grades available.")
        return

    # Use max() with lambda function as key to find top performer
    top_student = max(valid_students, key=lambda x: x[1])

    print(
        f"Top performer: {top_student[0]} with an average grade of {top_student[1]:.2f}"
    )


def main():
    """
    Main program loop with menu-driven interface.

    Menu Options:
        1. Add new student
        2. Add grades for student
        3. Generate full report
        4. Find top performer
        5. Exit program
    """
    while True:
        print(
            """\n--- Student Grade Analyzer ---
        1. Add a new student
        2. Add grades for a student
        3. Generate a full report
        4. Find the top student
        5. Exit program"""
        )
        choice: str = user_input("Enter your choice: ")
        match choice:
            case "1":
                student_name = user_input("Enter student name: ")
                add_new_student(student_name)
            case "2":
                student_name = user_input("Enter student name: ")
                if not is_student_exists(student_name):
                    print("Student does not exist")
                    continue
                grades = input_grades()
                add_grades(student_name, grades)
            case "3":
                show_report()
            case "4":
                find_top_performer()
            case "5":
                break
            case _:
                print("Invalid input. Please enter a number 1-5.")


if __name__ == "__main__":
    main()
