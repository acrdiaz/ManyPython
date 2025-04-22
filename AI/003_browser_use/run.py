import subprocess
import sys
import os

def main():
    # Path to the sample.py file
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sample_script = f"{script_dir}\\AI\\003_browser_use\\sample.py"

    # Run the sample.py script in a separate process and stream output to the console
    process = subprocess.Popen(
        [sys.executable, sample_script],
        stdout=sys.stdout,  # Stream stdout directly to the console
        stderr=sys.stderr   # Stream stderr directly to the console
    )

    # Wait for the process to complete
    process.wait()

if __name__ == "__main__":
    main()