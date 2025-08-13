import json
import os

# User-defined module
import utils

# Path to store baseline hashes
BASELINE_FILE = "data/baseline.json"
MONITORED_FILE = "monitored_files.json"

def load_files():
    """
    Load monitored files from the JSON configuration.
    
    Returns:
        list: List of file paths to monitor, or an empty list if
              the file is missing, invalid, or improperly formatted.
    """
    try:
        with open(MONITORED_FILE, 'r', encoding="utf-8") as f:
            config = json.load(f)
        
        files = config.get("files_to_monitor", [])
        
        if not isinstance(files, list):
            print(f"Error: 'files_to_monitor' must be a list in {MONITORED_FILE}")
            return []
        
        return files

    except FileNotFoundError:
        print(f"Config file not found: {MONITORED_FILE}")
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {MONITORED_FILE}: {e}")
        return []




def base_line():
    """
    Create a baseline JSON file with SHA-256 hashes of monitored files.
    
    This baseline serves as a trusted reference for later integrity checks.
    If any file is modified, its hash will no longer match the baseline.

    Returns:
        bool: True if baseline creation was successful, False otherwise.
    """
    # Files to monitor
    files_to_monitor = load_files()
    if not files_to_monitor:
        print("No files to monitor.Add files in monitored_files_json..")
        return []

    if not files_to_monitor:
        print("No files specified for monitoring. Please add files to 'files_to_monitor'.")
        return False
    
    base_data = {}

    for file_path in files_to_monitor:
        # Ensure file path is a valid string
        if not isinstance(file_path, str) or not file_path.strip():
            print(f"Error: Invalid file path entry: {file_path!r}")
            continue

        # Convert to absolute path
        file_path = os.path.abspath(file_path)

        # Ensure the file exists
        if not os.path.isfile(file_path):
            print(f"Invalid path: {file_path} is not a valid file.")
            continue
        
        # Calculate file hash
        hash_value = utils.calculate_hash_of_file(file_path)
        if hash_value:
            base_data[file_path] = hash_value
        else:
            print(f"Failed to hash file: {file_path}") 
    
    # Save baseline data to file
    try:
        os.makedirs(os.path.dirname(BASELINE_FILE) or ".", exist_ok=True)
        with open(BASELINE_FILE, "w") as f:
            json.dump(base_data, f, indent=4)
        print(f"Baseline data saved to {BASELINE_FILE}")
        return True

    except (PermissionError, OSError) as e:
        print(f"Error writing baseline to {BASELINE_FILE}: {e}")
        return False
