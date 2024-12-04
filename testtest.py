folder_path = 'E:\Hobbie\tectonic_poster\code'

import os

def count_python_lines(folder_path):
    """
    Counts the total number of lines in all Python files within the given folder.

    :param folder_path: Path to the folder containing Python files.
    :return: Total number of lines in Python files.
    """
    total_lines = 0

    # Walk through all files and subdirectories in the given folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):  # Check for Python files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return total_lines

# Example code:
# folder_path = "path/to/your/folder"
# total_lines = count_python_lines(folder_path)
# print(f"Total lines in Python files: {total_lines}")

total_lines = count_python_lines(folder_path)
print(f"Total lines in Python files: {total_lines}")