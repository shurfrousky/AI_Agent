from functions.get_file_content import *

print("Showing file content:")
print(get_file_content("calculator", "main.py"))
print("Showing file content:")
print(get_file_content("calculator", "pkg/calculator.py"))
print("Showing file content:")
print(get_file_content("calculator", "/bin/cat"))
print("Showing file content:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))