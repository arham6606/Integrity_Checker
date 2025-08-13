import argparse
from scanner import check_integrity
import baseline
import warnings

# Suppress plyer dbus warning if using notify-send
warnings.filterwarnings("ignore", category=UserWarning, module="plyer.platforms.linux.notification")



def main():
    
    parser = argparse.ArgumentParser(description="File Integrity Checker...")
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update base line with current file hashes"
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if files are touched..."
    )

    command =parser.parse_args()

    if command.update:
        print("Updating the base line..")
        baseline.base_line()
    elif command.check:
        print("Checking file intergrity..")
        check_integrity()
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
