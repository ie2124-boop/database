"""Part 1: Lists as Tables
Each row is a list: [id, name, school, credits]
Schema is implicit — your code depends on correct indexes.
"""

students = [
    [1, "Alice", "GSAS", 32],
    [2, "Bob", "Tandon", 28],
    [3, "Carol", "GSAS", 40],
    [4, "Dan", "CAS", 18]
]
# columns: [id, name, school, credits]

# TODO 1: Print all student names (one per line)
print("task 1")
for student in students:
    print(student[1])
# TODO 2: Print only the students in GSAS (id and name)
print("task 2")
for student in students:
    if student[2]=="GSAS":
        print(student[0], student[1])
# TODO 3: Print students with credits > 30 (name and credits)
print("task 3")
for student in students:
    if student[3]>30:
        print(student[0], student[1])
# TODO 4: Insert a new student row for: id=5, name='Eve', school='CAS', credits=22
print("task 4")
students.append([5, "Eve", "CAS", 22])
print(students)

# TODO 5: Update Bob’s credits to 30
students[1][3]=30
print(students)
# Reflection (answer in a comment):
# TODO: What breaks if we insert a new column at position 2?
#everything will break, indexes will shift and the codes that is to do with indexes beyond 2 would not work.