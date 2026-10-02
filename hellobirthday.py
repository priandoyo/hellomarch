from datetime import date

name = input("What is your name? ")
dob = input("Date of birth (YYYY-MM-DD): ")

birth_date = date.fromisoformat(dob)
today = date.today()

years = today.year - birth_date.year
months = today.month - birth_date.month
days = today.day - birth_date.day

if days < 0:
    months -= 1
    days += 30

if months < 0:
    years -= 1
    months += 12

print()
print(f"Hello {name}!")
print(f"You are {years} years, {months} months, and {days} days old.")
