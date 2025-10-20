from functions.run_python_file import *

print("TEST 1")
print(run_python_file("calculator", "main.py"))
print("TEST 2")
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("TEST 3")
print(run_python_file("calculator", "tests.py"))
print("TEST 4")
print(run_python_file("calculator", "../main.py"))
print("TEST 5")
print(run_python_file("calculator", "nonexistent.py"))
print("TEST 6")
print(run_python_file("calculator", "lorem.txt"))