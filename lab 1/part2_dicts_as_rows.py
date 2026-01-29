"""Part 2: Dictionaries as Rows
Each row is a dict: {"id": ..., "name": ..., ...}
Schema becomes explicit and safer to access.
"""

students = [
    {"id": 1, "name": "Alice", "school": "GSAS", "credits": 32},
    {"id": 2, "name": "Bob", "school": "Tandon", "credits": 28},
    {"id": 3, "name": "Carol", "school": "GSAS", "credits": 40},
    {"id": 4, "name": "Dan", "school": "CAS", "credits": 18}
]

# TODO 1: Print all student names
print("task 1")
for student in students:
    print(student["name"])
# TODO 2: Print only GSAS students (name + credits)
print("task 2")
for student in students:
    if student['school']=="GSAS":
        print(student["name"], student["credits"])
# TODO 3: Add a new field to each row:
#   status='full-time' if credits >= 30 else 'part-time'
print("task 3")
def status():
    for student in students:
      if student["credits"]>=30:
          student["status"]="full-time"
      else:
          student["status"]="part-time"
status()
# TODO 4: Update Bob’s credits to 30 AND ensure his status updates correctly
def credit_up(name, credit):
    for student in students:
        if student["name"]==name:
            student["credits"]=credit
    status()
credit_up("Bob", 30)


def get_students_by_school(rows, school):
    """Return a list of rows where row['school'] == school."""
    # TODO 5: implement
    result = []
    for row in rows:
        if row["school"] == school:
            result.append(row)
    return result

# TODO 6: Call get_students_by_school(students, "GSAS") and print results
print("task 6")
gsas_students = get_students_by_school(students, "GSAS")
for student in gsas_students:
    print(student)

# Reflection (answer in a comment):
# TODO: Why is dict-based code safer than index-based list code?
#Dict-based code is safer because fields are accessed by name instead of position.
