import csv
from pathlib import Path

DATA_FILE = Path(__file__).with_name("students.csv")


def get_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def load_students():
    students = []

    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            marks = [
                float(row["maths"]),
                float(row["science"]),
                float(row["english"]),
            ]

            if any(mark < 0 or mark > 100 for mark in marks):
                raise ValueError(f"Marks must be between 0 and 100: {row['name']}")

            total = sum(marks)
            average = total / len(marks)

            students.append({
                "name": row["name"],
                "total": total,
                "average": average,
                "grade": get_grade(average),
                "status": "Pass" if all(mark >= 35 for mark in marks) else "Needs improvement",
            })

    return students


def main():
    try:
        students = load_students()
    except (OSError, KeyError, ValueError) as error:
        print(f"Could not read student data: {error}")
        return

    if not students:
        print("No student records found.")
        return

    print("\nSTUDENT PERFORMANCE REPORT")
    print("-" * 76)
    print(f"{'Name':<20}{'Total':>10}{'Average':>12}{'Grade':>10}{'Status':>22}")
    print("-" * 76)

    for student in students:
        print(
            f"{student['name']:<20}"
            f"{student['total']:>10.1f}"
            f"{student['average']:>12.2f}"
            f"{student['grade']:>10}"
            f"{student['status']:>22}"
        )

    topper = max(students, key=lambda student: student["average"])
    class_average = sum(student["average"] for student in students) / len(students)

    print("-" * 76)
    print(f"Class average: {class_average:.2f}")
    print(f"Top performer: {topper['name']} ({topper['average']:.2f})")


if __name__ == "__main__":
    main()
