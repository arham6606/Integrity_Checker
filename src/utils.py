import hashlib

def calculate_hash_of_file(file_path):
    """
    Calculate the SHA-256 hash of a file.
    
    The file is read in binary mode and processed in chunks to handle large files efficiently.
    Returns:
        str: 64-character hexadecimal SHA-256 hash of the file.
        None: If the file does not exist or cannot be read due to permissions.
    """
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    except (FileNotFoundError, PermissionError):
        return None
