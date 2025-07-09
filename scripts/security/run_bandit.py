import subprocess
import datetime
import os

def run_bandit_scan():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(os.path.dirname(__file__), f"bandit_report_{timestamp}.json")
    
    command = [
        "bandit",
        "-r",  # Recursive
        "symbol", # Directory to scan
        "-f", "json", # Output format
        "-o", output_file # Output file
    ]
    
    print(f"Running bandit scan. Output will be saved to {output_file}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Bandit scan completed successfully.")
        print("Stdout:", result.stdout)
        print("Stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Bandit scan failed with error: {e}")
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)
    except FileNotFoundError:
        print("Error: 'bandit' command not found. Make sure Bandit is installed and in your PATH.")

if __name__ == "__main__":
    run_bandit_scan()
