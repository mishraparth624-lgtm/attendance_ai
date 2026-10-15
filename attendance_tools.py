import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).with_name("students.json")

VALID_STATUSES = {"Present", "Absent"}


def load_data():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def get_student(data, roll_no):
    for student in data["students"]:
        if student["roll_no"] == str(roll_no):
            return student

    raise ValueError("Student not found")


def calculate_student_attendance(student):
    records = student["attendance"]

    total_days = sum(
        status in VALID_STATUSES
        for status in records.values()
    )

    present_days = sum(
        status == "Present"
        for status in records.values()
    )

    percentage = (
        round(present_days / total_days * 100, 2)
        if total_days else 0.0
    )

    return {
        "name": student["name"],
        "roll_no": student["roll_no"],
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": total_days - present_days,
        "attendance_percentage": percentage
    }


def mark_attendance(roll_no, attendance_date, status):
    if status not in VALID_STATUSES:
        raise ValueError("Status must be Present or Absent")

    date.fromisoformat(attendance_date)

    data = load_data()
    student = get_student(data, roll_no)

    if attendance_date not in student["attendance"]:
        raise ValueError("Date not found in attendance records")

    student["attendance"][attendance_date] = status
    save_data(data)

    return calculate_student_attendance(student)


def remove_attendance(roll_no, attendance_date):
    date.fromisoformat(attendance_date)

    data = load_data()
    student = get_student(data, roll_no)

    if attendance_date not in student["attendance"]:
        raise ValueError("Date not found in attendance records")

    student["attendance"][attendance_date] = "Not Marked"
    save_data(data)

    return calculate_student_attendance(student)


def get_attendance_report():
    data = load_data()

    return [
        calculate_student_attendance(student)
        for student in data["students"]
    ]


def get_class_average():
    report = get_attendance_report()

    if not report:
        return {"class_average_percentage": 0.0}

    average = sum(
        student["attendance_percentage"]
        for student in report
    ) / len(report)

    return {
        "class_average_percentage": round(average, 2),
        "student_count": len(report)
    }


if __name__ == "__main__":
    print("STUDENT ATTENDANCE REPORT")

    for student in get_attendance_report():
        print(json.dumps(student, indent=2))

    print("\nCLASS AVERAGE")
    print(json.dumps(get_class_average(), indent=2))