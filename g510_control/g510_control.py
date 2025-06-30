import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QPushButton, QColorDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

# Paths to the backlight control files in /sys/
# Make sure 'g15::kbd_backlight' matches your system.
BRIGHTNESS_FILE = "/sys/class/leds/g15::kbd_backlight/brightness"
COLOR_FILE = "/sys/class/leds/g15::kbd_backlight/multi_intensity"

class LogitechG510Control(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logitech G510 Backlight Control")
        self.setFixedSize(400, 100)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.current_color = QColor(255, 255, 255) # Initial color is white

        self._create_ui()

    def _create_ui(self):
        """Creates the user interface elements."""

        # --- Brightness Slider ---
        brightness_label = QLabel("Brightness")
        self.layout.addWidget(brightness_label)

        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 255)
        self.brightness_slider.setValue(255)
        self.brightness_slider.setToolTip("Move to change brightness")
        self.brightness_slider.sliderReleased.connect(self.change_brightness)
        self.layout.addWidget(self.brightness_slider)

        # --- Color Selection ---
        color_layout = QHBoxLayout()

        self.color_button = QPushButton("Select Color")
        self.color_button.setToolTip("Click to open the color palette")
        self.color_button.clicked.connect(self.open_color_dialog)
        color_layout.addWidget(self.color_button)

        # --- Color Swatch ---
        self.color_swatch = QLabel()
        self.color_swatch.setFixedSize(100, 30)
        self.color_swatch.setAutoFillBackground(True)
        self.update_color_swatch(self.current_color)
        color_layout.addWidget(self.color_swatch)

        self.layout.addLayout(color_layout)

    def run_command_with_pkexec(self, command_path, input_data):
        """
        Executes a command with superuser privileges via pkexec.
        'pkexec' will graphically prompt for a password. This is the modern standard.
        """
        try:
            # Using pkexec, the modern standard for requesting privileges
            full_command = ['sudo', 'tee', command_path]
            # full_command = ['pkexec', 'tee', command_path]
            process = subprocess.run(
                full_command,
                input=input_data,
                text=True,
                check=True,
                capture_output=True
            )
            print("Command executed successfully.")
            if process.stderr:
                print("stderr:", process.stderr.strip())
        except FileNotFoundError:
            print("Error: 'pkexec' command not found. Make sure the 'polkit' package is installed.")
        except subprocess.CalledProcessError as e:
            # This error occurs if the user cancels the password entry or another problem happens
            print(f"Error executing command (possibly cancelled by user): {e}")
            print(f"Stderr: {e.stderr.strip()}")

    def change_brightness(self):
        """Changes the keyboard brightness."""
        value = self.brightness_slider.value()
        print(f"Setting brightness: {value}")
        self.run_command_with_pkexec(BRIGHTNESS_FILE, str(value))

    def open_color_dialog(self):
        """Opens the color selection dialog."""
        color = QColorDialog.getColor(self.current_color, self, "Select Backlight Color")
        if color.isValid():
            self.current_color = color
            self.update_color_swatch(color)
            self.change_color()

    def change_color(self):
        """Changes the keyboard backlight color."""
        r = self.current_color.red()
        g = self.current_color.green()
        b = self.current_color.blue()

        color_string = f"{r} {g} {b}"
        print(f"Setting color: {color_string}")
        self.run_command_with_pkexec(COLOR_FILE, color_string)

    def update_color_swatch(self, color):
        """Updates the color of the swatch widget."""
        palette = self.color_swatch.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.color_swatch.setPalette(palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LogitechG510Control()
    window.show()
    sys.exit(app.exec())