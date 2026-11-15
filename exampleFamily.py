# Copy this file to family.py and fill in your family's details.
# Do not commit family.py.
# Year is not stored here; santa.py uses the current calendar year.

family = [
    ("Tom", "tom@gmail.com"),
    ("Sally", "sally123@aol.com"),
    ("Mom", "mom@harvard.edu"),
    ("Dad", "father@gmail.com"),
    ("Timmy", "timothy@gmail.com"),
    ("Jane", "jane@gmail.com"),
    ("Kathy", "kathy@hotmail.com"),
    ("Max", "max@protonmail.com")
    ]

# People who should not get each other, either direction.
couples = [
    ("Tom", "Sally"),
    ("Mom", "Dad"),
    ("Jane", "Kathy")
    ]

# (giver, receiver) from last year. One-way: Tom got Mom last year, so Tom
# cannot get Mom this year, but Mom can get Tom.
# --send overwrites this list after all assignment emails succeed.
lastYear = [
    ("Tom", "Mom"),
    ("Sally", "Dad"),
    ("Mom", "Timmy"),
    ("Dad", "Jane"),
    ("Timmy", "Kathy"),
    ("Jane", "Max"),
    ("Kathy", "Tom"),
    ("Max", "Sally"),
    ]

capAmount = 1000

serverEmail = "myFamilySantaBot@gmail.com"

serverPass = "Password1234!@#$"

familyLink = "https://docs.google.com/document/d/DOC/OF/WHAT/PEOPLE/WANT"
