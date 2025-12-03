import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    # file path and direcotry variables
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    path_exists = os.path.exists(abs_full)

    # error checking for correct directries and files
    if not abs_full.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    if not path_exists:
        return f'Error: File "{file_path}" not found.'
    
    # executing on passed in python file
    try:
        result = subprocess.run([sys.executable, abs_full, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                cwd=abs_working, timeout=30, text=True)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    std_out = result.stdout or ""
    std_error = result.stderr or ""

    if not std_out and not std_error:
        return "No output produced."
    
    # formating for cleaner oputput and showing return code
    output_parts = [f"STDOUT:\n {std_out.strip()}", f"STDERR:\n {std_error.strip()}"]
    if result.returncode != 0:
        output_parts.append(f"Process exited with code {result.returncode}")

    return "\n".join(output_parts)