import os

# Write to a existing or new file. creates new directory if there is none.
def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    passed_in_dir = os.path.dirname(abs_full)

    if not abs_full.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
    
    try:
        os.makedirs(passed_in_dir, exist_ok=True)
        with open(abs_full, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'        
