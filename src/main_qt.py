import sys
import argparse
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QLabel,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from easyeda2kicad import EasyEDAToKicad

class ConversionThread(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, output_dir, part_numbers):
        super().__init__()
        self.output_dir = output_dir
        self.part_numbers = part_numbers

    def run(self):
        try:
            converter = EasyEDAToKicad()
            converter.set_output_dir(self.output_dir)

            for part_number in self.part_numbers:
                if part_number.strip():
                    converter.convert_component(part_number.strip())

            self.finished.emit(True, "")
        except Exception as e:
            self.finished.emit(False, str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EasyEDA to KiCad Converter")
        self.setMinimumSize(600, 400)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Directory selection
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Output Directory:")
        self.dir_entry = QTextEdit()
        self.dir_entry.setMaximumHeight(30)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_directory)

        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_entry)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)

        # Part numbers input
        parts_label = QLabel("Part Numbers (One per line):")
        layout.addWidget(parts_label)

        self.parts_text = QTextEdit()
        layout.addWidget(self.parts_text)

        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_btn)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.conversion_thread = None

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.dir_entry.setText(directory)

    def start_conversion(self):
        output_dir = self.dir_entry.toPlainText().strip()
        part_numbers = self.parts_text.toPlainText().strip().split('\n')

        if not output_dir:
            QMessageBox.critical(self, "Error", "Please select an output directory")
            return

        if not part_numbers or not part_numbers[0]:
            QMessageBox.critical(self, "Error", "Please enter at least one part number")
            return

        # Disable controls during conversion
        self.convert_btn.setEnabled(False)
        self.status_label.setText("Converting...")

        # Start conversion in a separate thread
        self.conversion_thread = ConversionThread(output_dir, part_numbers)
        self.conversion_thread.finished.connect(self.conversion_complete)
        self.conversion_thread.start()

    def conversion_complete(self, success, error_message):
        self.convert_btn.setEnabled(True)

        if success:
            self.status_label.setText("Conversion completed successfully!")
            QMessageBox.information(self, "Success", "Parts have been converted successfully!")
        else:
            self.status_label.setText("Error during conversion")
            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()