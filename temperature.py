import unittest
from abc import ABC, abstractmethod

DEG = "\u00b0" # Degree character code

# Abstract class for Celsius and Fahrenheit implementation
class Temperature(ABC):
    def __init__(self, temp):
        self._temp = float(temp)

    # Meant to return a Celsius representation of the temperature
    @abstractmethod
    def as_celsius(self):
        pass

    # Meant to return a Fahrenheit representation of the temperature
    @abstractmethod
    def as_fahrenheit(self):
        pass

    # Returns a string that shows the temperature represented in both C and F
    def __str__(self):
        return f"{self.as_celsius():.1f}{DEG}C/" + f"{self.as_fahrenheit():.1f}{DEG}F"

    # Converts a temperature from the format provided to the other
    def _convert_temp(self, original_format):
        if original_format == "C":
            new_value = self._temp * 1.8 + 32
            return round(new_value, 1)

        elif original_format == "F":
            new_value = (self._temp - 32) / 1.8
            return round(new_value, 1)

        else:
            raise ValueError("Invalid temperature format, please enter F or C")

# Represents temperature in Celsius
class CelsiusTemperature(Temperature):
    def __init__(self, temp):
        super().__init__(temp)

    def as_celsius(self):
        return round(self._temp, 1)

    def as_fahrenheit(self):
        return super()._convert_temp("C")

# Represents temperature in Fahrenheit
class FahrenheitTemperature(Temperature):
    def __init__(self, temp):
        super().__init__(temp)

    def as_celsius(self):
        return super()._convert_temp("F")

    def as_fahrenheit(self):
        return round(self._temp, 1)

# Framework for other test classes to inherit from
class BaseTemperatureTest(ABC):

    # Must be implemented in order for tests to run properly
    @abstractmethod
    def setUp(self):
        pass

    # Confirm that as_celsius, as_fahrenheit, and __str__ function as expected at both freezing and boiling temps
    def test_celsius_freezing(self):
        self.assertEqual(self._freezing_temp.as_celsius(), 0.0)

    def test_fahrenheit_freezing(self):
        self.assertEqual(self._freezing_temp.as_fahrenheit(), 32.0)

    def test_str_freezing(self):
        self.assertEqual(str(self._freezing_temp), f"0.0{DEG}C/32.0{DEG}F")

    def test_celsius_boiling(self):
        self.assertEqual(self._boiling_temp.as_celsius(), 100.0)

    def test_fahrenheit_boiling(self):
        self.assertEqual(self._boiling_temp.as_fahrenheit(), 212.0)

    def test_str_boiling(self):
        self.assertEqual(str(self._boiling_temp), f"100.0{DEG}C/212.0{DEG}F")

# CelsiusTemperature and FahrenheitTemperature test class implementations
# Due to polymorphism and identical tests, implementation only requires defining variables
class TestCelsiusTemperature(unittest.TestCase, BaseTemperatureTest):
    def setUp(self): #initializes freezing and boiling temps in Celsius for test functions
        self._freezing_temp = CelsiusTemperature(0)
        self._boiling_temp = CelsiusTemperature(100)

class TestFahrenheitTemperature(unittest.TestCase, BaseTemperatureTest):
    def setUp(self):#initializes freezing and boiling temps in Fahrenheit for test functions
        self._freezing_temp = FahrenheitTemperature(32)
        self._boiling_temp = FahrenheitTemperature(212)


def main():
    temp = CelsiusTemperature(100)
    print(f"{temp.as_celsius()}   {temp.as_fahrenheit()}   {temp}")
    return


if __name__ == '__main__':
    main()