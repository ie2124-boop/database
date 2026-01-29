"""Part 3: Tuples as Records
A tuple is immutable. In databases, 'tuple' can also mean a row/record.
"""

students = [
    (1, "Alice", "GSAS", 32),
    (2, "Bob", "Tandon", 28),
    (3, "Carol", "GSAS", 40)
]
# columns: (id, name, school, credits)

# TODO 1: Print the name for each record
print("task 1")
for student in students:
    print(student[1])

# TODO 2: Try to change Bob’s credits directly (observe the error)
print("task 2: TypeError: 'tuple' object does not support item assignment")
#students[1][3] = 30

# TODO 3: Create a new tuple for Bob with credits=30 and replace the old record in the list
for i, student in enumerate(students):
    if student[1] == "Bob":
        students[i] = (student[0], student[1], student[2], 30)

# Reflection (answer in a comment):
# TODO: Why might immutability be good for data integrity?
#Immutability helps preserve data integrity because records cannot be changed accidentally after creation. 