from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QCheckBox, QVBoxLayout, QSizePolicy,QPushButton,QSpacerItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
from logger import load_monitored_files,log_results
from scanner import check_integrity
from baseline import base_line
from PyQt5.QtCore import pyqtSignal, QObject
from notify import send_discord_alerts,send_warnings
import warnings


class IntegrityChecker(QObject):
    report_signal = pyqtSignal(str)  # signal to send text to GUI

    def run_check(self, modified_files, delete_files, unchanged_files):
        self.report_signal.emit("Integrity Check Report...")

        if modified_files:
            self.report_signal.emit("\nModified Files")
            for f in modified_files:
                self.report_signal.emit(f"{f}")
                log_results(f, "Modified")
                send_warnings("File Integrity Alert,", f"{f} has been modified!")
                send_discord_alerts(f"Warning: File modified: {f}")
        else:
            self.report_signal.emit("No files modified")

        if delete_files:
            self.report_signal.emit("\nFiles Deleted.")
            for d in delete_files:
                self.report_signal.emit(f"{d}")
                log_results(d, "Deleted")
                send_warnings("File Integrity Alert,", f"{d} has been deleted!")
                send_discord_alerts(f"Warning: File deleted: {d}")
        else:
            self.report_signal.emit("No files deleted...")

        if unchanged_files:
            self.report_signal.emit(f"\nUnchanged Files: {len(unchanged_files)}")




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Integrity Checker")
        self.resize(800, 600)
        self.setMinimumSize(500, 500)

        # Title label
        self.title_label = QLabel("File Integrity Checker")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("""
            QLabel {
                padding: 8px 15px;
                border-radius: 8px;
                background-color: transparent;
            }
            QLabel:hover {
                border: 2px solid #00FF00;
                background-color: rgba(0, 255, 0, 0.15);
            }
        """)

        # Dark mode toggle
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        # Main container layout for files (no QFrame to avoid extra box)
        self.files_container = QWidget()
        self.files_container.setContentsMargins(0,0,1100,0)
       
        self.files_container.setStyleSheet("""
            QWidget {
                border: 2px solid green;
                border-radius: 8px;
                background-color: rgba(0, 255, 0, 0.05);
                padding-top:100px;
                                           
            }
        """)
        self.files_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Files layout
        self.files_layout = QVBoxLayout(self.files_container)
        self.files_layout.setContentsMargins(20, 20, 20, 20)
        self.files_layout.setSpacing(30)

        # Writing text inside the block
        self.files_label = QLabel("Files Being Monitored:")
        self.files_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 30px;
                background-color: transparent;
                border:none;
            }
        """)
        self.files_label.setAlignment(Qt.AlignLeft)

        # Displaying file names
        self.files_names = load_monitored_files("monitored_files.json")
        self.files_names_label = QLabel(self.files_names)
        self.files_names_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 25px;
                background-color: transparent;
                border:none;
                padding-left:200px
                
            }
        """)
        self.files_names_label.setAlignment(Qt.AlignLeft)
        self.files_names_label.setWordWrap(True)

        # Add labels to files layout
        self.files_layout.addWidget(self.files_label)
        self.files_layout.addWidget(self.files_names_label)

             # --- Buttons Layout ---
        self.check_button = QPushButton("Check Integrity")
        self.check_button.setStyleSheet("""
        QPushButton {
            font-size: 25px;
            background-color: green;
            color: white;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: darkgreen;
        }
        """)
        self.integrity_checker = IntegrityChecker()
        self.integrity_checker.report_signal.connect(self.append_result_text)
        self.check_button.clicked.connect(self.run_integrity_check)

        self.update_button = QPushButton("Update Files")
        self.update_button.setStyleSheet("""
        QPushButton {
            font-size: 25px;
            background-color: green;
            color: white;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: darkgreen;
        }
        """)
        self.update_button.clicked.connect(base_line)

        # Vertical button container
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.check_button)
        buttons_layout.addSpacing(30)  # Space between buttons
        buttons_layout.addWidget(self.update_button)
        buttons_layout.setAlignment(Qt.AlignLeft)  # Align left (can change to Qt.AlignCenter or Qt.AlignRight)
        buttons_layout.setContentsMargins(50, 0, 0, 0)  # Left, Top, Right, Bottom margins for both buttons

            # Result label (placeholder for backend output)
        self.result_label = QLabel("Result: [No scan performed yet]")
        self.result_label.setAlignment(Qt.AlignLeft)
        self.result_label.setStyleSheet("""
            font-size: 30px; 
            color:white ;
        """)

        # A layout just for the result area
        self.result_layout = QVBoxLayout()
        self.result_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)

        # Left layout (files list)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.files_container, alignment=Qt.AlignLeft)
        left_layout.setContentsMargins(50, 200, 0, 0)
        left_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()

        # Top bar layout
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.dark_mode_checkbox)

        # Combine everything
        main_layout.addLayout(top_layout)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(self.result_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.set_dark_theme()
    
    def append_result_text(self, text):
        # Append messages to result label instead of overwriting
        current_text = self.result_label.text()
        # Remove "Result: " prefix if first time appending
        if current_text.startswith("Result: "):
         current_text = current_text.replace("Result: ", "")
         self.result_label.setText(f"{current_text}\n{text}")

    def run_integrity_check(self):
        # Get the results from the backend
        result_text, modified_files, delete_files, unchanged_files = check_integrity()

        # Display in the GUI label
        self.result_label.setText(result_text)

        # (Optional) Send file lists somewhere else if needed
        self.integrity_checker.run_check(modified_files, delete_files, unchanged_files)


    def set_result_text(self, text, color="white"):
        self.result_label.setText(f"Result: {text}")
        self.result_label.setStyleSheet(f"""
        font-size: 24px; 
        font-weight: bold; 
        color: {color};
    """)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: white; }
            QCheckBox { color: white; }
        """)
        self.title_label.setStyleSheet("""
            QLabel {
                padding: 8px 15px;
                border-radius: 8px;
                color: #00FF00;
                background-color: transparent;
            }
            QLabel:hover {
                border: 2px solid #00FF00;
                background-color: rgba(0, 255, 0, 0.15);
            }
        """)
        self.files_container.setStyleSheet("""
            QWidget {
                border: 2px solid green;
                border-radius: 8px;
                background-color: transparent;
            }
        """)

    def set_light_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: white; color: black; }
            QCheckBox { color: black; }
        """)
        self.title_label.setStyleSheet("""
            QLabel {
                padding: 8px 15px;
                border-radius: 8px;
                background-color: transparent;
            }
            QLabel:hover {
                border: 2px solid #00FF00;
                background-color: rgba(0, 255, 0, 0.15);
            }
        """)
        self.files_container.setStyleSheet("""
            QWidget {
                border: 2px solid rgba(0, 0, 0, 1);
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 1);
            }
        """)

    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            self.set_dark_theme()
        else:
            self.set_light_theme()

if __name__ == "__main__":
    
    warnings.filterwarnings("ignore", message="The Python dbus package is not installed.")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())