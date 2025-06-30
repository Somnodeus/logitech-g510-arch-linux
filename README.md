# This repository contains the Logitech G510 keyboard settings for Arch Linux, current as of June 2025

> Attention: Don't forget to replace somnodeus with your linux user name in the configuration files from this guide! 
> Also pay attention to the file paths. Either make the same directories or change the file paths in the scripts and configuration files.

## g15ctrld and key and screen management

Jörg Hettwer wrote an excellent program g15ctrld, which works fine in 2025 on the current version of Arch Linux.
https://gitlab.com/raycollector/g15ctrld
https://aur.archlinux.org/packages/g15ctrld

### Installing g15ctrld

```bash
paru -S g15ctrld
```

Next, we copy the configuration file
```bash
sudo rm /etc/LCDd.conf
sudo cp /etc/LCDd.conf.pacnew /etc/LCDd.conf
```

#### g15ctrld requires ydotool to work

> Attention: You may already have ydotool installed or installed it with `paru -S g15ctrld` command, check it!

```bash
paru -S ydotool
```

To autoload ydotool, you need to create a systemd service. The configuration file option can be taken from the repository https://gitlab.com/raycollector/g15ctrld


```bash
sudo nano /etc/systemd/system/ydotoold.service
```

```ini
[Unit]
Description=ydotoold daemon
After=network.target

[Service]
ExecStart=/usr/bin/ydotoold
Restart=always
User=root
Group=input
CapabilityBoundingSet=CAP_SYS_ADMIN
ProtectSystem=full
ProtectHome=yes
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable ydotool.service
sudo systemctl start ydotool.service
```

#### Restarting services after installing the program

```bash
sudo systemctl enable --now lcdd
sudo systemctl enable --now lcdproc
sudo systemctl enable --now g15ctrld
sudo systemctl enable --now ydotoold
sudo shutdown -r now
```

### Setting up keys in g15ctrld

To record a macro on a button in the desired mode M1, M2 or M3, you need to press MR, press the key combination and press the desired button, for example G18.

To erase a macro from the G18 button, you need to press MR, and then G18.

An alternative option that works with g15ctrld if nothing is configured for the desired key in g15ctrld is to use the Input Remapper program.
https://github.com/sezanzeb/input-remapper

In Input Remapper, everything is configured through the GUI, it is intuitive.
Input Remapper does not conflict with g15ctrld at least until keys are assigned in g15ctrld.

### Setting up the screen in g15ctrld

Configuring `lcdproc.conf`
```bash
nano /etc/lcdproc.conf
```

There are different display options here, you need to write Active or false in the configuration file to enable or disable a specific block.
If you want to display your own monitoring information based on the Conky configuration, see below.

## Setting up buttons around the screen by replacing the LCDd file

The LCDd executable file can be compiled in such a way that it will support the operation of buttons around the display. The buttons will call the menu and switch the display of widgets. For example, you can use built-in (and not disabled via `/etc/lcdproc.conf`) widgets, as well as some of your own.

> Attention. Perhaps the author has already improved the application and the buttons around the screen are already working, check it out!

