import os
from datetime import datetime
import json

LOG_FILE = "logs/integrity_log.txt"

def log_results(file_path, status):
    """Logs the file integrity check result with a timestamp."""
    
    # Type validation
    if not isinstance(file_path, str) or not isinstance(status, str):
        print("Invalid file path or status type. Both must be strings.")
        return False
    
    try:
        # Ensure log directory exists
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        
        # Append to log file
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} | {file_path} | {status}\n")
        
        return True
    
    except (PermissionError, IOError) as e:
        print(f"Logging Error: {e}")
        return False

def load_monitored_files(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        # Expecting the format: { "files_to_monitor": [ ... ] }
        if "files_to_monitor" in data and isinstance(data["files_to_monitor"], list):
            return "\n".join(data["files_to_monitor"])  # New line for each file
        else:
            return "No files_to_monitor found in JSON."

    except Exception as e:
        return f"Error reading JSON: {e}"

