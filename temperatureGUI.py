from sys import exit
from temperature import CelsiusTemperature, FahrenheitTemperature
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QGridLayout, QLineEdit, QLabel, QPushButton, QRadioButton)

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize central widget and layout
        # Outer column layout using QVBox
        # contains Grid for user input and QHBox for result display
        self.center = QWidget()
        self.outer_column_layout = QVBoxLayout()
        self.input_grid = QGridLayout()
        self.results_box = QHBoxLayout()

        # First grid row -value input- initialization (label, input field, button)
        self.degree_input_label = QLabel("Number of Degrees:")
        self.degree_input = QLineEdit()
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)

        # Second grid row -degree type select- initialization (label, radio buttons)
        self.degree_type_label = QLabel("Degree Type:")
        self.radio_f = QRadioButton("Fahrenheit")
        self.radio_c = QRadioButton("Celsius")

        # Second vertical box -results display- initialization (text labels)
        self.fahrenheit_result = QLabel("Degrees Fahrenheit: ")
        self.celsius_result = QLabel("Degrees Celsius: ")

        # Third vertical box -error display- initialization (text label)
        self.error_display = QLabel()

        # Set up UI with initialized values
        self.init_ui()

    def init_ui(self):
        # Add first row to input grid
        self.input_grid.addWidget(self.degree_input_label, 0, 0)
        self.input_grid.addWidget(self.degree_input, 0, 1)
        self.input_grid.addWidget(self.button, 0, 2)

        # Add second row to input grid
        self.input_grid.addWidget(self.degree_type_label, 1, 0)
        self.input_grid.addWidget(self.radio_f, 1, 1)
        self.input_grid.addWidget(self.radio_c, 1, 2)

        # Add result labels to results box
        self.results_box.addWidget(self.fahrenheit_result)
        self.results_box.addWidget(self.celsius_result)

        # Add boxes to outer column layout
        self.outer_column_layout.addLayout(self.input_grid)
        self.outer_column_layout.addLayout(self.results_box)
        self.outer_column_layout.addWidget(self.error_display)

        # Add layout to central widget and add to main window
        self.center.setLayout(self.outer_column_layout)
        self.setCentralWidget(self.center)
        self.setWindowTitle("Temperature Conversion App")

    @Slot()
    def convert(self):
        # Terminates callback if user input is bad
        input_text = self.degree_input.text()
        if not self.validate_input(input_text): return

        # Turns input into either Celsius or Fahrenheit object depending on radio buttons
        if self.radio_f.isChecked():
            temp = FahrenheitTemperature(input_text)
        elif self.radio_c.isChecked():
            temp = CelsiusTemperature(input_text)
        else: # Refuses to do anything if radio button not selected
            self.error_display.setText("Error: degree type not selected")
            self.fahrenheit_result.setText("Degrees Fahrenheit: ")
            self.celsius_result.setText("Degrees Celsius: ")
            return

        # Sets results on third row using polymorphic temperature functions
        fahrenheit_str = str(temp.as_fahrenheit()) + " \u00b0" + "F"
        celsius_str = str(temp.as_celsius())  + " \u00b0" + "C"
        self.fahrenheit_result.setText("Degrees Fahrenheit: " + f"{fahrenheit_str:>12}")
        self.celsius_result.setText("Degrees Celsius: " + f"{celsius_str:>12}")
        self.error_display.setText("")

    def validate_input(self, input_text):
        # Make sure there are no letters in the input and that input can convert to float
        # Perhaps this sort of exception handling should be moved to class?
        try:
            if any(char.isalpha() for char in input_text): raise ValueError
            float(input_text)

        # Either of those operations failing should produce a value error
        except ValueError:
            self.error_display.setText("Error: invalid degree input")
            self.fahrenheit_result.setText("Degrees Fahrenheit: ")
            self.celsius_result.setText("Degrees Celsius: ")
            return False

        # Unknown situation, general error message
        except Exception as e:
            self.error_display.setText(f"An unexpected error: {repr(e)} occurred")
            self.fahrenheit_result.setText("Degrees Fahrenheit: ")
            self.celsius_result.setText("Degrees Celsius: ")
            return False
        return True


def main():
    app = QApplication([])
    widget = AppWindow()
    widget.resize(400, 1)
    widget.show()
    exit(app.exec())

if __name__ == "__main__":
    main()