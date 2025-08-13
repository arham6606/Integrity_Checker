#user defined fucntions
import utils
from logger import log_results
import os
import baseline
import json
from notify import send_warnings,send_discord_alerts

import os
import json
import utils
import baseline
from logger import log_results
from notify import send_discord_alerts, send_warnings

def check_integrity():
    """Checks the integrity of monitored files and returns the result text plus file lists."""
    modified_files = []
    delete_files = []
    unchanged_files = []
    result_text = []

    # Baseline file must exist
    if not os.path.isfile(baseline.BASELINE_FILE):
        return "Baseline file not found. Please run baseline.py first.", modified_files, delete_files, unchanged_files
    
    # Load baseline data
    try:
        with open(baseline.BASELINE_FILE, 'r') as f:
            base_line_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return f"Error reading baseline file: {e}", modified_files, delete_files, unchanged_files
    
    # Check each file
    for file_path, hashing in base_line_data.items():
        if not os.path.isfile(file_path):
            delete_files.append(file_path)
            continue
        
        current_hash = utils.calculate_hash_of_file(file_path)
        if current_hash != hashing:
            modified_files.append(file_path)
        else:
            unchanged_files.append(file_path)

    # Build result report
    result_text.append("Integrity Check Report:")

    if modified_files:
        result_text.append("\nModified Files:")
        for f in modified_files:
            result_text.append(f" - {f}")
            log_results(f, "Modified")
            send_warnings("File Integrity Alert", f"{f} has been modified!")
            send_discord_alerts(f"Warning: File modified: {f}")
    else:
        result_text.append("\nNo files modified.")

    if delete_files:
        result_text.append("\nDeleted Files:")
        for d in delete_files:
            result_text.append(f" - {d}")
            log_results(d, "Deleted")
            send_warnings("File Integrity Alert", f"{d} has been deleted!")
            send_discord_alerts(f"Warning: File deleted: {d}")
    else:
        result_text.append("\nNo files deleted.")

    result_text.append(f"\nUnchanged Files: {len(unchanged_files)}")

    return "\n".join(result_text), modified_files, delete_files, unchanged_files
