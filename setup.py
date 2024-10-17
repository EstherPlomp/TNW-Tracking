import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and print its output."""
    try:
        result = subprocess.run(command, check=True, text=True, shell=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        sys.exit(1)

# Setup python environment and possibly other requirements
print("Installing requirements...")
run_command("pip install -r requirements.txt")

print("Python version:")
run_command("python --version")

print("Changing directory and running setup...")
original_dir = os.getcwd()
try:
    os.chdir("find_by_pdf_content/pure_text_analysis")
    run_command("python setup.py")
finally:
    os.chdir(original_dir)

print("Setup completed successfully.")
