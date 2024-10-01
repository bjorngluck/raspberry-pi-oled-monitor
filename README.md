# OLED System Monitor for Raspberry Pi Cluster

This project provides a dynamic system monitoring display for your Raspberry Pi cluster. It utilizes an SSD1306 OLED display to show real-time information such as CPU load, memory usage, disk usage, running Docker containers, and system information.

## Table of Contents

- [Introduction](#introduction)
- [Hardware Requirements](#hardware-requirements)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Run as a Service](#run-as-a-service)
- [Code Explanation](#code-explanation)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)
- [Contact](#contact)
- [Repository](#repository)
- [Screenshots](#screenshots)
- [Dependencies and Links](#dependencies-and-links)
- [Final Notes](#final-notes)

## Introduction

As part of building a new Raspberry Pi cluster with a custom 3D-printed case (design in progress), this project aims to provide a visual interface to monitor system metrics. The OLED display is mounted on the cluster case and cycles through various system statistics, providing at-a-glance information.

## Hardware Requirements

- **Raspberry Pi** (any model with I2C support)
- **SSD1306 OLED Display** (128x64 pixels, dual-color optional)
  - Purchase link: [SSD1306 OLED Display on Temu](https://share.temu.com/CKcEp5PY9LA)

## Dependencies

Ensure the following Python libraries are installed:

- [Adafruit CircuitPython SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)
- [Pillow (PIL) Imaging Library](https://python-pillow.org/)
- [Adafruit Blinka](https://github.com/adafruit/Adafruit_Blinka) (for CircuitPython support on Raspberry Pi)

## Installation
1. Enable I2C on Raspberry Pi:
   Run `sudo raspi-config`, navigate to Interface Options, and enable I2C.

2. Connect the OLED Display:
   - SDA to GPIO 2 (SDA1)
   - SCL to GPIO 3 (SCL1)
   - VCC to 3.3V
   - GND to GND

3. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/raspberry-pi-oled-monitor.git
   cd raspberry-pi-oled-monitor
   ```
   
4. Install Python Dependencies `pip`:
   ```bash
   pip install adafruit-circuitpython-ssd1306
   pip install Pillow
   pip install adafruit-blinka
   ```
   
## Usage
Run the Python script to start the system monitor:
```bash
python3 oled_system_monitor.py
```
Note: Ensure you have the necessary permissions to access I2C and Docker without using sudo. You may need to add your user to the i2c and docker groups:

```bash
sudo usermod -aG i2c,docker $(whoami)
```
Log out and log back in for the group changes to take effect.

## Run as a Service
1. Now create the service so that the script automaticall starts on reboot and no manual intervention is needed. Make sure you copy over the contents of the `oled_display.service` file that is part of this repo. Make sure to replace the `{Your_Username}` attribute with your username where the script is stored 
   ```bash
   sudo nano /etc/systemd/system/oled_display.service
   ```
2. Now we need to reload the daemon
   ```bash
   sudo systemctl daemon-reload
   ```
3. Let’s enable enable the service
   ```bash
   sudo systemctl enable oled_display.service
   ```
4. Starting the service.
   ```bash
   sudo systemctl start oled_display.service
   ```

**Other userful service commands**
There are several commands you can do to start, stop, restart, and check status.

1. To stop the service.
   ```
   sudo systemctl stop oled_display.service
   ```
2. To restart.
   ```
   sudo systemctl restart oled_display.service
   ```
3. To check status.
   ```
   sudo systemctl status oled_display.service
   ```

## Code Explanation
The script performs the following functions:

- **Scrolling Text Display:**
  - Displays a scrolling text (e.g., hostname or custom message) at the top of the OLED screen.
  - The text scrolls smoothly across the screen, providing a marquee effect.
- **System Statistics Screens:**
  - **CPU Load:**
    - Displays current CPU usage percentage.
    - Shows a line graph of CPU usage over time.
  - **Memory Usage:**
    - Displays used memory in MB and percentage.
    - Shows a line graph of memory usage over time.
  - **Disk Usage:**
    - Displays used disk space in GB and percentage.
    - Shows a line graph of disk usage over time.
  - **Docker Containers:**
    - Lists running Docker containers with their status.
  - **System Info:**
    - Displays OS version.
    - Shows the date of the last system update.
    - Indicates if a system reboot is pending.
- **Screen Rotation:**
  - Cycles through the different screens every 3 seconds.
  - Uses a list (stats) to manage the rotation.
- **Graphics and Layout:**
  - Utilizes the Pillow library to draw text and graphics on the OLED display.
  - Adjusts positions and font sizes to accommodate dual-color displays (e.g., yellow and blue regions).

## Future Enhancements
 - **3D-Printed Case Integration:**
   - The display will be mounted on a custom 3D-printed case for the Raspberry Pi cluster.
   - Case design is in progress and will be available soon.
- **Open Source Contributions:**
   - The code will be open-sourced, and contributions are welcome.
   - Please acknowledge the original author when using or modifying the code.

## License
This project is licensed under the MIT License - see the [LICENSE file](https://github.com/bjorngluck/raspberry-pi-oled-monitor/blob/main/LICENSE) for details.

## Acknowledgements
- **Temu:** Bought a pack of 5 displays [SSD1306 OLED Display](https://share.temu.com/CKcEp5PY9LA).
- **Adafruit:** Libraries and examples provided by Adafruit greatly facilitated the development of this project.
- **Community:** Inspired by various open-source projects and the Raspberry Pi community.
Note: This project is not affiliated with or endorsed by Temu or the display seller. The link provided is for convenience to obtain the same hardware used in this project.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss changes or enhancements.

## Contact
For questions or suggestions, please contact:
- **Name:** Björn
- **Email:** TBC

## Repository
The source code is available on GitHub:
- [Raspberry Pi OLED System Monitor](https://github.com/bjorngluck/raspberry-pi-oled-monitor)

## Screenshots
![Containers](https://github.com/user-attachments/assets/525626d0-5dcf-4e50-8909-af25fc43a4da)
![Sys_Info](https://github.com/user-attachments/assets/3a4ec3b4-4353-44bd-99c2-7f0b436b3a53)
![Memory](https://github.com/user-attachments/assets/b7c44d91-2e67-4700-b1c0-def53467cef1)


**Disclaimer:** Use this code at your own risk. The author is not responsible for any damage or data loss resulting from the use of this code.

## Dependencies and Links
- Adafruit CircuitPython SSD1306: [GitHub Repository](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)
- Pillow (PIL) Imaging Library: [Official Website](https://python-pillow.org/)
- Adafruit Blinka: [GitHub Repository](https://github.com/adafruit/Adafruit_Blinka)
- SSD1306 OLED Display: [Purchase on Temu](https://share.temu.com/CKcEp5PY9LA)

**Note:** Ensure that you have all the necessary permissions and comply with the licenses of the libraries and resources used in this project.

## Final Notes
Thank you for using this OLED system monitor for your Raspberry Pi cluster. I hope it enhances your project's functionality and provides valuable insights into your system's performance.
