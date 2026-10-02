name = input("What is your name? ")
note = input("Write your note: ")

print()
print(f"Hello {name}!")
print(f"Your note: {note}")

with open("hellonote.py", "a") as file:
    file.write(f"\n# {name}: {note}\n")
