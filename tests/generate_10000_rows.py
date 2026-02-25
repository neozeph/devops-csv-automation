import csv
import random

filename = "students_stress_test.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["StudentID", "Name", "Subject", "Grade"])

    for i in range(1, 10001):
        grade = random.randint(-20, 120)  # includes invalid grades
        name = f"Student_{i}"
        subject = random.choice(["Math", "Science", "English"])
        writer.writerow([i, name, subject, grade])

    # Add duplicates
    writer.writerow([1, "Student_1", "Math", 95])
    writer.writerow([2, "Student_2", "Science", 85])

    # Add missing values
    writer.writerow([10001, "", "Math", 90])
    writer.writerow([10002, "Student_10002", "Science", ""])

print("Generated students_stress_test.csv successfully.")