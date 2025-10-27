import sysimport sys

import argparsefrom PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,                            QHBoxLayout, QPushButton, QTextEdit, QLabel,

                            QHBoxLayout, QPushButton, QTextEdit, QLabel,                            QFileDialog, QMessageBox)

                            QFileDialog, QMessageBox)from PyQt6.QtCore import Qt, QThread, pyqtSignal

from PyQt6.QtCore import Qt, QThread, pyqtSignalfrom jlc2kicadlib import JLCKicad

from JLC2KiCadLib import add_component

class ConversionThread(QThread):

class ConversionThread(QThread):    finished = pyqtSignal(bool, str)

    finished = pyqtSignal(bool, str)    

        def __init__(self, output_dir, part_numbers):

    def __init__(self, output_dir, part_numbers):        super().__init__()

        super().__init__()        self.output_dir = output_dir

        self.output_dir = output_dir        self.part_numbers = part_numbers

        self.part_numbers = part_numbers        

        def run(self):

    def run(self):        try:

        try:            converter = JLCKicad()

            # Create argument parser to match the library's expectations            converter.set_lib_path(self.output_dir)

            parser = argparse.ArgumentParser()            

            parser.add_argument('-dir', dest='output_dir', type=str, default=self.output_dir)            for part_number in self.part_numbers:

            parser.add_argument('--no_footprint', dest='footprint_creation', action='store_false')                if part_number.strip():

            parser.add_argument('--no_symbol', dest='symbol_creation', action='store_false')                    converter.generate_lib(part_number.strip())

            args = parser.parse_args([])  # Parse empty args to get defaults            

            args.output_dir = self.output_dir            self.finished.emit(True, "")

                    except Exception as e:

            for part_number in self.part_numbers:            self.finished.emit(False, str(e))

                if part_number.strip():  # Skip empty lines

                    add_component(part_number.strip(), args)class JLCConverterApp(QMainWindow):

                def __init__(self):

            self.finished.emit(True, "")        super().__init__()

        except Exception as e:        self.setWindowTitle("JLC2KiCad Converter")

            self.finished.emit(False, str(e))        self.setMinimumSize(600, 400)

        

class MainWindow(QMainWindow):        # Create main widget and layout

    def __init__(self):        main_widget = QWidget()

        super().__init__()        self.setCentralWidget(main_widget)

        self.setWindowTitle("JLC2KiCad Converter")        layout = QVBoxLayout(main_widget)

        self.setMinimumSize(600, 400)        

                # Directory selection

        # Create central widget and layout        dir_layout = QHBoxLayout()

        central_widget = QWidget()        dir_label = QLabel("Output Directory:")

        self.setCentralWidget(central_widget)        self.dir_entry = QLabel("No directory selected")

        layout = QVBoxLayout(central_widget)        self.dir_entry.setStyleSheet("background-color: white; padding: 5px; border: 1px solid gray;")

                browse_btn = QPushButton("Browse")

        # Directory selection        browse_btn.clicked.connect(self.browse_directory)

        dir_layout = QHBoxLayout()        

        dir_label = QLabel("Output Directory:")        dir_layout.addWidget(dir_label)

        self.dir_entry = QTextEdit()        dir_layout.addWidget(self.dir_entry, stretch=1)

        self.dir_entry.setMaximumHeight(30)        dir_layout.addWidget(browse_btn)

        browse_btn = QPushButton("Browse")        layout.addLayout(dir_layout)

        browse_btn.clicked.connect(self.browse_directory)        

                # Part numbers input

        dir_layout.addWidget(dir_label)        layout.addWidget(QLabel("Part Numbers:"))

        dir_layout.addWidget(self.dir_entry)        self.parts_text = QTextEdit()

        dir_layout.addWidget(browse_btn)        layout.addWidget(self.parts_text)

        layout.addLayout(dir_layout)        layout.addWidget(QLabel("(One part number per line)"))

                

        # Part numbers input        # Convert button

        parts_label = QLabel("Part Numbers (One per line):")        self.convert_btn = QPushButton("Convert")

        layout.addWidget(parts_label)        self.convert_btn.clicked.connect(self.start_conversion)

                layout.addWidget(self.convert_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.parts_text = QTextEdit()        

        layout.addWidget(self.parts_text)        # Status label

                self.status_label = QLabel("")

        # Convert button        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.convert_btn = QPushButton("Convert")        

        self.convert_btn.clicked.connect(self.start_conversion)        self.output_dir = ""

        layout.addWidget(self.convert_btn)        self.conversion_thread = None

                

        # Status label    def browse_directory(self):

        self.status_label = QLabel("")        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")

        layout.addWidget(self.status_label)        if directory:

                    self.output_dir = directory

        self.conversion_thread = None            # Show only the last part of the path if it's too long

                display_path = directory.split('/')[-1] if len(directory) > 40 else directory

    def browse_directory(self):            self.dir_entry.setText(display_path)

        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")            self.dir_entry.setToolTip(directory)  # Show full path on hover

        if directory:    

            self.dir_entry.setText(directory)    def start_conversion(self):

            if not self.output_dir:

    def start_conversion(self):            QMessageBox.warning(self, "Error", "Please select an output directory")

        output_dir = self.dir_entry.toPlainText().strip()            return

        part_numbers = self.parts_text.toPlainText().strip().split('\n')        

                part_numbers = self.parts_text.toPlainText().strip().split('\n')

        if not output_dir:        if not part_numbers or not part_numbers[0]:

            QMessageBox.critical(self, "Error", "Please select an output directory")            QMessageBox.warning(self, "Error", "Please enter at least one part number")

            return            return

                    

        if not part_numbers or not part_numbers[0]:        # Disable controls during conversion

            QMessageBox.critical(self, "Error", "Please enter at least one part number")        self.convert_btn.setEnabled(False)

            return        self.status_label.setText("Converting...")

                

        # Disable controls during conversion        # Start conversion in a separate thread

        self.convert_btn.setEnabled(False)        self.conversion_thread = ConversionThread(self.output_dir, part_numbers)

        self.status_label.setText("Converting...")        self.conversion_thread.finished.connect(self.conversion_complete)

                self.conversion_thread.start()

        # Start conversion in a separate thread    

        self.conversion_thread = ConversionThread(output_dir, part_numbers)    def conversion_complete(self, success, error_message):

        self.conversion_thread.finished.connect(self.conversion_complete)        self.convert_btn.setEnabled(True)

        self.conversion_thread.start()        

            if success:

    def conversion_complete(self, success, error_message):            self.status_label.setText("Conversion completed successfully!")

        self.convert_btn.setEnabled(True)            QMessageBox.information(self, "Success", "Parts have been converted successfully!")

                else:

        if success:            self.status_label.setText("Error during conversion")

            self.status_label.setText("Conversion completed successfully!")            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")

            QMessageBox.information(self, "Success", "Parts have been converted successfully!")

        else:def main():

            self.status_label.setText("Error during conversion")    app = QApplication(sys.argv)

            QMessageBox.critical(self, "Error", f"An error occurred: {error_message}")    window = JLCConverterApp()

    window.show()

if __name__ == "__main__":    sys.exit(app.exec())

    app = QApplication(sys.argv)

    window = MainWindow()if __name__ == "__main__":

    window.show()    main()
    sys.exit(app.exec())