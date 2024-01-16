import os
import shutil
import hashlib
import subprocess

# Find all firmware binaries of type ELF 32-bit LSB executable, and not stripped, copy to new directory for analysis


def remove_all_files(directory):
    """Remove all files in the specified directory."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # remove file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove directory
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def is_desired_executable(file_path):
    """
    Determine if a file is a specific type of executable using the bash 'file' command.
    """
    try:
        result = subprocess.run(["file", file_path], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        return "ELF 32-bit LSB executable" in output and "not stripped" in output
    except Exception as e:
        print(f"Error checking file type of {file_path}: {e}")
        return False


def generate_file_hash(filepath):
    """Generate a hash for a file."""
    hash_algo = hashlib.sha256()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()


def find_and_copy_executables(source_directory, binary_names, target_directory):
    """Find and copy executables with a hash in the filename for uniqueness."""
    matches = []
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file in binary_names:
                full_path = os.path.join(root, file)
                if os.path.isfile(full_path) and is_desired_executable(full_path):
                    file_hash = generate_file_hash(full_path)
                    unique_filename = f"{file}_{file_hash}"
                    target_path = os.path.join(target_directory, unique_filename)
                    shutil.copy(full_path, target_path)
                    matches.append(target_path)
    return matches


output_directory = "/home/danielsokil/Lab/user1342/Tweezer/firmware_binaries"

remove_all_files(output_directory)

find_and_copy_executables(
    "/home/danielsokil/Lab", ["bmminer", "cgminer"], output_directory
)
find_and_copy_executables(
    "/home/danielsokil/Downloads", ["bmminer", "cgminer"], output_directory
)
