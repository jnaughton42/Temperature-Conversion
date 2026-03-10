import sys

from temperature import CelsiusTemperature, FahrenheitTemperature
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize central widget and layout
        self.center = QWidget()
        self.outer_column_layout = QVBoxLayout()
        self.input_grid = QGridLayout()

        # First row -value input- initialization (label, input field, button)
        degree_input_label = QLabel("Number of Degrees:")
        self.degree_input = QLineEdit()
        self.button = QPushButton("Convert")
        self.button.clicked.connect(self.convert)

        # Second row -degree type select- initialization (label, radio buttons)
        degree_type_label = QLabel("Degree Type:")
        self.radio_f = QRadioButton("Fahrenheit")
        self.radio_c = QRadioButton("Celsius")

        # Third row -results display- initialization (text fields)
        self.result_label = QLabel("Results:")
        self.fahrenheit_result = QLabel()
        self.celsius_result = QLabel()

        # Add first row to layout
        self.input_grid.addWidget(degree_input_label, 0, 0)
        self.input_grid.addWidget(self.degree_input, 0, 1)
        self.input_grid.addWidget(self.button, 0, 2)

        # Add second row to layout
        self.input_grid.addWidget(degree_type_label, 1, 0)
        self.input_grid.addWidget(self.radio_f, 1, 1)
        self.input_grid.addWidget(self.radio_c, 1, 2)

        # Add third row to layout
        self.input_grid.addWidget(self.result_label, 2, 0)
        self.input_grid.addWidget(self.fahrenheit_result, 2, 1)
        self.input_grid.addWidget(self.celsius_result, 2, 2)

        # Add layout to central widget and add to main window
        self.outer_column_layout.addLayout(self.input_grid)
        self.center.setLayout(self.outer_column_layout)
        self.setCentralWidget(self.center)
        self.setWindowTitle("Temperature Conversion App")

    @Slot()
    def convert(self):
        input_text = self.degree_input.text()

        try: # Make sure there are no letters in the input and that input can convert to float
            if any(char.isalpha() for char in input_text): raise ValueError
            float(input_text)
        except ValueError: # Either of those operations failing should produce a value error
            self.fahrenheit_result.setText("Error: invalid degree input")
            self.celsius_result.setText("")
            return
        except Exception: # Unknown situation, general error message
            self.fahrenheit_result.setText("Error: unknown error")
            self.celsius_result.setText("")
            return

        # Turns input into either Celsius or Fahrenheit object depending on radio buttons
        if self.radio_f.isChecked():
            temp = FahrenheitTemperature(input_text)
        elif self.radio_c.isChecked():
            temp = CelsiusTemperature(input_text)
        else: # Refuses to do anything if radio button not selected
            self.fahrenheit_result.setText("Error: degree type not selected")
            self.celsius_result.setText("")
            return
        # Sets results on third row using polymorphic temperature functions
        self.fahrenheit_result.setText(str(temp.as_fahrenheit()) + " \u00b0" + "F")
        self.celsius_result.setText(str(temp.as_celsius()) + " \u00b0" + "C")


def main():
    app = QApplication([])
    widget = AppWindow()
    widget.resize(380, 1)
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()