LCDd with menu support compatible with version g15ctrld 1.6.6-1 from AUR (haven't tested with other versions)
https://mega.nz/file/w6wSWbRQ#Wf621A11oaTIiJ4HoEr1kdL5Rzgi3AS_X3ow_69B-8o

When copying, remember to make the LCDd file executable.
```bash
sudo mv /usr/bin/LCDd /usr/bin/LCDd.bak
sudo cp ~/Downloads/LCDd /usr/bin/LCDd
chmod +x /usr/bin/LCDd
sudo systemctl restart lcdd
```

## Configuration option for displaying monitoring on the screen via Conky

If you have any comments on my scripts, please write.
This method requires a Conky version with LUA support.
https://github.com/brndnmtthws/conky
https://aur.archlinux.org/packages/conky-lua-nv

```bash
paru -s conky-lua-nv
```

> Don't forget to set all blocks in the /etc/lcdproc.conf file to false! Or use a version of the LCDd file that supports buttons around the screen so that you can select the desired widget through the menu.

### Setting up Conky

```bash
nano /home/somnodeus/.config/conky/conky_for_lcd/conky_for_lcd.conf
```

```conf
conky.config = {
    lua_load = '/home/somnodeus/.config/conky/conky_for_lcd/networkspeeds.lua',
    out_to_console = true,
    out_to_x = true,
    out_to_ncurses = false,
    update_interval = 1.0,
    total_run_times = 0,
    template = nil,
    max_text_width = 20,
    pad_percents = 2,
    override_utf8_locale = true,
    
    background = true,
    own_window = true,
    own_window_type = 'desktop',
    own_window_transparent = true,
    own_window_argb_visual = true,
    own_window_argb_value = 0,
    own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',
    double_buffer = true,
    minimum_width = 1,
    minimum_height = 1,
    x_offset = -10000,
    y_offset = -10000,    
};
  
conky.text = [[  
${alignr}${lua conky_cpu_perc_padded} CPU ${cpubar 9}  
${alignr}${lua conky_mem_perc_padded} Mem ${membar 9}  
${alignr}${lua conky_gpu_perc_padded} GPU Up: ${uptime_short}  
${alignr}DL:${lua conky_downloadspeed_formatted} UL:${lua conky_uploadspeed_formatted}  
${alignr}root:${lua conky_fs_root_perc_padded} home:${lua conky_fs_home_perc_padded}  
]];

```

```bash
nano /home/somnodeus/.config/conky/conky_for_lcd/networkspeeds.lua
```

```lua
function conky_cpu_perc_padded()
    local cpu_load = tonumber(conky_parse("${cpu cpu0}")) or 0
    return string.format("%02d%%", cpu_load)
end

function conky_mem_perc_padded()
    local mem_usage = tonumber(conky_parse("${memperc}")) or 0
    return string.format("%02d%%", mem_usage)
end

function conky_fs_root_perc_padded()
    local fs_usage = tonumber(conky_parse("${fs_used_perc /}")) or 0
    return string.format("%02d%%", fs_usage)
end

function conky_fs_home_perc_padded()
    local fs_usage = tonumber(conky_parse("${fs_used_perc /home}")) or 0
    return string.format("%02d%%", fs_usage)
end

function conky_uploadspeed_formatted()    
    local speed_str = conky_parse("${upspeed enp7s0}")
    local val_mbps = 0    
    
    local num_part = string.match(speed_str, "([%d%.,]+)") 
    local unit_part = string.match(speed_str, "[%a]+$")    

    if num_part then
        
        num_part = string.gsub(num_part, ",", ".")
        local value = tonumber(num_part) or 0

        if unit_part == "MiB" or unit_part == "MB" then
            val_mbps = value * 8 -- MB/s * 8 = Mbits/s
        elseif unit_part == "KiB" or unit_part == "KB" then
            val_mbps = value * 8 / 1024 -- KB/s * 8 / 1024 = Mbits/s
        elseif unit_part == "B" then
            val_mbps = value * 8 / 1024 / 1024 -- B/s * 8 / 1024 / 1024 = Mbits/s
        end
    end

    local formatted_mbps
    if val_mbps >= 100.0 then
        formatted_mbps = string.format("%.1f", val_mbps)
    elseif val_mbps >= 10.0 then
        formatted_mbps = string.format("%5.1f", val_mbps)
    else
        formatted_mbps = string.format("%5.1f", val_mbps)
    end

    formatted_mbps = string.gsub(formatted_mbps, "%.", ",")
    return formatted_mbps
end


function conky_downloadspeed_formatted()
    local speed_str = conky_parse("${downspeed enp7s0}")
    local val_mbps = 0

    local num_part = string.match(speed_str, "([%d%.,]+)")
    local unit_part = string.match(speed_str, "[%a]+$")

    if num_part then
        num_part = string.gsub(num_part, ",", ".")
        local value = tonumber(num_part) or 0

        if unit_part == "MiB" or unit_part == "MB" then
            val_mbps = value * 8
        elseif unit_part == "KiB" or unit_part == "KB" then
            val_mbps = value * 8 / 1024
        elseif unit_part == "B" then
            val_mbps = value * 8 / 1024 / 1024
        end
    end

    local formatted_mbps
    if val_mbps >= 100.0 then
        formatted_mbps = string.format("%.1f", val_mbps)
    elseif val_mbps >= 10.0 then
        formatted_mbps = string.format("%5.1f", val_mbps)
    else
        formatted_mbps = string.format("%5.1f", val_mbps)
    end

    formatted_mbps = string.gsub(formatted_mbps, "%.", ",")
    return formatted_mbps
end

```

### Script

```bash
nano /home/somnodeus/.config/0_my/my_lcd_client.py
```

```python
import sys
import socket
import time

HOST = 'localhost' 
PORT = 13666       
SCREEN_DURATION = 5

def send_command(sock, command):
    """Sends a command to LCDd and returns the response."""
    try:
        sock.sendall((command + '\n').encode('utf-8'))
        response = sock.recv(1024).decode('utf-8').strip()
        return response
    except socket.error as e:
        print(f"Socket error during send/receive: {e}")
        return None

def main():
    sock = None
    try:
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"Connected to LCDd on {HOST}:{PORT}")
        
        send_command(sock, "hello")
        send_command(sock, "client_set name conky_lcd_client")

        screen_id = 'conky_info_screen'

        send_command(sock, f'screen_add {screen_id}')
        send_command(
            sock,
            f'screen_set {screen_id} -name "Conky Info" -priority 255 -duration {SCREEN_DURATION} -heartbeat off'
        )

        for i in range(1, 6):
            send_command(sock, f'widget_add {screen_id} line{i} string')

        print("Starting LCD client, waiting for Conky data via stdin...")

        line_buffer = []

        for raw_line in sys.stdin:
            processed_line = raw_line.strip()
            if processed_line:
                line_buffer.append(processed_line)
                
                if len(line_buffer) == 5:
                    for idx, text in enumerate(line_buffer):

                        if len(text) > 20:
                            text = text[:20]

                        send_command(
                            sock,
                            f'widget_set {screen_id} line{idx+1} 1 {idx+1} "{text}"'
                        )

                    line_buffer = []

    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    except ConnectionRefusedError:
        print(f"Error: Could not connect to LCDd on {HOST}:{PORT}. Make sure LCDd is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if sock:
            print("Closing connection to LCDd.")
            sock.close()

if __name__ == '__main__':
    main()

```

### Manual launch of the resulting script

```bash
conky -c ~/.config/conky/conky_for_lcd/conky_for_lcd.conf | python3 my_lcd_client.py &
```

### Autostart on login in KDE

#### 1. Shell script wrapper

Create a file, for example, `~/.local/bin/start_lcd_conky.sh` (don't forget to set `chmod +x`):

```bash
#!/usr/bin/env bash

sudo systemctl stop lcdd lcdproc g15ctrld
sudo systemctl start lcdd lcdproc g15ctrld

sleep 1

exec conky -c "$HOME/.config/conky/conky_for_lcd/conky_for_lcd.conf" \
     | python3 "/home/somnodeus/.config/0_my/my_lcd_client.py"
```

> **Important:**
To prevent this script from asking for a password when `sudo systemctl`, add a line like this to `sudoers` (via `sudo visudo`):

 ```
somnodeus ALL=(root) NOPASSWD: /usr/bin/systemctl stop lcdd lcdproc g15ctrld
somnodeus ALL=(root) NOPASSWD: /usr/bin/systemctl start lcdd lcdproc g15ctrld
 ```

#### 2. Autostart via KDE

Create a file `~/.config/autostart/conky-lcd-client.desktop` with the following content:

```ini
[Desktop Entry]
Type=Application
Exec=bash -c "sleep 7 && /home/somnodeus/.local/bin/start_lcd_conky.sh"
Hidden=false
X-GNOME-Autostart-enabled=true
Name=LCD Conky Client
Comment=Restarting LCD services and launching Conky→LCD client
```

* The next time you log into KDE, this script will be automatically run.

#### 3. Check

1. **Manual start**

   ```bash
   ~/.local/bin/start_lcd_conky.sh
   ```

Make sure that services restart without password and that Conky strings are displayed on G15/LCD.

2. **Relogin to KDE**
The script will run automatically when you log in.

If something doesn't work (e.g. services don't restart without password), check `sudoers` and service paths. Otherwise, this is a solid way to integrate your client into KDE startup.

## Commands for adjusting screen brightness and backlighting Logitech G510

Backlighting brightness is changed by the command
```bash
echo 255 | sudo tee /sys/class/leds/g15::kbd_backlight/brightness
```
Where 255 is the maximum brightness, 0 is the minimum.

The backlight color is set by the command
```bash
echo 255 255 255 | sudo tee /sys/class/leds/g15::kbd_backlight/multi_intensity
```
Accordingly, R, G and B are given separately and the final color is obtained.

## Permanent backlight setting in Garuda Linux

### systemd service to set color at boot

```bash
sudo nano /usr/local/bin/set_g510_color.sh
```

```bash
#!/bin/bash

# Set your desired RGB values ​​here (e.g. for white)
# Format: RED GREEN BLUE (values ​​from 0 to 255, separated by spaces)
COLOR_VALUES="255 255 255" # white

echo "$COLOR_VALUES" > /sys/class/leds/g15::kbd_backlight/multi_intensity
```

```bash
sudo chmod +x /usr/local/bin/set_g510_color.sh
```

```bash
sudo nano /etc/systemd/system/g510-backlight.service
```

```ini
[Unit]
Description=Set Logitech G510 Keyboard Backlight Color
After=sys-devices-platform.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/set_g510_color.sh

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable g510-backlight.service
sudo systemctl start g510-backlight.service
systemctl status g510-backlight.service
```

### Additionally, you can configure udev

Restore color when reconnecting the keyboard

```bash
sudo nano /etc/udev/rules.d/99-g510-backlight.rules
```

```
ACTION=="add", SUBSYSTEM=="leds", KERNEL=="g15::kbd_backlight", RUN+="/bin/sh -c 'echo \"255 255 255\" > /sys/class/leds/g15::kbd_backlight/multi_intensity'"
```

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Restart g15ctrld when reconnecting keyboard

```bash
sudo nano /etc/udev/rules.d/90-g510-service-restart.rules
```

```
ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c22d", RUN+="/bin/sh -c 'sudo systemctl stop lcdd && sudo systemctl stop lcdproc && sudo systemctl stop g15ctrld && sudo systemctl start lcdd && sudo systemctl start lcdproc && sudo systemctl start g15ctrld'"
```

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### And also when entering KDE

```bash
nano ~/.local/bin/set_g510_color_kde_login.sh
```

```bash
#!/bin/bash

sleep 5
COLOR_VALUES="255 255 255"

echo "$COLOR_VALUES" | sudo tee /sys/class/leds/g15::kbd_backlight/multi_intensity
```

```bash
chmod +x ~/.local/bin/set_g510_color_kde_login.sh
```

```bash
nano ~/.config/autostart/set_g510_color.desktop
```

```
[Desktop Entry]  
Type=Application  
Exec=/home/somnodeus/.local/bin/set_g510_color_kde_login.sh  
Hidden=false  
NoDisplay=false  
X-KDE-AutostartScript=true  
Name=Set G510 Color  
Comment=Customize Logitech G510 Keyboard Color When Logging In to KDE
Terminal=false  
StartupNotify=false
```

```bash
sudo visudo
```

```
somnodeus ALL=(root) NOPASSWD: /usr/bin/tee /sys/class/leds/g15\:\:kbd_backlight/multi_intensity
```

## Python script to adjust the backlight of the Logitech G510 via GUI


```bash
nano  g510_control.py
```

```python
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
```

```bash
nano g510_control.desktop
```

```ini
#!/usr/bin/env xdg-open
[Desktop Entry]
Name=Logitech G510 Control
Comment=Control backlight for Logitech G510 keyboard
Exec=python3 /home/somnodeus/.config/0_my/g510_control.py
Icon=/home/somnodeus/.config/0_my/logitech_g510.png
Terminal=false
Type=Application
Categories=Settings;Utility;
```
