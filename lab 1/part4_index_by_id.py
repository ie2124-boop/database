"""Part 4: Indexing with a Dictionary (id -> row)
This mimics a database index for fast lookups.
"""

students = [
    {"id": 1, "name": "Alice", "school": "GSAS", "credits": 32},
    {"id": 2, "name": "Bob", "school": "Tandon", "credits": 30},
    {"id": 3, "name": "Carol", "school": "GSAS", "credits": 40},
    {"id": 4, "name": "Dan", "school": "CAS", "credits": 18}
]

# Build an index: id -> student row
index_by_id = {}
for row in students:
    index_by_id[row["id"]] = row

# TODO 1: Use index_by_id to print the record for id=3
print("task 1")
print(index_by_id[3])
def find_by_id(index, student_id):
    """Return the row for student_id, or None if missing."""
    return index.get(student_id)


# TODO 3: Insert a new student into BOTH students and index_by_id
#   Example: {"id": 5, "name": "Eve", "school": "CAS", "credits": 22}
print("task 3")
new_student = {"id": 5, "name": "Eve", "school": "CAS", "credits": 22}

students.append(new_student)
index_by_id[new_student["id"]] = new_student

# TODO 4: Update a student’s credits using the index (show list reflects it too)
print("task 4")
index_by_id[5]["credits"] = 25

# show that students list reflects the change
for student in students:
    if student["id"] == 5:
        print(student)

# Reflection (answer in a comment):
# TODO: Why is dict lookup conceptually faster than scanning a list?
#dont have to go thru everything to find stuff. O(1)